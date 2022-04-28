import socket

HOST = "localhost"
PORT = 21
STREAM_SIZE = 1024
USERNAME = "user1"
PASSWORD = "users"

def execute(commands):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    i = 1
    response = ""
    while True:
        try:
            if i > len(commands):            
                msg = str(s.recv(STREAM_SIZE)) 
                response += msg.strip()
                # print(msg.strip())
                return response
                break

            msg = str(s.recv(STREAM_SIZE))   
            s.send(commands[i-1].encode("utf-8"))
            response += msg.strip()     
            # print(msg.strip())
            i += 1
                    
        except socket.error:
            s.close()
            break

commands = [
    "USER " + USERNAME + "\r\n", 
    "PASS " + PASSWORD + "\r\n", 
    "HELP\r\n", 
    "AUTH\r\n", 
    "OPTS\r\n",
    "QUIT\r\n"
    ]

message = execute(commands)
# print(message)

ftp_server = message.split("\\r\\n")[0].split("-")[1]
print(ftp_server)