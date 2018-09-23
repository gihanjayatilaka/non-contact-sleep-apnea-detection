import paho.mqtt.client as mqtt
import time
import random

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    print(userdata)
    topic = userdata
    #client.subscribe(topic)#, qos=1)

def on_publish(client, userdata, mid):
    print(mid)

def on_log(client, userdata, level, buf):
    print("log: ",buf)



#server = "server2.teambitecode.com"
server = "localhost"
user = "user1"
passwd = "user1"
message = "Hello world!"
broker_port = 8883
timout_reconnect = 60
cli_id = "0"
ca_cert = "ca.crt"

topic = "topic/" + str(user)
#topic = "topic/" + str(user) + "/" + str(cli_id)

client = mqtt.Client()
#client = mqtt.Client(cli_id, clean_session=False)
client.user_data_set(topic)

#client.username_pw_set(user, passwd)
#client.tls_set(ca_cert)
#client.tls_insecure_set(True)

client.on_connect = on_connect
#client.on_publish = on_publish
client.on_log = on_log

client.connect(server, broker_port, timout_reconnect)

#client.loop_start()    #new thread
#client.loop_forever()  #blocking

rc = client.loop()
while rc == 0:
    t = time.time()
    r = random.randint(0, 1000000)
    message = str(t) + " , " + str(r)
    client.publish(topic,message, 1, True)
    time.sleep(1)
    rc = client.loop()

client.disconnect()