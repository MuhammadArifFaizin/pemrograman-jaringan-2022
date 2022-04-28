import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 21))

commands = ['USER user1\r\n', 'PASS users\r\n', 'HELP\r\n', 'AUTH\r\n', 'OPTS\r\n','QUIT\r\n']

def execute(commands):
    i = 1
    response = ""
    while True:
        try:
            if i > len(commands):            
                msg = str(s.recv(1024)) 
                response += msg.strip()
                # print(msg.strip())
                return response
                break

            s.send(commands[i-1].encode('utf-8'))
            msg = str(s.recv(1024))   
            response += msg.strip()     
            # print(msg.strip())
            i += 1
                    
        except socket.error:
            s.close()
            break

message = execute(commands).split("\\r\\n")[0].split("\'")[1].split("-")[1]
# .split("(")[1].split(")")[0].split(",")[4:6]
# message = tuple(message)
print(message)