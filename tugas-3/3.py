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
    while True:
        try:
            if i > len(commands):            
                msg = str(s.recv(STREAM_SIZE).decode())        
                # print(msg.strip())
                break

            msg = str(s.recv(STREAM_SIZE).decode())
            s.send(commands[i-1].encode('utf-8'))
            # print(msg.strip())
            
            if "Entering Passive Mode" in msg:
                msg_ip = msg.split('\r\n')[0].strip().split('\r\n')[0]
                p1, p2 = msg_ip.split()[-1].strip('()').split(',')[-2:]
                DATA_PORT = int(p1)*256 + int(p2)

                data_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                data_sock.connect((HOST, DATA_PORT))
            elif "start data transfer" in msg:
                data = data_sock.recv(STREAM_SIZE).decode('utf-8')
                # print(data)

                while data:
                    list_data = data.split('\r\n')[:-1]
                    file_list = [' '.join(x.split()[1:]) for x in list_data]
                    print('\n'.join(file_list))
                    data = data_sock.recv(STREAM_SIZE).decode('utf-8')

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
            "TYPE I" + "\r\n",
            "PASV" + "\r\n",
            "MLSD" + "\r\n", 
            "QUIT" + "\r\n"]

execute(commands)