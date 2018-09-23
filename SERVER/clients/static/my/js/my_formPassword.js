$('#password + .glyphicon').on('click', function() {
    $(this).toggleClass('glyphicon-eye-close').toggleClass('glyphicon-eye-open'); // toggle our classes for the eye icon
    $('#password').togglePassword(); // activate the hideShowPassword plugin
});

//$('#register_button').click(function(){
//    $("#client")[0].reset();
//});