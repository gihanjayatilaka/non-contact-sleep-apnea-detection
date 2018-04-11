import socket

#host = socket.gethostname()
#print(host)

host = '0.0.0.0'
port = 8089

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind((host, port))
serversocket.listen(5) # become a server socket, maximum 5 connections

while True:
    connection, address = serversocket.accept()
    buf = connection.recv(64)
    if len(buf) > 0:
        print (buf)
        break

