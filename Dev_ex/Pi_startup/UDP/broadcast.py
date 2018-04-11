from socket import *
import threading
import cv2

def sendFile(fName):
    s = socket(AF_INET, SOCK_DGRAM)
    s.sendto(fName, addr)
    f = open(fName, "rb")
    data = f.read(buf)
    while data:
        if (s.sendto(data, addr)):
            data = f.read(buf)
    f.close()
    s.close()


def captureFunc():
    count = 0
    while (cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            cv2.imshow('frame', frame)
            count = count + 1
            if count == ratio:
                cv2.imwrite("img.jpg", frame)
                sendFile("img.jpg")
                count = 0
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break


status = 0
message = "DISCOVER_BC_SERVER_REQUEST"
reply = "DISCOVER_BC_SERVER_RESPONSE"
UDP_server = ('255.255.255.255', 8888)

sock = socket(AF_INET, SOCK_DGRAM)
sock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
sock.settimeout(1)

while(1):
    sock.sendto(message, UDP_server)
    print "sent message:", message
    try:
        data, addr = sock.recvfrom(15000)  # buffer size is 15000 bytes
        print "received message:", data
        if data == reply:
            print(addr)
            status = 1
            sock.close()
            break
    except:
        pass

cap = cv2.VideoCapture(0)

FPS = cap.get(5)
setFPS = 10
ratio = int(FPS) / setFPS

host = "255.255.255.255"
port = 3141
addr = (host, port)
buf = 1024



