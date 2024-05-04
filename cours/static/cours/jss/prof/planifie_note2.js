var index=0;



const button = document.getElementById('ajouter');

button.addEventListener("click", ajoute);

function clonerBlock() {
        const template = document.querySelector('#first-message');
        const output = document.querySelector('.output');

        const  clone = template.cloneNode(true);
        clone.id = '';
        output.appendChild(clone);

        var mon_text = clone.querySelector('.message');
        var ponde = clone.querySelector('.pond');

        mon_text.name = 'text+' + index;
        ponde.name = 'ponde+' + index;
        index ++;
        return clone.querySelector('.message');

}

function écrire(message){
        var element = clonerBlock();
        element.value = message;
        return element;
}

function ajoute(){
        var mon_text = document.getElementById('chapitre');
        if(mon_text.value === ''){
                console.log("Input vide");
        }
        else{
                écrire(mon_text.value);
                mon_text.value = '';
        }

}

function supprimerMessage(button){
        var parent_div = button.parentElement;

        parent_div.remove();
}
