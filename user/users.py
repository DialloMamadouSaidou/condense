import string
from pprint import pprint


class Verify:
    context = {}

    def __init__(self, password):
        self.password = password

    def __str__(self):
        return self.password

    def verln(self):
        if len(self.password) < 8:
            self.context['lenf'] = 'Votre mot de passe content moins de 8 characteres'
        else:
            self.context['lent'] = 'Longueur verifié'

        return self.context

    def vermaj(self):
        maj = [asc for asc in string.ascii_uppercase]

        for let in self.password:

            if str(let) in maj:
                self.context['majt'] = 'Merci pour lajout de la majuscule'
                break
            else:
                self.context['majt'] = ''

        if self.context['majt'] == '':
            self.context['majf'] = 'Veuillez ajouter une majuscule'

        # return self.context

    def vernu(self):
        numbers = [num for num in string.digits]
        i = 0
        for let in self.password:

            if str(let) in numbers:
                i += 1
        if i == len(self.password):
            self.context['dig'] = 'Le mot de passe dois pas être digit'

        elif i < len(self.password) and i > 0:
            self.context['vernut'] = "Merci d'avoir ajouté un chiffre"

        else:
            self.context['verf'] = 'Veuillez ajouter un chiffre'

        return self.context

    def sepeci(self):
        punct = [punc for punc in string.punctuation]
        for let in punct:

            if let in self.password:
                self.context['punct'] = "Merci pour lajout du caractere special"
                break

            else:
                self.context['punct'] = ''

        if self.context['punct'] == '':
            self.context['puncf'] = "Le mot de passe dois contenir une caractere special"

        return self.context

    def general(self):
        self.verln()
        self.vermaj()
        self.vernu()
        self.sepeci()
        return self.context


if __name__ == '__main__':
    import string

    context = {}
    liste,values = [], []
    i, j = 0, 0
    saidou = str(input('donnez votre mot de passe afin detre verifié: '))
    verif = Verify(saidou)
    context = verif.general()
    for key, value in context.items():
        if key.endswith('f'):
            liste.append(key)
            values.append(value)

    if len(values) > 0:
        pprint(values)

    else:
        print("Votre mot de passe est rassurant.")
