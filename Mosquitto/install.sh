sudo apt-get install mosquitto

sudo apt-get install mysql-server

git clone https://github.com/jpmens/mosquitto-auth-plug
cp mosquitto-auth-plug/config.mk.in mosquitto-auth-plug/config.mk

pip install paho-mqtt
pip install pycryptodome
pip install pyDH
