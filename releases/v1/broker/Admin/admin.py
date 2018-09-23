import paho.mqtt.client as mqtt
import time
import requests
import json
from requests.auth import HTTPBasicAuth
import subprocess
import MySQLdb
import datetime

def np(pw):
    proc = subprocess.Popen(["./np","-p",str(pw)],stdout=subprocess.PIPE)
    token = ""
    for line in iter(proc.stdout.readline,''):
        token = line.rstrip()
    return token
    '''
    # call(["./np", "-p", "suren"])

    proc = subprocess.Popen(["./np","-p","suren"],stdout=subprocess.PIPE)

    for line in iter(proc.stdout.readline,''):
       print (line.rstrip())
    '''

def add_user(uname, pw):
    pw = np(pw)
    command = "INSERT INTO users (username, pw) VALUES ('" + uname + "' ,'" + pw + "');"
    cur.execute(command)
    db.commit()

def remove_user(uname):
    command = "REMOVE FROM users WHERE username = '" + uname + "';"
    cur.execute(command)
    db.commit()

def add_acl(uname, topic, rw):
    command = "INSERT INTO acls (username, topic, rw) VALUES ('" + uname + "', '" + topic + "', " + str(rw) + " );"
    cur.execute(command)
    db.commit()

def remove_acl(uname):
    command = "REMOVE FROM acls WHERE username = '" + uname + "';"
    cur.execute(command)
    db.commit()

def reg_device(uname, dev, token):
    username = uname + "_" + dev
    topic = uname + "/" + dev + "/#"
    try:
        add_user(username, token)
        add_acl(username, topic, 2)
    except:
        pass

def remove_device(uname, dev):
    username = uname + "_" + dev
    remove_acl(username)
    remove_user(username)

def login(user, pw):
    pw = hash(pw)
    # ADD TO DJANGO DB @punky
    topic = user + "/#"
    try:
        add_user(user, pw)
        add_acl(user, topic, 1)
    except:
        pass

def create_user():
    try:
        cur.execute("CREATE TABLE users ( id INTEGER AUTO_INCREMENT, username VARCHAR(25) NOT NULL, pw VARCHAR(128) NOT NULL, super INT(1) NOT NULL DEFAULT 0, PRIMARY KEY (id));")
        cur.execute("CREATE UNIQUE INDEX users_username ON users (username);")
    except:
        pass

def create_acl():
    try:
        cur.execute("CREATE TABLE acls (id INTEGER AUTO_INCREMENT, username VARCHAR(25) NOT NULL, topic VARCHAR(256) NOT NULL, rw INTEGER(1) NOT NULL DEFAULT 1, PRIMARY KEY (id));")
        cur.execute("CREATE UNIQUE INDEX acls_user_topic ON acls (username, topic(228));")
    except:
        pass


get_time = lambda : time.asctime(time.localtime(time.time()))
current_milli_time = lambda: int(round(time.time()))

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    for topic in topics:
        client.subscribe(topic, qos=1)
        print("Subscribed to topic " + str(topic))



def on_message(client, userdata, msg):
    # print(msg.payload.decode(), msg.topic, msg.qos, msg.retain)
    # print(get_time())
    topic = msg.topic
    data = msg.payload.decode()
    jdata = {}
    try:
        uname, dev, subtopic = topic.strip().split("/")
        data = json.loads(data)
        print(data['data'])
        # print(data["data"])
        print("JDATA")

        print(subtopic)

        if subtopic == "data":
            print(subtopic)
            jdata['device_id'] = dev
            jdata['timestamp'] = str(datetime.datetime.now())
            jdata['data']  = ",".join(str(i) for i in data["data"])

    except:
        if topic == "register":
            data = json.loads(data)
            print(data)

            uname = data["user"]
            token = data["token"]
            dev = data['dev_id']

            reg_device(uname, dev, token)


            pass

        pass

def on_log(client, userdata, level, buf):
    print("log: ",buf)
    #print(level)


db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                     user="root",         # your username
                     passwd="admin",    # your password
                     db="test")        # name of the data base

cur = db.cursor()

create_user()
create_acl()


#server = "server2.teambitecode.com"
server = "localhost"
URL = ""

#TOPIC
# topic = "$SYS/#"
topics = [
    # "$SYS/broker/log/#",
    "#",
    "connection/#"]

#MQTT
user = "admin"
passwd = user

broker_port = 8883
timout_reconnect = 60

#CLIENT
client = mqtt.Client()
#client = mqtt.Client(cli_id, clean_session=False)
client.user_data_set(topics)

# Username & password
client.username_pw_set(user, passwd)

# TLS
ca_cert = "ca.crt"
client.tls_set(ca_cert)
client.tls_insecure_set(True)

client.on_connect = on_connect
client.on_message = on_message
#client.on_log = on_log

client.connect(server, broker_port, timout_reconnect)

# client.loop_forever()
client.loop_start()

while(1):
    pass

