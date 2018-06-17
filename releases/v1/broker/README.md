To install mosquitto : <br>
	sudo apt-get install mosquitto

To get mosquitto-auth-plugin:
	git clone https://github.com/jpmens/mosquitto-auth-plug
	cp mosquitto-auth-plug/config.mk.in mosquitto-auth-plug/config.mk

To create tables:
	sudo service mysql start
	mysql -u root

In mysql:
	mysql > source /home/user/mosquitto-auth-plug/examples/mysql.sql

