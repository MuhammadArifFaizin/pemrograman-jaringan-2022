import os
import socket
import sys

server_address = ('127.0.0.1', 5001)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(server_address)

# sys.stdout.write('>> ')

try:
    while True:
        message = sys.stdin.readline()
        client_socket.send(bytes(message, 'utf-8'))
        received_data = client_socket.recv(1024).decode('utf-8')
        
        sys.stdout.write('-=-=- output -=-=-\n')
        sys.stdout.write(received_data)
    
        if not os.path.exists(os.path.join(os.getcwd(), "Download")):
            os.mkdir("Download")

        filename = received_data.splitlines()[0].split()[1]

        with open(os.path.join(os.getcwd(), "Download", filename), "w+") as f:
            content_file = received_data.splitlines()[4:]
            
            for line in content_file:
                f.write(line + '\n')
        
        # while received_data:
        #     received_data = client_socket.recv(1024).decode('utf-8')
        #     sys.stdout.write(received_data)
        #     sys.stdout.write('>> ')
            

except KeyboardInterrupt:
    client_socket.close()
    sys.exit(0)