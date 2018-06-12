import paho.mqtt.client as mqtt
import time
import random
import json
import configparser

'''
Username & pass
TLS
'''

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.publish(connection_topic, 1, retain=True)
    print(userdata)
    topic = userdata
    #client.subscribe(topic)#, qos=1)

def on_publish(client, userdata, mid):
    print(mid)

def on_log(client, userdata, level, buf):
    print("log: ",buf)

def on_disconnect(client, userdata, rc):
    print ("Unexpected MQTT disconnection. Will auto-reconnect")


config = configparser.ConfigParser()
config.read('example.ini')
print(config.sections())  # dictionary of dictionary


#server = "server2.teambitecode.com"
server = "localhost"

#TOPIC
username = config['settings']['username']
device_id = config['settings']['device_id']
passwd = config['settings']['access_token']
print(username, device_id, passwd)

topic = username + "/" + device_id
message_topic = topic + "/data"
connection_topic = topic + "/connection"

#MQTT
user = username+"_"+device_id
# passwd = user

broker_port = 8883
timout_reconnect = 60

#CLIENT
client = mqtt.Client()
#client = mqtt.Client(cli_id, clean_session=False)
# client.user_data_set(topic)
client.will_set(connection_topic,0, qos=1, retain=True) #set will

# Username & password
client.username_pw_set(user, passwd)

# TLS
ca_cert = "ca.crt"
client.tls_set(ca_cert)
client.tls_insecure_set(True)

# Log & Action
client.on_connect = on_connect
client.on_log = on_log
client.on_disconnect = on_disconnect
#client.on_publish = on_publish

try:
    client.connect(server, broker_port, timout_reconnect)
    # client.

    client.loop_start()    #new thread

    # rc = client.loop()
    r = random.randint(0, 120)
    r_min = 0
    r_max = 120
    size = 50

    while (1):

        t = int(time.time())

        data = [0 for i in range(size)]
        for i in range(size):
            r = r + random.randint(0, 11) - 5
            r = r_min if r < r_min else (r_max if r > r_max else r)
            data[i] = r

        # battery = random.randint(0, 100)
        # temp = random.randint(20, 30)

        dict = {"time": t, "data": data}

        message = json.dumps(dict)
        # message = str(t) + " , " + str(r)

        client.publish(message_topic, message, 1, True)
        time.sleep(1)

    client.disconnect()

except:
    print("ERROR")