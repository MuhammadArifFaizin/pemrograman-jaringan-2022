import socket
import select
import sys
from os import path
import os

server_address = ('127.0.0.1', 5001)
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
                data = sock.recv(1024)
                print('sock.getpeername(), data:', sock.getpeername(), data)

                if data:
                    cmd = data.decode("utf-8").split()
                    print('cmd:', cmd)
                    if cmd[0] == "unduh":
                        is_exist = path.exists("dataset/" + cmd[1])
                        is_file = path.isfile("dataset/" + cmd[1])
                        if is_exist and is_file:
                            size = os.path.getsize("dataset/" + cmd[1])
                            header = "file-name: " + cmd[1] + ",\n"
                            header = header + "file-sizes: "+str(size)+",\n\n\n"
                            with open("dataset/" + cmd[1]) as f:
                                lines = f.readlines()
                                lines = "".join(lines)
                                lines = lines + "\n"
                                lines = header + lines
                                sock.send(bytes(lines, 'utf-8'))
                    else:
                        msg = "do you mean \'unduh\'?"
                        sock.send(bytes(msg, 'utf-8'))
                else:                    
                    sock.close()
                    input_socket.remove(sock)

except KeyboardInterrupt:        
    server_socket.close()
    sys.exit(0)