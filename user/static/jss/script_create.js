

function cacheme(){
    $(".programme").hide();
}

function showme(){
    $(".programme").show();
}

$('#choix').change(function(){
    var element = $(this).val();
    if ((element == "charge_crs") || (element == "etudiant")){
        index = 1;
        showme();
    }
    else {
        index = 0;
        cacheme();

    }
    /*

    */
    console.log(element);
})

console.log(index);