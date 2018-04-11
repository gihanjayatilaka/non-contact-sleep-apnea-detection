import socket

#UDP_IP = "127.0.0.1"
UDP_IP = "255.255.255.255"
UDP_PORT = 5005
MESSAGE = "Hello, World!"

print "UDP target IP:", UDP_IP
print "UDP target port:", UDP_PORT
print "message:", MESSAGE

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP

while(1):
    sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))