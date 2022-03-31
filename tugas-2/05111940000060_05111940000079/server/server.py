import os
import socket
import select
import sys
import threading
from os import path
import configparser

from numpy import size

def convert_to_bytes(no):
    result = bytearray()
    result.append(no & 255)
    for i in range(3):
        no = no >> 8
        result.append(no & 255)
    return result

def check_file(paths):
    is_exist = path.exists(paths)
    is_file = path.isfile(paths)

    return is_exist and is_file

def check_folder(paths):
    is_exist = path.exists(paths)
    is_folder = path.isdir(paths)

    return is_exist and is_folder

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.size = 1024
        self.server = None
        self.client_threads = []

    def init_socket(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.host, self.port))
        self.server.listen(5)

    def run(self):
        self.init_socket()
        input_socket = [self.server]
        running = 1

        while running:
            read_ready, write_ready, exception = select.select(input_socket, [], [])
            
            for sock in read_ready:
                if sock == self.server:
                    client_socket, client_address = self.server.accept()
                    client = Client(client_socket, client_address)
                    client.run()
                    self.client_threads.append(client_socket)                       
                
                elif sock == sys.stdin:
                    # handle standard input
                    _ = sys.stdin.readline()
                    running = 0

        # close threads
        self.server.close()
        for client in self.client_threads:
            client.join()

class Client(threading.Thread):
    def __init__(self, client, address):
        self.client = client
        self.address = address
        self.size = 1024

    def get_index(self, request_file, request_dir):
        response_header = b''
        response_data = b''

        if request_file == '/' or request_file == '/index.html':
            f = open('index.html', 'r')
        else:
            f = open(request_dir + '/' + 'index.html', 'r')
        response_data = f.read()
        f.close()
        
        content_length = len(response_data)
        response_header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=UTF-8\r\nContent-Length:' \
                        + str(content_length) + '\r\n\r\n'
        self.client.sendall(response_header.encode('utf-8') + response_data.encode('utf-8'))

    def get_listdir(self, request_dirname):
        response_header = b''
        response_data = b''

        response_data = '''
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta http-equiv="X-UA-Compatible" content="IE=edge">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Document</title>
            </head>
            <body>
                Index of directory
            '''
        for root, dirs, files in os.walk(path.join(request_dirname), topdown=False):
            for name in files:
                response_data += '''
                <div>
                File: {}
                </div>
                '''.format(name)
            for name in dirs:
                response_data += '''
                <div>
                Folder: {}
                </div>
                '''.format(name)
        response_data += '''
        </body>
        </html>
        '''
        content_length = len(response_data)
        response_header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=UTF-8\r\nContent-Length:' \
                        + str(content_length) + '\r\n\r\n'

        self.client.sendall(response_header.encode('utf-8') + response_data.encode('utf-8'))

    def get_file(self, file_path):
        response_header = b''
        data_send = b''

        file = open(file_path, 'rb')
        data_send = file.read()
        file.close()

        length = len(data_send)
        byte = 0

        if length < self.size:
            print("Y")
            self.client.sendall(data_send)
        else:
            while byte < length:
                self.client.send(data_send[byte:byte+self.size])
                byte += self.size
        
    def get_404(self):
        response_header = b''
        response_data = b''

        f = open('404.html', 'r')
        response_data = f.read()
        f.close()
        
        response_header = 'HTTP/1.1 404 Not Found\r\n\r\n'

        self.client.sendall(response_header.encode('utf-8') + response_data.encode('utf-8'))

    def run(self):
        running = 1
        while running:
            data = self.client.recv(self.size)
            if data:
                data = data.decode('utf-8')
                request_header = data.split('\r\n')
                print(request_header[0])

                request_file = request_header[0].split(" ")[1]
                request_dirname = path.dirname(request_file)
                request_basename = path.basename(request_file)
                request_fullname = request_dirname[1:] + "/" + request_basename
                print("request_fullname : " + request_fullname)

                
                if request_file == '/' \
                    or request_basename == 'index.html' \
                    or (check_folder(request_dirname[1:]) and not check_file(request_fullname)):
                    try:
                        self.get_index(request_file, request_dirname[1:])
                        
                    except IOError:
                        self.get_listdir(request_dirname[1:])

                elif check_file(request_fullname):
                    self.get_file(request_fullname)

                else:
                    try:
                        print(request_file)
                        self.get_404()
                    except IOError:
                        self.client.sendall(b'HTTP/1.1 404 Not found\r\n\r\n')
            else:
                self.client.close()
                running = 0

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('httpserver.conf')

    configserver = config['SERVER']
    HOST = configserver['host']
    PORT = int(configserver['port'])

    server = Server(HOST, PORT)
    server.run()
