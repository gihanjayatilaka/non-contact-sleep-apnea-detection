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
	mysql > source /home/user/mosquitto-auth-plug/examples/mysql.sql<br>

Generate Key Pair and Certificate:<br>
	openssl genrsa -out server.key 2048	# Generate key pair<br>
	openssl req -out server.csr -key server.key -new	# Generate certificate signing request<br>
<br>
Self sign certificate (by generating CA certificate):<br>
	openssl genrsa -des3 -out ca.key 2048	# Generate CA key pair<br>
	openssl req -new -x509 -days 1826 -key ca.key -out ca.crt	# Generate CA certificate<br>
	openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out server.crt -days 360	# Sign certificate signing request using self made CA cert<br>
