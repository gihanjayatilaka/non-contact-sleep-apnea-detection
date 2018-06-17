//Flot Moving Line Chart
var container = $("#flot-line-chart-moving");
var y_min = -2;
var y_max = 2;
var max_size = 1000;

// Determine how many data points to keep based on the placeholder's initial size;
// this gives us a nice high-res plot while avoiding more than one point per pixel.

var maximum = container.outerWidth() / 2 || max_size;
//    var maximum = container.outerWidth() / 2 || 300;

maximum = 1000;

var max_points = 10
var data = [];
var dict = {};
var plot;
var mqtt;
var series;


//


//


function getRandomData() {

    if (data.length) {
        data = data.slice(1);
    }

    while (data.length < maximum) {
        var previous = data.length ? data[data.length - 1] : 50;
        var y = previous + Math.random() * 10 - 5;
        data.push(y < y_min ? 0 : y > y_max ? y_max : y);
    }

    // zip the generated y values with the x values

    var res = [];
    for (var i = 0; i < data.length; ++i) {
        res.push([i, data[i]])
    }

    return res;
}

function initData(){
    var getURL = "../../api/client/client_buffer_data_recv/retrieve"       // Punky
    var jsonURL = getURL + "/" + max_points + "/" + device_id 
//    var jsonDat = {'username' : user, 'device_id' : device_id, 'data_size' : maximum };
//    var jsonDat = {username : user, device_id : device_id, n : maximum };

//    $.getJSON( jsonURL,
//              {username : user, device_id : device_id, n : maximum },
//              function( data ) {
//        var array = JSON.parse(data)
//        for (var i = 0 ; i < array.length; i++){
//            console.log(array[i]);
//            console.log(array[i]["fields"]);
//            var ts = array[i]["fields"]["timestamp"];
//            var val = array[i]["fields"]["data"].split(',');
            
//            dict[ts] = val;
//            console.log(val);
//        }
//    });
}

series = [{
    data: initData(),
    lines: {
        fill: true
    }
}];


function initPlot(){
    plot = $.plot(container, series, {
        grid: {
            borderWidth: 1,
            minBorderMargin: 20,
            labelMargin: 10,
            backgroundColor: {
                colors: ["#fff", "#e4f4f4"]
            },
            margin: {
                top: 8,
                bottom: 20,
                left: 20
            },
            //Alterntive colour for grid
            markings: function(axes) {
                var markings = [];
                var xaxis = axes.xaxis;
                for (var x = Math.floor(xaxis.min); x < xaxis.max; x += xaxis.tickSize * 2) {
                    markings.push({
                        xaxis: {
                            from: x,
                            to: x + xaxis.tickSize
                        },
                        color: "rgba(232, 232, 255, 0.2)"
                    });
                }
                return markings;
            }
        },
        xaxis: {
            tickFormatter: function() {
                return "";
            },
            min:0,
            max:1000
        },
        yaxis: {
            min: y_min,
            max: y_max
        },
        legend: {
            show: true
        }
    });
}

// Update the random dataset at 25FPS for a smoothly-animating chart

/*
setInterval(function updateRandom() {
    series[0].data = getRandomData();
    plot.setData(series);
    plot.draw();
}, 40);
*/


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
    $('#status').val('Connected to ' + host + ':' + port + path);
    // Connection succeeded; subscribe to our topic
    mqtt.subscribe(topic, {qos: 0});
    console.log('Subscribed to topic ' + topic)
    $('#topic').val(topic);
}

function onConnectionLost(response) {
    setTimeout(MQTTconnect, reconnectTimeout);
    $('#status').val("connection lost: " + responseObject.errorMessage + ". Reconnecting");

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
        console.log(obj);
        try{
            plotOnReceive(obj);
        }catch(err){
            console.log(err);            
        }
    }else if (subtopic == "connection"){
        console.log(subtopic);        
    }

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

//    console.log(data)


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
    console.log('plot');

}

MQTTconnect();

$(document).ready(function() {
    initPlot();
});