#author: harshana.w@eng.pdn.ac.lk
import socket
import sys
import pigpio
import time
from thread import *

pi = pigpio.pi()
#initializing hw pwm pins
pin_gpio_z = 12
pin_gpio_x = 13
pi.hardware_PWM(pin_gpio_z, 0, 0)
pi.hardware_PWM(pin_gpio_x, 0, 0)
time.sleep(0.1)

HOST = '0.0.0.0'
PORT = 8989

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')

try:
    s.bind((HOST, PORT))
except socket.error , msg:
    print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
    sys.exit()

print('Socket bind complete')

s.listen(10)
print('Socket now listening')

def clientthread(conn):
    #Sending message to connected client
    conn.send('Welcome to the server. Receving Data...\n') 
    z,x=75000,75000
    #infinite loop so that function do not terminate and thread do not end.
    while True:

        #Receiving from client
        data = conn.recv(1024)
        if not data:
            break
        dz,dx,h,w = map(int,data.split())
        z -= int(10000*(1.0*dz/w))
        x -= int(10000*(1.0*dx/h))
        z = max(z,29000)
        z = min(z,115000)
        x = max(x,50000)
        x = min(x,90000)
        print("dz", dz, "dx", dx, "z", z,"x",x)

        pi.hardware_PWM(pin_gpio_z, 50, z) #50Hz
        pi.hardware_PWM(pin_gpio_x, 50, x) #50Hz
        time.sleep(1)

    conn.close()

#now keep talking with the client
while 1:
    #wait to accept a connection
    conn, addr = s.accept()
    print('Connected with ' + addr[0] + ':' + str(addr[1]))

    #start new thread
    start_new_thread(clientthread ,(conn,))

s.close()
