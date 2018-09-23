import paho.mqtt.client as mqtt
import time
import random

'''
Basic node
No username/pass
No tls
'''
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
r = random.randint(0, 120)
r_min = 0
r_max = 120

while rc == 0:
    t = time.time()
    r = r + random.randint(0, 11) - 5
    r = r_min if r < r_min else (r_max if r > r_max else r)
    message = str(t) + " , " + str(r)
    client.publish(topic,message, 1, True)
    time.sleep(.1)
    rc = client.loop()

client.disconnect()