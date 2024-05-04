console.log("Hello Mamadou Saidou Diallo");


var myname = document.querySelectorAll('.name');
var ligne = document.querySelectorAll('.line')
var title = document.querySelectorAll('.title');

$('.line').eq(0).hide();
for(var i=1; i<myname.length; i++){
        if(myname[i].innerHTML == myname[i-1].innerHTML){
            $('.line').eq(i).hide();
        }
        if(title[i].innerHTML == title[i-1].innerHTML){
            $('.title').eq(i).hide();
        }
    }
$('.name').hide();

console.log("hello mamadou saidou diallo comment vas tu ?")