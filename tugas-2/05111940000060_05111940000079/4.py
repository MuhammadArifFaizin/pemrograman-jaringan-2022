import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
url = 'classroom.its.ac.id'
# url = 'www.google.com'

server_address = (url, 80)
client_socket.connect(server_address)

request_header = 'GET / HTTP/1.0\r\nHost: ' + url + '\r\n\r\n'
client_socket.send(request_header.encode())

response = ''

while True:
    received = client_socket.recv(1024)
    if not received:
        break
    response += received.decode('utf-8')
#     break;
    
print('Charset of', url, ':', response.split('\n')[3].split(' ')[2].split('\r')[0])
client_socket.close()