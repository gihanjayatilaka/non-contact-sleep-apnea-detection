var dict = {};

var mqtt;
var reconnectTimeout = 2000;
//    var host = "127.0.0.1";
//    var port = 9001;
//    var topic = "#"

function MQTTconnect() {
    if (typeof path == "undefined") {
        path = '/mqtt';
    }
//        path = "";    //  What is this ????

    mqtt = new Paho.MQTT.Client(
        host,
        port,
        path,
        "web_" + parseInt(Math.random() * 100, 10)
    );

    var options = {
        timeout: 3,
        useSSL: useTLS,
//            cert: CERT,
//            rejectUnauthorized: false,
        cleanSession: cleansession,
        onSuccess: onConnect,
        onFailure: function (message) {
            $('#status').val("Connection failed: " + message.errorMessage + "Retrying");
            setTimeout(MQTTconnect, reconnectTimeout);
        }
    };

    mqtt.onConnectionLost = onConnectionLost;
    mqtt.onMessageArrived = onMessageArrived;

    if (username != null) {
        options.userName = username;
        options.password = password;
    }
    console.log("Host="+ host + ", port=" + port + ", path=" + path + " TLS = " + useTLS + " username=" + username + " password=" + password);
    mqtt.connect(options);
}

function onConnect() {
//    $('#status').val('Connected to ' + host + ':' + port + path);
    // Connection succeeded; subscribe to our topic
    mqtt.subscribe(topic, {qos: 0});
    console.log('Subscribed to topic ' + topic)
//    $('#topic').val(topic);
};

function onConnectionLost(response) {
    setTimeout(MQTTconnect, reconnectTimeout);
//    $('#status').val("connection lost: " + responseObject.errorMessage + ". Reconnecting");

};

function onMessageArrived(message) {

    var topic = message.destinationName;
    var payload = message.payloadString;

    var val = parseInt(payload.split(',')[1]);
    var obj = JSON.parse(payload);

    val = obj.data;
    var tim = obj.time;
    
    var tab = $('table');
    console.log(tab.row(0));
    
    console.log(val);

//        console.log(obj)
    if(val){        
        console.log(1);
    }else{
        console.log(0);
    }

};
//$(document).ready(function() {
MQTTconnect();
//});

