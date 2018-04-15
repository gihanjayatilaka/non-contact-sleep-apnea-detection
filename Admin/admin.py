import paho.mqtt.client as mqtt
from SQL.my_sql import *
import atexit
import sys
from signal import signal, SIGTERM

def exit_handler():
    admin.disconnect()
    mysql.disconnect()
    print("exit")
    #sys.exit()

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    #client.subscribe("#", qos=1)
    client.subscribe("#")

def on_message(client, userdata, msg):
    #print(client)
    #print(userdata)
    #print(msg)
    print(msg.payload.decode(), msg.topic, msg.qos, msg.retain)
    recv = msg.payload.decode()
    mysql.insert("DATA", recv)
    mysql.db.commit()

def on_log(client, userdata, level, buf):
    print("log: ",buf)
    #print(level)


'''SQL'''

mysql = MySQL("localhost", "root", "admin", "test")
mysql.connect()

# This is the Publisher
#server = "server2.teambitecode.com"


server = "localhost"
user = "suren"
passwd = "suren3141"
broker_port = 8883
timout_reconnect = 60
ca_cert = "ca.crt"
topic = "control"

admin = mqtt.Client()
admin.username_pw_set(user, passwd)
admin.tls_set(ca_cert)
admin.tls_insecure_set(True)

admin.on_connect = on_connect
admin.on_message = on_message
admin.on_log = on_log


admin.connect(server, broker_port, timout_reconnect)

#admin.publish("topic/test", "Hello world!")
atexit.register(exit_handler)
#signal.signal(signal.SIGTERM, exit_handler())

admin.loop_forever()

signal(SIGTERM, exit_handler())
