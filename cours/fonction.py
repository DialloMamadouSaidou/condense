"""
from PIL import Image, ImageEnhance
image = Image.open("/home/med/Documents/imagedir/_images/portrait.jpg")
image = ImageEnhance.Brightness(image)
image = image.enhance(1.0)
image = ImageEnhance.Sharpness(image)
image.enhance(2.6).show()
"""
from pprint import pprint
from collections import defaultdict, deque


class file_verify:
    def __init__(self, image, video, document):
        self.image = image
        self.video = video
        self.document = document
        self.message_error = {}

    def verifie_image(self):
        terminaison_image = ['jpg', 'jpeg', 'png']
        termine = self.image.split('.')[-1]
        if not termine in terminaison_image:
            self.message_error['imageF'] = "Le format dimage nest pas respecté!"
        return self.message_error

    def verifie_video(self):
        terminaison_video = ['mp4', 'avi']
        termine = self.video.split('.')[-1]
        if not termine in terminaison_video:
            self.message_error["videoF"] = "Le format de video nest pas respecté!"
            #return self.message_error
        return self.message_error

    def verifie_document(self):
        terminaison_document = ['pdf', 'docx', 'odt', 'txt', 'tar']
        termine = self.document.split('.')[-1]
        if not termine in terminaison_document:
            self.message_error["docF"] = "Le format de document nest pas respecté!"
        return self.message_error

    def general(self):
        self.verifie_image()
        self.verifie_video()
        self.verifie_document()
        return self.message_error

    def __str__(self):
        return f"limage est {self.image}, la video est {self.video}, le document est {self.document}"


def notation(majoration, note) -> float:  #Retourne la moyenne qu'il à reçu en pourcentage
    return note * 100 / majoration


#Ces fonctions son justes utilisé au niveau de la fonction de la notation des etudiants par le prof
def moyenne(liste_note: list) -> float:
    somme = 0
    for item in liste_note:
        somme += item

    return round(somme / len(liste_note), 4)


def calcul_moyenne(liste_note: list, majoration: list):
    liste = []
    dico_note = defaultdict(list)
    for index, item in enumerate(liste_note):
        for i, valeur in enumerate(item):
            valeur = list(valeur)
            essentiel, ponde = valeur[0], valeur[1]
            name, note = essentiel.split('~')

            result = 0

            if note == '':
                result = 0

            else:
                result = round(notation(majoration[i], int(note)), 4)

            dico_note[name].append(result)

    return dico_note


def decortique(dico: dict):
    """
    Cette fonction permet de casser un dictionnaire donné en paramètre en donnant juste des clés
    Mais attention on parle dici de dico vraiment complexe.
    La fonction est utilisé dans la vue give_note_max pour donner a chaque exam une note max.
    """
    liste = []
    dico2 = {}
    for key, value in dico.items():
        for k, v in value.items():
            dico2[k] = ''

    return dico2


#-------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    dico = {'0': {'exam0': '35'}, '1': {'exam1': '40'}, '2': {'exam2': '25'}}
    dico2 = decortique(dico)
    print(dico2)

    """
         liste_etudiant = [
        [('etudiant1@example.com~15', '72'), ('etudiant1@example.com~7', '84')],
        [('etudiant2@example.com~18', '56'), ('etudiant2@example.com~9', '50'), ],
        [('etudiant3@example.com~6', '30'), ('etudiant3@example.com~11', '92')],
        [('etudiant4@example.com~14', '65'), ('etudiant4@example.com~9', '81')],
        [('etudiant5@example.com~7', '41'), ('etudiant5@example.com~0', '58')],

        # Les données pour les autres étudiants suivent ici...
    ]

    dico = calcul_moyenne(liste_etudiant, [20, 22])
    ma_note = notation(20, 18.85)
    for key in dico:
        dico[key].append(moyenne(dico[key]))

    for key, values in dico.items():
        print(key, values)
        print("--"*20)
    """

"""
from PIL import Image, ImageEnhance
image = Image.open("/home/med/Documents/imagedir/_images/portrait.jpg")
image = ImageEnhance.Brightness(image)
image = image.enhance(1.0)
image = ImageEnhance.Sharpness(image)
image.enhance(2.6).show()
"""
from pprint import pprint
from collections import defaultdict, deque


class file_verify:
    def __init__(self, image, video, document):
        self.image = image
        self.video = video
        self.document = document
        self.message_error = {}

    def verifie_image(self):
        terminaison_image = ['jpg', 'jpeg', 'png']
        termine = self.image.split('.')[-1]
        if not termine in terminaison_image:
            self.message_error['imageF'] = "Le format dimage nest pas respecté!"
        return self.message_error

    def verifie_video(self):
        terminaison_video = ['mp4', 'avi']
        termine = self.video.split('.')[-1]
        if not termine in terminaison_video:
            self.message_error["videoF"] = "Le format de video nest pas respecté!"
            #return self.message_error
        return self.message_error

    def verifie_document(self):
        terminaison_document = ['pdf', 'docx', 'odt', 'txt', 'tar']
        termine = self.document.split('.')[-1]
        if not termine in terminaison_document:
            self.message_error["docF"] = "Le format de document nest pas respecté!"
        return self.message_error

    def general(self):
        self.verifie_image()
        self.verifie_video()
        self.verifie_document()
        return self.message_error

    def __str__(self):
        return f"limage est {self.image}, la video est {self.video}, le document est {self.document}"


def notation(majoration, note) -> float:  #Retourne la moyenne qu'il à reçu en pourcentage
    return note * 100 / majoration


#Ces fonctions son justes utilisé au niveau de la fonction de la notation des etudiants par le prof
def moyenne(liste_note: list) -> float:
    somme = 0
    for item in liste_note:
        somme += item

    return round(somme / len(liste_note), 4)


def calcul_moyenne(liste_note: list, majoration: list):
    liste = []
    dico_note = defaultdict(list)
    for index, item in enumerate(liste_note):
        for i, valeur in enumerate(item):
            valeur = list(valeur)
            essentiel, ponde = valeur[0], valeur[1]
            name, note = essentiel.split('~')

            result = 0

            if note == '':
                result = 0

            else:
                result = round(notation(majoration[i], int(note)), 4)

            dico_note[name].append(result)

    return dico_note


def decortique(dico: dict):
    """
    Cette fonction permet de casser un dictionnaire donné en paramètre en donnant juste des clés
    Mais attention on parle dici de dico vraiment complexe.
    La fonction est utilisé dans la vue give_note_max pour donner a chaque exam une note max.
    """
    liste = []
    dico2 = {}
    for key, value in dico.items():
        for k, v in value.items():
            dico2[k] = ''

    return dico2


#-------------------------------------------------------------------------------------------------------------

#fonction qui va permettre de rajouter mes notes dans ma base de donné à chaque fois.

def regroupe_synchronise(liste1: list, liste2: list) -> list:
    pass


if __name__ == "__main__":
    """
    dico = {'0': {'exam0': '35'}, '1': {'exam1': '40'}, '2': {'exam2': '25'}}
    dico2 = decortique(dico)
    print(dico2)

    
         liste_etudiant = [
        [('etudiant1@example.com~15', '72'), ('etudiant1@example.com~7', '84')],
        [('etudiant2@example.com~18', '56'), ('etudiant2@example.com~9', '50'), ],
        [('etudiant3@example.com~6', '30'), ('etudiant3@example.com~11', '92')],
        [('etudiant4@example.com~14', '65'), ('etudiant4@example.com~9', '81')],
        [('etudiant5@example.com~7', '41'), ('etudiant5@example.com~0', '58')],

        # Les données pour les autres étudiants suivent ici...
    ]

    dico = calcul_moyenne(liste_etudiant, [20, 22])
    ma_note = notation(20, 18.85)
    for key in dico:
        dico[key].append(moyenne(dico[key]))

    for key, values in dico.items():
        print(key, values)
        print("--"*20)
    """
