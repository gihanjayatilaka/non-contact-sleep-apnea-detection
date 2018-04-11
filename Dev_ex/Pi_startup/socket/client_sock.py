import socket

host = 'localhost'
port = 8089

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect((host, port))
clientsocket.send('hello'.encode('utf8'))