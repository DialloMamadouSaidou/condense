"""
from PIL import Image, ImageEnhance
image = Image.open("/home/med/Documents/imagedir/_images/portrait.jpg")
image = ImageEnhance.Brightness(image)
image = image.enhance(1.0)
image = ImageEnhance.Sharpness(image)
image.enhance(2.6).show()
"""
import time
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


def notation(majoration, note: float) -> float:  #Retourne la moyenne qu'il à reçu en pourcentage
    return note * 100 / majoration


#Ces fonctions son justes utilisé au niveau de la fonction de la notation des etudiants par le prof
def moyenne(liste_note: list) -> float:
    somme = 0
    for item in liste_note:
        somme += item

    return round(somme / len(liste_note), 4)





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

#Ne pas oublier de garder une copie de mes anciens donnés pour plus d'aisance

def key_dict(liste1):
    liste1 = list(liste1)
    return [key for item in liste1 for key in item.keys()]


def retrouve_element(element: str, liste_c: list):
    """
    Cette fonction permet de retrouver un element dune liste contenant
    des dictionnaires d'élément.
    Il reçoit la clé de lement puis retourne lelement au complète
    liste = [{'exam1': 30}, {'exam2': 40}]
    en donnant exam1 il retounera {'exam1': 30}
    """
    liste_t = key_dict(liste_c)

    if element in liste_t:
        c = liste_t.index(element)
        return liste_c[c]


def trouver_cle_par_valeur(dictionnaire, valeur):
    for cle, val in dictionnaire.items():
        if val == valeur:
            return cle


def disposition_liste(liste_first, liste_second):
    """
    Cette fonction permet d'ordonner la deuxième liste
    en fonction de la disposition de ma première liste
    Utilité dans ma vue au niveau de la notation.
    """
    liste = []
    liste1 = key_dict(liste_first)
    liste2 = key_dict(liste_second)
    mon_dico = {item: index for index, item in enumerate(liste1)}

    liste2.sort(key=lambda x: mon_dico[x])

    for item in liste2:
        liste.append(retrouve_element(item, liste_second))
    return liste


def regroupe_synchronise(liste1: list, liste2: list) -> list:
    """
    Cette fonction est celle qui permet de rajouter des notes aux étudiants
    en donnant deux fonctions si la deuxième liste contient des elements notés,
    il les rajoutera suivant la disposition de la premiere liste
    """
    list_general = []
    if len(liste1) == len(liste2):
        return liste2

    else:
        liste_total = []
        liste3 = key_dict(liste1)
        liste = liste3.copy()
        liste4 = key_dict(liste2)
        liste.extend(liste4)
        uni_liste = list(set(liste))

        for item in uni_liste:
            if liste.count(item) > 1:
                liste_total.append(retrouve_element(item, liste2))
            else:
                liste_total.append(retrouve_element(item, liste1))

        liste_total = disposition_liste(liste1, liste_total)
        return liste_total



def calcul_moyenne(liste_note: list, majoration: list):
    notes = 0
    dico_note = defaultdict(list)
    dico = liste_note[0]

    for i, item in enumerate(liste_note):
        print(i, item)
        for key, note in item.items():
            ponderation = key.split('~')[-1]

            if note != '':
               notes += notation(majoration[i], eval(note)) * eval(ponderation)

            else:
                note = 0
                notes += notation(majoration[i], note) * eval(ponderation)

    return round(notes / 100.0, 4)

if __name__ == "__main__":
    liste_etudiant = [{'exam1~80': '10'}, {'exam2~20': '16'}]

        # Les données pour les autres étudiants suivent ici...


    print(calcul_moyenne(liste_etudiant, [20, 20]))

