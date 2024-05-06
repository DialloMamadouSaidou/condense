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


def notation(majoration, note) -> float:    #Retourne la moyenne qu'il à reçu en pourcentage
    return note * 100 / majoration


#Ces fonctions son justes utilisé au niveau de la fonction de la notation des etudiants par le prof
def moyenne(liste_note: list) -> float:
    somme = 0
    for item in liste_note:
        somme += item

    return round(somme/len(liste_note), 4)


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



def calcul_tien_compte():
    pass

#-------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    liste_etudiant = [[('saidessai466@gmail.com~19', '45'), ('saidessai466@gmail.com~19', '55')],
                      [('lamarana@gmail.com~15', '45'), ('lamarana@gmail.com~19', '55')]]
    dico = calcul_moyenne(liste_etudiant, [20, 22])
    ma_note = notation(20, 18.85)
    for key in dico:
        dico[key].append(moyenne(dico[key]))

    for key, values in dico.items():
        print(key, values)
        print("--"*20)
