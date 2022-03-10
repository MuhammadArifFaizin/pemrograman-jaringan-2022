import socketserver
import sys
import os

HOST, PORT = "localhost", 5001
SERVER_FILE_PATH = "dataset/"

def convert_to_bytes(no):
    result = bytearray()
    result.append(no & 255)
    for i in range(3):
        no = no >> 8
        result.append(no & 255)
    return result

def check_file(paths):
    is_exist = os.path.exists(SERVER_FILE_PATH + paths)
    is_file = os.path.isfile(SERVER_FILE_PATH + paths)

    return is_exist and is_file

class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        try:
            while True:
                self.data = self.request.recv(1024).strip()
                filename = self.data.decode("utf-8")
                print('file:', filename)
                chk_file = check_file(filename)
                if chk_file:
                    with open(SERVER_FILE_PATH + filename, "rb") as file:
                        self.data = file.read()
                    self.send_stream()
        except KeyboardInterrupt:
            server.shutdown()

    def send_stream(self):
        length = len(self.data)
        self.request.send(convert_to_bytes(length))
        
        byte = 0

        while byte < length:
            self.request.send(self.data[byte:byte+1024])
            byte += 1024

try:
    while True:
        server_address = (HOST, PORT)
        server = socketserver.TCPServer(server_address, MyTCPHandler)
        server.serve_forever()
            
except KeyboardInterrupt:
    server.shutdown()
    sys.exit(0)