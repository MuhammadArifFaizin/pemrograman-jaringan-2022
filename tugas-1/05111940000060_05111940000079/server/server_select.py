import socket
import select
import sys
from os import path

HOST, PORT = "127.0.0.1", 5001

server_address = (HOST, PORT)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(server_address)
server_socket.listen(5)

input_socket = [server_socket]

def convert_to_bytes(no):
    result = bytearray()
    result.append(no & 255)
    for i in range(3):
        no = no >> 8
        result.append(no & 255)
    return result

SERVER_FILE_PATH = "dataset/"

def check_file(paths):
    is_exist = path.exists(SERVER_FILE_PATH + paths)
    is_file = path.isfile(SERVER_FILE_PATH + paths)

    return is_exist and is_file

def send(sock, data):
    length = len(data)
    sock.send(convert_to_bytes(length))
    byte = 0

    while byte < length:
        sock.send(data[byte:byte+1024])
        byte += 1024

try:
    while True:
        read_ready, write_ready, exception = select.select(input_socket, [], [])
        
        for sock in read_ready:
            if sock == server_socket:
                client_socket, client_address = server_socket.accept()
                input_socket.append(client_socket)        
            
            else:            	
                data = sock.recv(1024)
                print('sock.getpeername(), data:', sock.getpeername(), data)

                if data:
                    file = data.decode("utf-8")
                    print('file:', file)
                    chk_file = check_file(file)
                    if chk_file:
                        with open(SERVER_FILE_PATH + file, "rb") as file:
                            data = file.read()
                        send(sock, data)
                else:                    
                    sock.close()
                    input_socket.remove(sock)

except KeyboardInterrupt:        
    server_socket.close()
    sys.exit(0)