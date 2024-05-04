console.log("hello mamadou saidou");

var element_cache = $('.label4');
var element_montre = $('.label3');
    element_montre.hide();




    $(".label4").click(function(){
        var password = $("#password");
        var confirm = $("#confirmation")
        password.attr('type', 'text');
        confirm.attr('type', 'text');
        element_montre.show();
        element_cache.hide();
    })

    $(".label3").click(function(){
        var password = $("#password");
        var confirm = $("#confirmation");
        password.attr('type', 'password');
        confirm.attr('type', 'password');
        element_montre.hide();
        element_cache.show();
    })

function cacheme(){
    $(".programme").hide();
}

function showme(){
    $(".programme").show();
}

$('#choix').change(function(){
    var element = $(this).val();
    if ((element == "charge_cours") || (element == "etudiant")){
        index = 1;
        showme();
    }
    else {
        index = 0;
        cacheme();

    }
    console.log(element);
})