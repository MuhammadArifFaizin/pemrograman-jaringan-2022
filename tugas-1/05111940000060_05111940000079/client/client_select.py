import os
import socket
import sys

HOST, PORT = "127.0.0.1", 5001

server_address = (HOST, PORT)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(server_address)

# sys.stdout.write('>> ')

CLIENT_FILE_PATH = "Download"

def convert_to_bytes(no):
    result = bytearray()
    result.append(no & 255)
    for i in range(3):
        no = no >> 8
        result.append(no & 255)
    return result

def bytes_to_number(b):
    res = 0
    for i in range(4):
        res += b[i] << (i*8)
    return res

def receive(sock):
    size = bytes_to_number(sock.recv(4))
    curr_size = 0
    buff = b""

    while curr_size < size:
        data = sock.recv(1024)
        if not data:
            break
        if(len(data) + curr_size > size):
            data = data[:size-curr_size]
        buff += data

        curr_size += len(data)
    
    return buff

try:
    while True:
        message = sys.stdin.readline()
        cmd = message.split()[0]
        filename = message.split()[1]

        if (cmd != 'unduh'):
            break

        client_socket.send(filename.encode())
        
        # sys.stdout.write('-=-=- output -=-=-\n')
        if not os.path.exists(os.path.join(os.getcwd(), CLIENT_FILE_PATH)):
            os.mkdir(CLIENT_FILE_PATH)

        buffer = receive(client_socket)

        with open(os.path.join(os.getcwd(), CLIENT_FILE_PATH, filename), "wb") as f:
            f.write(buffer)
        
        sys.stdout.write('file_name : ' + filename + ',\n')
        sys.stdout.write('file_size : ' + str(os.path.getsize(os.path.join(os.getcwd(), CLIENT_FILE_PATH, filename))) + ',\n\n\n')

except KeyboardInterrupt:
    client_socket.close()
    sys.exit(0)