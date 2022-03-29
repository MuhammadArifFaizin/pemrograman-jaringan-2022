import os
import socket
import select
import sys

server_address = ('127.0.0.1', 80)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(server_address)
server_socket.listen(5)

input_socket = [server_socket]

try:
    while True:
        read_ready, write_ready, exception = select.select(input_socket, [], [])
        
        for sock in read_ready:
            if sock == server_socket:
                client_socket, client_address = server_socket.accept()
                input_socket.append(client_socket)                       
            
            else:                
                # receive data from client, break when null received          
                data = sock.recv(4096)
                if data:
                
                    data = data.decode('utf-8')
                    request_header = data.split('\r\n')
                    request_file = request_header[0].split(" ")[1].split("/")[-2]
                    request_file += "/"
                    print("request_file_split : " + request_file)
                    response_header = b''
                    response_data = b''
                    
                    if request_file == 'index.html' or request_file == '/' or request_file == '/index.html' or request_file == 'dataset/':
                        try:
                            if request_file == '/':
                                f = open('index.html', 'r')
                            else:
                                f = open(request_file + 'index.html', 'r')
                            response_data = f.read()
                            f.close()
                            
                            content_length = len(response_data)
                            response_header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=UTF-8\r\nContent-Length:' \
                                            + str(content_length) + '\r\n\r\n'
                        except IOError:
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
                            for root, dirs, files in os.walk(".", topdown=False):
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

                        sock.sendall(response_header.encode('utf-8') + response_data.encode('utf-8'))

                    else:
                        try:
                            print(request_file)
                            f = open('404.html', 'r')
                            response_data = f.read()
                            f.close()
                            
                            response_header = 'HTTP/1.1 404 Not Found\r\n\r\n'

                            sock.sendall(response_header.encode('utf-8') + response_data.encode('utf-8'))
                        except IOError:
                            sock.sendall(b'HTTP/1.1 404 Not found\r\n\r\n')
                else:
                    sock.close()
                    input_socket.remove(sock)
                    
except KeyboardInterrupt:        
    server_socket.close()
    sys.exit(0)
