"""
from PIL import Image, ImageEnhance
image = Image.open("/home/med/Documents/imagedir/_images/portrait.jpg")
image = ImageEnhance.Brightness(image)
image = image.enhance(1.0)
image = ImageEnhance.Sharpness(image)
image.enhance(2.6).show()
"""
import os
import time
from pprint import pprint
from collections import defaultdict, deque
from django.conf import settings
from faker import Faker
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import LETTER
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer


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
    Fonction pour un cas bcp specifique.
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


def create_pdf(name_pdf, data):
    path = os.path.join(settings.MEDIA_ROOT, "pdfs")
    os.makedirs(path, exist_ok=True)
    path = os.path.join(path, name_pdf)

    fake = Faker()
    code = fake.bothify('?????###-??-\?;???')
    document = SimpleDocTemplate(
        path,
        pagesize=LETTER,
        title="Relevé de note"
    )

    col_width = [250, 100, 100]
    row_height = [70] * len(data)
    table = Table(data, rowHeights=row_height, colWidths=col_width)

    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.Color(117, 195, 95)),
        ("FONTNAME", (0, 0), (-1, -1), "Courier-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 14),
        ('TEXTALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 25),
        ('LEFTPADDING', (0, 0), (-1, -1), 15),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.blue)

    ])

    table.setStyle(style)

    for item in range(1, len(data)):
        if item % 2 == 0:
            bc = colors.burlywood
        else:
            bc = colors.beige

        ts = TableStyle([
            ("BACKGROUND", (0, item), (-1, item), bc)

        ])

        table.setStyle(ts)

    ts = TableStyle([

        ("GRID", (0, 0), (-1, -1), 2, colors.black)
    ])
    spacer = Spacer(1, 12)
    table.setStyle(ts)
    element = []

    style = getSampleStyleSheet()

    text = f"""
        Allo Mamadou Saidou,
        comment vas tu, je vais bien
        Hello Mamadou Saidou Diallo
        hmdl et la famille de ton coté sa roule jespère <br></br>
        <i color="blue">{code}</i>
    """

    custom_style = ParagraphStyle(
        name='Custom Style',
        parent=style["Normal"],
        fontName='Courier-Bold',
        fontSize=25,
        leading=25,
        Alignment=1,
        spaceAfter=20,
        textColor=colors.brown

    )
    paragraph_text = Paragraph(text, custom_style)

    element = [paragraph_text, spacer, table]

    document.build(element)

    return path


def reorganise_liste(liste):
    non_vides = [element for element in liste if element]
    vide = [element for element in liste if not element]

    return non_vides + vide


class Etudiant_Exist(Exception):

    def __init__(self, message="Letudiant est déjà dans un groupe"):
        self.message = message
        super().__init__(self.message)


class gere_note_groupe:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def recherche_element(self, element) -> int:  #Cette fonction verifie si un groupe existe ou pas

        liste_groupe = [key for item in self.name for key in item]
        if element in liste_groupe:
            return liste_groupe.index(element)

        else:
            return -1

    def ajout_note(self, groupe: int, note: float):
        reponse = self.recherche_element(groupe)
        if reponse != -1:
            element = self.name[reponse]
            for value in element.values():
                value["Note"] = str(note)
        else:
            raise ValueError("Ce numéro de groupe nexiste pas!")

    def ajout_etudiant(self, groupe: int, etudiant):
        reponse = self.recherche_element(groupe)
        dico = self.place_limite_and_available()

        if reponse != -1:
            if self.rechercher_etudiant(etudiant) == -1:
                if dico[groupe] != 0:
                    element = self.name[reponse]
                    for value in element.values():
                        for item, valeur in enumerate(value["ETUDIANT"]):
                            if valeur == "":
                                value["ETUDIANT"][item] = etudiant
                                break

                else:
                    raise Etudiant_Exist("Letudiant existe déjà")
            else:
                raise Etudiant_Exist(f"letudiant existe déjà au groupe {self.rechercher_etudiant(etudiant)}")
        else:
            print("Le groupe nexiste pas!")

    def supprimer_etudiant(self, groupe, etudiant):
        reponse = self.recherche_element(groupe)
        if reponse != -1:
            element = self.name[reponse]
            rep = self.rechercher_etudiant(etudiant)

            for value in element.values():
                for item in value["ETUDIANT"]:
                    mon_index = value["ETUDIANT"].index(etudiant)
                    value["ETUDIANT"][mon_index] = ""
                    value["ETUDIANT"] = reorganise_liste(value["ETUDIANT"])
                    break

        else:
            pass

    def supprimer_note(self, groupe, etudiant):
        pass

    def ajout_fichier(self, groupe, file):
        pass

    def rechercher_etudiant(self, etudiant):

        if etudiant in [i for item in self.name for key, value in item.items() for i in value["ETUDIANT"]]:
            for item in self.name:
                for key, value in item.items():
                    if etudiant in value["ETUDIANT"]:
                        return key
        else:
            return -1

    #la place limite est automatiquement instauré dans la création de ma table
    #la place disponible que je dois calculé
    def place_limite_and_available(self):
        ma_reference = {}
        for item in self.name:
            for key, value in item.items():
                nombre_empty = sum(1 for char in value["ETUDIANT"] if char != "")
                ma_reference[key] = value["limit"] - nombre_empty

        return ma_reference

    def rajout_longueur_etudiant(self, groupe, ma_nouvelle_liste):
        search_group = self.recherche_element(groupe)

        if search_group != -1:
            index = 0
            etudiant, rep = "", ""
            for item in ma_nouvelle_liste:
                if item != "":
                    rep = self.rechercher_etudiant(item)
                    if rep != -1:
                        index = 1
                        etudiant = item
                        break

            if index == 1:
                raise Etudiant_Exist(f"Letudiant {etudiant} existe déjà au groupe {rep}")
            else:

                mon_concerne = self.name[search_group]
                for key, value in mon_concerne.items():
                    value["ETUDIANT"].extend(ma_nouvelle_liste)
                    value["ETUDIANT"] = reorganise_liste(value["ETUDIANT"])

        else:
            print("Ce groupe nexiste pas")


if __name__ == "__main__":
    mon_dico = [{1: {"ETUDIANT": ["", "", "", ""], "Note": "", "limit": 4}},
                {2: {"ETUDIANT": ["", "mamadou", "", ""], "Note": "5", "limit": 4}}]
    essaie_note = gere_note_groupe(mon_dico)
    essaie_note.ajout_note(2, 5)
    #essaie_note.ajout_etudiant(1, "KOTO")
    #essaie_note.ajout_etudiant(1, "mignan an")
    #essaie_note.ajout_etudiant(1, "saidou")

    #print(essaie_note.rechercher_etudiant("KOTO"))
    essaie_note.rajout_longueur_etudiant(1, ["mamadou", ""])
    print(mon_dico)


    #print(mon_dico)
    #print("--"*50)
    #print(essaie_note.place_limite_and_available())
    #element = essaie_note.rechercher_etudiant("Saidou")
    #print(element)
    #print(mon_dico)
    #indexi = essaie_note.recherche_element(2)
    #for value in mon_dico[indexi].values():
    #   value["Note"] = "45"

    #print(mon_dico)
    """
    
    data = [
        ["Examen", "Note"],
        ["exam1", 20],
        ["exam2", 40]
    ]
    liste_etudiant = [{'exam1~80': '10'}, {'exam2~20': '16'}]

    #create_pdf("document.pdf", data)

    tableau = [
        {'a': 1, 'b': 2, 'c': 3},
        {'d': 4, 'e': 5},
        {'f': 6, 'g': 7, 'h': 8}
    ]

    # Extraction des clés et valeurs dans une liste globale
    resultat = [[k, v] for dico in tableau for k, v in dico.items()]

    print(resultat)
    """
