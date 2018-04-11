import time
from socket import *
import threading

def send(sock):
    while(1):
        sock.sendto(message, UDP_server)
        print "sent message:", message
        time.sleep(1)


message = "DISCOVER_BC_SERVER_REQUEST"
reply = "DISCOVER_BC_SERVER_RESPONSE"
UDP_server = ('255.255.255.255', 8888)
UDP_recvr = ('0.0.0.0', 3141)

sock = socket(AF_INET, SOCK_DGRAM)
sock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
sock.settimeout(1)


#cs.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

#sock = socket(AF_INET, SOCK_DGRAM)
#sock.bind(UDP_recvr)

#send_thread = threading.Thread(name="detect_face", target=send, kwargs={'sock':cs})
#send_thread.start()

#sent = cs.sendto(message, UDP_server)
#print(sent)
while(1):
    sock.sendto(message, UDP_server)
    print "sent message:", message
    try:
        data, addr = sock.recvfrom(15000)  # buffer size is 15000 bytes
        print "received message:", data
        if data == reply:
            break
    except:
        pass


'''
cs.connect(('<broadcast>', 5455))


while 1:
    cmd = int(raw_input('send: '))
    if (cmd == 1):
        cs.send('1')
    time.sleep(1)
'''