console.log("hello world!");
    var item;
    let mes_choix = document.querySelectorAll(".choice");

    let mes_cle = document.querySelectorAll(".cle");

    mes_cle.forEach(function(item){
       console.log(item.innerHTML);
    });


mes_choix.forEach(function(item){
var index = 1;
item.addEventListener("click", function(){

if(index === 1){
            this.checked = true;
            index = 0;
}else {
            this.checked = false;
            index = 1;
};
        })
    });

$("#icon-erreur").hide();

$("#modifie").click(function(){
    mes_choix.forEach(function(item){
        item.disabled = false;
    })
});

$("#post-choix").on("submit", function(e){
    e.preventDefault();
    var form_data = $(this).serialize();
$.ajax({
        type: "POST",
        url: createGroupUrl,

        data: form_data,
        success: function(response){
            console.log(response.valeur);
            if(response.valeur){
                $("#icon-erreur").show();
            }
            else{
                $("#icon-erreur").hide();
            }

        }
})


})