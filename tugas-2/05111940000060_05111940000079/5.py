# get short tutorial here: http://www.pythonforbeginners.com/python-on-the-web/beautifulsoup-4-python/
import socket
import ssl
from bs4 import BeautifulSoup

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('classroom.its.ac.id', 443)
client_socket.connect(server_address)
client_socket = ssl.wrap_socket(client_socket, ssl_version=ssl.PROTOCOL_SSLv23)

request_header = b'GET https://classroom.its.ac.id/ HTTP/1.0\r\nHost: classroom.its.ac.id\r\n\r\n'
client_socket.send(request_header)

response = ''
while True:
    received = client_socket.recv(1024)
    if not received:
        break
    response += received.decode('utf-8')

responses = response.rsplit('\r\n',1)

soup = BeautifulSoup(response, 'html.parser')
print(soup.find("ul").get_text())