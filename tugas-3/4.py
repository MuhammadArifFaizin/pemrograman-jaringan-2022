import socket

USERNAME = "user1"
PASSWORD = "users"

def execute(commands):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost', 21))

    i = 1
    list_response = ""
    while True:
        try:
            if i > len(commands):            
                msg = str(s.recv(1024).decode())        
                print(msg.strip())
                break

            s.send(commands[i-1].encode('utf-8'))
            msg = str(s.recv(1024).decode())
            print(msg.strip())
            


            
            if "Entering Passive Mode" in msg:
                msg_ip = msg.split('\r\n')[0].strip().split('\r\n')[0]
                p1, p2 = msg_ip.split()[-1].strip('()').split(',')[-2:]
                data_port = int(p1)*256 + int(p2)
                data_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                print("data_port", data_port)
                data_sock.connect(('localhost', data_port))
                data = data_sock.recv(4096)
                print(data)

                file_name = ' '.join(commands[4].strip('\r\n').split()[1:])
                file_path = os.path.join(os.getcwd(), file_name)

            elif "start data transfe" in msg:
                data = data_sock.recv(1024).decode()

                while data:
                    list_data = data.split('\r\n')[:-1]
                    file_list = [' '.join(x.split()[1:]) for x in list_data]
                    print('\n'.join(file_list))
                    data = data_sock.recv(4096).decode('utf-8')

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
            "STOR data.txt" + "\r\n", 
            "QUIT" + "\r\n"]

execute(commands)