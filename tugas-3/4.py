import socket
import os

HOST = "localhost"
PORT = 21
STREAM_SIZE = 1024
USERNAME = "user1"
PASSWORD = "users"
FILENAME = "test.txt"

def execute(commands):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    i = 1
    while True:
        try:
            if i > len(commands):            
                msg = str(s.recv(STREAM_SIZE).decode())        
                print(msg.strip())
                break

            s.send(commands[i-1].encode('utf-8'))
            msg = str(s.recv(STREAM_SIZE).decode())
            print(msg.strip())
            
            if "Entering Passive Mode" in msg:
                msg_ip = msg.split('\r\n')[0].strip().split('\r\n')[0]
                p1, p2 = msg_ip.split()[-1].strip('()').split(',')[-2:]
                data_port = int(p1)*256 + int(p2)
                data_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                # print("data_port", data_port)
                data_sock.connect(('localhost', data_port))

                file_name = ' '.join(commands[4].strip('\r\n').split()[1:])
                file_path = os.path.join(os.getcwd(), file_name)
                # print(file_path)

                with open(file_path, 'rb') as file:
                    while True:
                        bytes_read = file.read(4096)
                        if not bytes_read:
                            break
                        data_sock.sendall(bytes_read)
                    file.close()
                data_sock.close()
                msg = str(s.recv(STREAM_SIZE).decode('utf-8'))
                print(msg.strip())

            i += 1
                    
        except socket.error:
            print("SOCKET ERROR")
            s.close()
            break

        except AttributeError:
            print("ATTRIBUTE ERROR")
            s.close()
            break

commands = ["USER " + USERNAME + "\r\n", 
            "PASS " + PASSWORD + "\r\n", 
            "TYPE A" + "\r\n",
            "PASV" + "\r\n",
            "STOR " + FILENAME + "\r\n", 
            "QUIT" + "\r\n"]

execute(commands)