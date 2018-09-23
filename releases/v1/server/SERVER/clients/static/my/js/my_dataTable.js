//var dict = {};
//
//var mqtt;
//var reconnectTimeout = 2000;
//var table;
//
////    var host = "127.0.0.1";
////    var port = 9001;
////    var topic = "#"
//
//function MQTTconnect() {
//    if (typeof path == "undefined") {
//        path = '/mqtt';
//    }
////        path = "";    //  What is this ????
//
//    mqtt = new Paho.MQTT.Client(
//        host,
//        port,
//        path,
//        "web_" + parseInt(Math.random() * 100, 10)
//    );
//
//    var options = {
//        timeout: 3,
//        useSSL: useTLS,
////            cert: CERT,
////            rejectUnauthorized: false,
//        cleanSession: cleansession,
//        onSuccess: onConnect,
//        onFailure: function (message) {
////            $('#status').val("Connection failed: " + message.errorMessage + "Retrying");
//            setTimeout(MQTTconnect, reconnectTimeout);
//        }
//    };
//
//    mqtt.onConnectionLost = onConnectionLost;
//    mqtt.onMessageArrived = onMessageArrived;
//
//    if (username != null) {
//        options.userName = username;
//        options.password = password;
//    }
//    console.log("Host="+ host + ", port=" + port + ", path=" + path + " TLS = " + useTLS + " username=" + username + " password=" + password);
//    mqtt.connect(options);
//}
//
//function onConnect() {
////    $('#status').val('Connected to ' + host + ':' + port + path);
//    // Connection succeeded; subscribe to our topic
//    mqtt.subscribe(topic, {qos: 0});
//    console.log('Subscribed to topic ' + topic)
////    $('#topic').val(topic);
//}
//
//function onConnectionLost(response) {
//    setTimeout(MQTTconnect, reconnectTimeout);
////    $('#status').val("connection lost: " + responseObject.errorMessage + ". Reconnecting");
//
//};
//
//function onMessageArrived(message) {
//
//    var topic = message.destinationName;
//    var payload = message.payloadString;
//    
//    console.log(topic);
//    console.log(payload)
//    
//    var subtopic = topic.split('/')[2];
//    var devices = topic.split('/')[1];
//    
//    if (subtopic == "data"){
////        console.log("data");
////        var obj = JSON.parse(payload);
////        try{
////            plotOnReceive(obj);
////        }catch(err){
////            console.log(err);            
////        }
//    }else if (subtopic == "connection"){
//        console.log(subtopic);
//        console.log
//    }
//
//};
//

$(document).ready(function() {
    var data;
    var dev;
    var delete_url = '../../api/client/device/destroy'
    var chart_url = '../charts'
    
    table = $('table').DataTable({
//        "ajax": {
//            "url": "/tables/data.json",         //punky
//            "data": {"user_id": 451}},
//        "columnDefs": [ {
//            "targets": -1,
//            "data": null,
//            "defaultContent": "<button id= 'edit' type='button' class='btn btn-outline btn-info'>Edit</button> <button id = 'delete' type='button' class='btn btn-outline btn-danger'>Delete</button>"
//        } ]
        responsive: true
    });

//    $('table').DataTable({
//        responsive: true
//    });

    $('table tbody').on( 'click', 'button', function () {
        data = table.row( $(this).parents('tr') ).data();
        var id = $(this).attr('class').split(' ')[2];
//        console.log(id);
        console.log(data);
        dev = data[1];
        if (id == 'btn-info'){
//            $.get(chart_url + "/?q=" + dev , function( data ) {
//                $( ".result" ).html( data );
//              alert( "Load was performed." );
//            });
            location.href = chart_url + "?dev_id=" + dev;
        }else if(id == 'btn-danger'){
            
        }
    });
    
    $('#delete_button').click(function(){
        console.log(data);
//        $.ajax({
//            type: 'POST',
//            url: delete_url,
//            data: {device_id  : data[1]}, // or JSON.stringify ({name: 'jonas'}),
//            success: function(data) {
////                window.location.href = data.redirect;
//                window.location.href = redirect_url;
//                alert('data: ' + data);
//            },
//            contentType: "application/json",
//            dataType: 'json'
//        });
    });

    $('#confirm-delete').on('show.bs.modal', function(e) {
        $(this).find('.btn-ok').attr('href', delete_url + "/" + dev);
//        $(this).find('.btn-ok').attr('href', $(e.relatedTarget).data('href'));
        
//        $('.debug-url').html('Delete URL: <strong>' + $(this).find('.btn-ok').attr('href') + '</strong>');
    });

} );