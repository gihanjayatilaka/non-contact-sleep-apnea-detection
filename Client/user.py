import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(topic, qos=1)

def on_message(client, userdata, msg):
    #print(client)
    #print(userdata)
    #print(msg)
    print(msg.payload.decode(), msg.topic, msg.qos, msg.retain)
    #topics = msg.topic

def on_log(client, userdata, level, buf):
    print("log: ",buf)
    #print(level)

# This is the Publisher
#server = "server2.teambitecode.com"

server = "localhost"
user = "user1"
passwd = "user1"
broker_port = 8883
timout_reconnect = 60
ca_cert = "ca.crt"
topic = "topic/" + user

client = mqtt.Client()
client.username_pw_set(user, passwd)
client.tls_set(ca_cert)
client.tls_insecure_set(True)

client.on_connect = on_connect
client.on_message = on_message
client.on_log = on_log


client.connect(server, broker_port, timout_reconnect)

#client.publish("topic/test", "Hello world!")

client.loop_forever()