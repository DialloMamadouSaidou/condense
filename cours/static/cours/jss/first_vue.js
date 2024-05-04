var buttons = document.querySelectorAll('.titres');

buttons.forEach(button => {

button.addEventListener('click', () => {
    var valeur = button.value;
    console.log(valeur);
    })
})