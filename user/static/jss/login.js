//console.log("hello mamadou saidou");

var element =1;
var index = 1;

    console.log("hello world");
    var element_cache = $('.label4');
    var element_montre = $('.label3');
    element_montre.hide();
    element_cache.hide();
    $(".form_input2").focus(function(){
        element_cache.show();
    })



    $(".label4").click(function(){
        var password = $("#password");
        password.attr('type', 'text');
        element_montre.show();
        element_cache.hide();
    })

    $(".label3").click(function(){
        var password = $("#password");
        password.attr('type', 'password');
        element_montre.hide();
        element_cache.show();
    })
