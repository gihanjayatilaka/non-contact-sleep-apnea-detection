To install mosquitto :<br>
	sudo apt-get install mosquitto<br>
<br>
To get mosquitto-auth-plugin:<br>
	git clone https://github.com/jpmens/mosquitto-auth-plug<br>
	cp mosquitto-auth-plug/config.mk.in mosquitto-auth-plug/config.mk<br>
<br>
To create tables:<br>
	sudo service mysql start<br>
	mysql -u root<br>
<br>
In mysql:<br>
	mysql > source /home/user/mosquitto-auth-plug/examples/mysql.sql<br>

