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
            console.log("Connection failed: " + message.errorMessage + "Retrying");
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
    $('#status').val('Connected to ' + host + ':' + port + path);
    // Connection succeeded; subscribe to our topic
    mqtt.subscribe(topic, {qos: 0});
    console.log('Subscribed to topic ' + topic)
    $('#topic').val(topic);
}

function onConnectionLost(response) {
    setTimeout(MQTTconnect, reconnectTimeout);
    $('#status').val("connection lost: " + response.errorMessage + ". Reconnecting");
    console.log(response.errorMessage);
};

function onMessageArrived(message) {

    var topic = message.destinationName;
    var payload = message.payloadString;
    
    console.log(topic);
    console.log(payload)
    
    var subtopic = topic.split('/')[2];
    
    if (subtopic == "data"){
        console.log("data");
        var obj = JSON.parse(payload);
//        plotOnReceive(obj);
    }else if (subtopic == "connection"){
        
    }

//    var val = parseInt(payload.split(',')[1]);
//    var obj = JSON.parse(payload);

//        console.log(obj)
//    try {       // DATA
//        var val = obj.data;
//        plotOnReceive(obj);
//    } catch(err) {      //CONNECTION
////            document.getElementById("demo").innerHTML = err.message;
//    }


    //$('#ws').prepend('<li>' + topic + ' = ' + payload + '</li>');
};

function plotOnReceive(obj){

    var tim = obj.time;
    var val = obj.data;

    dict[tim] = val;

//        console.log(dict)

//        var keys = Object.keys(dict); // or loop over the object to get the array. keys will be in any order
//        keys.sort(); // maybe use custom sort, to change direction use .reverse(). keys now will be in wanted order

//        var min = Math.min(keys)
//        console.log(min)

    data = data.concat(val)

    if (data.length > maximum){
        data = data.slice(data.length-maximum)
    }

//        data.concat()

//        console.log(max_key)

//        var start = keys.length - max_size;
//        start = start > 0 ? start : 0;
//        var data = dict[start];


//        for (var i=start+1; i<keys.length; i++) { // now lets iterate in sort order
//            var key = keys[i];
//            var value = dict[key];
//            console.log(value)
//            data.concat(value)
//            console.log(data)
//            
//            /* do something with key & value here */
//        }

    console.log(data)


//        if (keys.length > max_size){
//            for (var i = 0; i < keys.length-max_size; i ++){
//                delete data[keys[i]]
//            }
//        }

//        console.log(data)

//        if (data.length) {
//            data = data.slice(1);
//        }
//        
//        data.push(val);
//
//        // zip the generated y values with the x values
//
    var res = [];
    for (var i = 0; i < data.length; ++i) {
        res.push([i, data[i]])
    }

    series[0].data = res;

    plot.setData(series);
    plot.draw();

}

//$(document).ready(function() {
MQTTconnect();
//});

