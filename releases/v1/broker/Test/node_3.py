import paho.mqtt.client as mqtt
import time
import random
import json

'''
Username & pass
TLS
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

#TOPIC
username = "suren"
device_id = "dev1"
topic = username + "/" + device_id

#MQTT
user = username+"_"+device_id
passwd = user

broker_port = 8883
timout_reconnect = 60

#CLIENT
client = mqtt.Client()
#client = mqtt.Client(cli_id, clean_session=False)
client.user_data_set(topic)

# Username & password
client.username_pw_set(user, passwd)

# TLS
ca_cert = "ca.crt"
client.tls_set(ca_cert)
client.tls_insecure_set(True)

# Log & Action
client.on_connect = on_connect
client.on_log = on_log
#client.on_publish = on_publish

client.connect(server, broker_port, timout_reconnect)

#client.loop_start()    #new thread
#client.loop_forever()  #blocking

rc = client.loop()
r = random.randint(0, 120)
r_min = 0
r_max = 120

while rc == 0:

    t = time.time()

    data = [0 for i in range(100)]
    for i in range(100):
        r = r + random.randint(0, 11) - 5
        r = r_min if r < r_min else (r_max if r > r_max else r)
        data[i] = r

    # battery = random.randint(0, 100)
    # temp = random.randint(20, 30)

    dict = {"time": t, "data": data}

    message = json.dumps(dict)
    # message = str(t) + " , " + str(r)

    client.publish(topic, message, 1, True)
    time.sleep(.1)

    rc = client.loop()

client.disconnect()