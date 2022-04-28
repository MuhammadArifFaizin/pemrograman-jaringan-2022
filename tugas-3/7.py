import socket

HOST = "localhost"
PORT = 21
STREAM_SIZE = 1024
USERNAME = "user1"
PASSWORD = "users"
FOLDER_NAME_1 = "test"
FOLDER_NAME_2 = "test2"

def execute(commands):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    i = 1
    while True:
        try:
            if i > len(commands):            
                msg = str(s.recv(1024).decode("utf-8")) 
                print(msg.strip())
                break

            msg = str(s.recv(1024).decode("utf-8"))
            s.send(commands[i-1].encode("utf-8"))
            print(msg.strip())
            i += 1
                    
        except socket.error:
            s.close()
            break

commands = [
    "USER " + USERNAME + "\r\n", 
    "PASS " + PASSWORD + "\r\n", 
    "RNFR " + FOLDER_NAME_1 + "\r\n", 
    "RNTO " + FOLDER_NAME_2 + "\r\n", 
    "QUIT\r\n"
    ]

execute(commands)
