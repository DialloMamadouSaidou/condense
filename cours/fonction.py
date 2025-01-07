"""
from PIL import Image, ImageEnhance
image = Image.open("/home/med/Documents/imagedir/_images/portrait.jpg")
image = ImageEnhance.Brightness(image)
image = image.enhance(1.0)
image = ImageEnhance.Sharpness(image)
image.enhance(2.6).show()
"""
import ast
from pathlib import Path
import shutil

from django.core.cache import cache
from django.http import JsonResponse

from all.settings import MEDIA_ROOT
import os
import time

from typing import List, Dict, Set
from pprint import pprint
from collections import defaultdict, deque
from django.conf import settings
from faker import Faker
from datetime import date, datetime
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


#cette fonction me permet de crée des pdfs
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


class group_Exist(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class File_Exist(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


#cette classe est bcp faite pour les étudiants.
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

    def _recherche_all(self, concerne, dir):
        if concerne in [i for item in self.name for key, value in item.items() for i in value[f"{dir}"]]:
            for item in self.name:
                for key, value in item.items():
                    if concerne in value[f"{dir}"]:
                        return key
        else:
            return -1   #le return -1 indique que le fichier nexiste pas dans ma base de donné encores

    def _help_add(self, concerne, groupe, dir, name_exam): #cette fonction me facilite lajout dans nimporte quel context
        #que sa sois pour le fichier, letudiant, ou la  note.
        for item in self.name:
            for key, value in item.items():
                if key == groupe:
                    for index, content in enumerate(value[dir]):
                        #####Pour ce qui suit en bas sera pour les notes et les files, lajout etudiant ne sera pas concerné
                        for k, v in content.items():
                            if k == name_exam:
                                content[k] = concerne
                                break
                #print("**"*25)

    def ajout_fichier(self, file, groupe, exam):

        mon_groupe_concerne = self.recherche_element(groupe)
        if mon_groupe_concerne != -1:
            self._help_add(file, groupe, "file", exam)

        else:
            raise group_Exist("Ce groupe nous lavons pas dans notre BD")

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
                raise Etudiant_Exist(f"letudiant existe déjà au groupe {list(self.rechercher_etudiant(etudiant))[0]}")
        else:
            print("Le groupe nexiste pas!")

    def supprimer_etudiant(self, etudiant):
        reponse, index = self.rechercher_etudiant(etudiant)
        if reponse != -1:
            element = self.name[index]

            for value in element.values():
                for _ in value["ETUDIANT"]:
                    mon_index = value["ETUDIANT"].index(etudiant)
                    value["ETUDIANT"][mon_index] = ""
                    value["ETUDIANT"] = reorganise_liste(value["ETUDIANT"])
                    break

        else:
            raise Etudiant_Exist("Desolé letudiant nexiste pas!")

    def supprimer_note(self, groupe, etudiant):
        pass

    def rechercher_etudiant(self, etudiant):

        if etudiant in [i for item in self.name for key, value in item.items() for i in value["ETUDIANT"]]:
            for item in self.name:
                for key, value in item.items():
                    if etudiant in value["ETUDIANT"]:
                        return key, self.recherche_element(key)
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

    def rechercher_fichier(self, file):

        if file in [i for item in self.name for key, value in item.items() for i in value["file"]]:
            for item in self.name:
                for key, value in item.items():
                    if file in value["file"]:
                        return key

        else:
            return -1

    def estnote(self, exam: str, etudiant: str):
        reponse, indexis = self.rechercher_etudiant(etudiant)
        note_temporaire = self.name[indexis][reponse].get("Note")

        for item in note_temporaire:
            #print(item)
            for key, value in item.items():
                if key == exam:
                    if value != "":
                        return value

        return False




#Utilisé dans ma vu et reglementation
def aide_recherche(content, name):
    #Cette fonction est utilisé dans la vue pour mes choix de cours
    #La fonction maide à rechercher un cours dans le champs cours
    if name in content:
        return content.index(name)
    else:
        return -1


class verifi_dico_in_planifie:

    def __init__(self, dico: dict):
        self.dico = dico

    def aide_de_gerance(self):
        for key, value in self.dico.items():
            for item in value:
                for k, v in item.items():
                    pass

    def recherche_manque(self):     #cette fonction sera amelioré au fure et à mesure
        for key, value in self.dico.items():
            for item in value:
                for k, v in item.items():
                    if v == "":
                        return f"{key}{k}"

        else:
            return -1

    def inverse_manque(self):   #cette fonction au contraire ne cheche pas les
        #champs qui ne sont pas renseignés mais ceux qui sont renseignés pour
        #géré les inputs en cas derreur
        liste_content = []
        for key, value in self.dico.items():
            for item in value:
                for k, v in item.items():
                    if v != "":
                        liste_content.append(f"{k.lower()}~{key}")

        return liste_content


def vide_liste(liste: List[str]) -> List[str]:
    return [item for item in liste if item != ""]


def normalise_date(date: List) -> str:
    veritable_jours_debut = date[0].split('-')[0].split('.')

    veritable_jours_debut = f"{veritable_jours_debut[1]}-{veritable_jours_debut[0]}-{veritable_jours_debut[-1]}"

    return veritable_jours_debut

def recherche_nom_fichier(dir: str, nom_fichier: str):
    mon_dossier = Path(MEDIA_ROOT)

    mon_dossier = [item for item in mon_dossier.glob('*') if item.is_dir()]

    mon_dossier_content = [element.name for item in mon_dossier if item.name == dir for element in item.glob('*')]

    if nom_fichier in mon_dossier_content:
        return True

    else:
        return False


#cette classe va me permettre de faire mes depot de fichier pour mes professeur
#genre les td, examen annonce et consors
#Information importante:

#couleur_rouge designe les dates de debut
#couleur_bleu designe les dates de depot pour les étudiants


#'8.2.2024- nene~50- Programmation_debutant',
#exemple de date

#en general dans cette classe tant que
#jai la reponse qui me donne la valeur 1 ce que cest faux en resumé ce nétait pas sa qui était attendu

class depot_vide(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class confus_date(Exception):

    def __init__(self, message):
        self.message = message

        super().__init__(self.message)

class confus_month(Exception):

    def __init__(self, message):
        self.message = message

        super().__init__(message)

class confus_day(Exception):

    def __init__(self, message):
        self.message = message

        super().__init__(message)

class exces_date(Exception):

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class exces_month(Exception):

    def __init__(self, message):
        self.message = message

        super().__init__(self.message)
class depot_fichier:
    def __init__(self, couleur_rouge, couleur_bleu):
        self.couleur_rouge = couleur_rouge
        self.couleur_bleu = couleur_bleu
        self.today_exact = date.today().strftime('%d-%m-%Y')

    def verif_logique(self):

        try:
            reponse = self.verif_longueur_bleu_rouge()

            if reponse == 0:
                if len(self.couleur_rouge) == 0:    #si la date de debut n'a pas été donné la date daujourdhui sera la date par défaut
                    self.couleur_rouge = date.today().strftime('%d-%m-%Y')
                else:
                    self.couleur_rouge = normalise_date(self.couleur_rouge)

                self.couleur_bleu = normalise_date(self.couleur_bleu)

                """
                    je dois verifier les mois en sassurant qu'on a pas des mois
                    qui ne correspondent pas où le mois darrivé est inferieur
                    au mois initial
                """
                month_exact = int(self.today_exact.split('-')[1])
                month_rouge = int(self.couleur_rouge.split('-')[1])
                month_bleu = int(self.couleur_bleu.split('-')[1])

                if any(mois > 12 for mois in [month_exact, month_rouge, month_bleu]):
                    raise exces_month("Attention vous ne pouvez pas avoir un mois qui depasse 12!")
                #jai verifier la logique des mois ici

                if month_exact > month_rouge or month_rouge > month_bleu:
                    raise confus_month("Verifié bien la logique des mois que vous avez choisi")

                #et maintenant ici je verifie la logique des jours ici les dates
                else:

                    date_exact = int(self.today_exact.split('-')[0])
                    date_rouge_exact = int(self.couleur_rouge.split('-')[0])
                    date_bleu_exact = int(self.couleur_bleu.split('-')[0])
                    if month_exact == month_rouge and month_rouge == month_bleu:

                        if any(dates > 31 for dates in [int(date_exact), int(date_rouge_exact), int(date_bleu_exact)]):
                            raise confus_day("Attention vous ne devez pas avoir une date qui dépasse 31")

                        if int(date_exact) > int(date_rouge_exact) or int(date_rouge_exact) > int(date_bleu_exact):
                            raise confus_day("Regardez bien vos jours dans le meme mois, ces entrées ne sont pas correct!")

                        else:
                            return self.couleur_rouge, self.couleur_bleu    #sa veut dire ici que tout mes controles sont corrects

                    elif month_exact != month_rouge and month_rouge == month_bleu:

                        if date_rouge_exact > date_bleu_exact:

                            raise confus_day("Regardez bien le jours du dépot il doit pas étre infeur à la date daujourdhui")

                        else:
                            return self.couleur_rouge, self.couleur_bleu
                        """
                                                    if int(date_rouge_exact) < int(date_exact):
                        else:

                            
                        """
                    else:
                        return self.couleur_rouge, self.couleur_bleu

        except confus_date as e:
            raise confus_date(e)
        """
             cette fonction va permettre de verifier si les dates de debut sont logique
             par exemple si la date des débuts est inférieur de la date daujourdhui
        """

    def verif_longueur_bleu_rouge(self):

        try:
            reponse_date_depot = self.not_date_depot()

            if reponse_date_depot == 0:
                if len(self.couleur_bleu) != 1:

                    raise confus_date("Vous ne pouvez avoir qu'une seule date de depot ou de reprise de document!")

                else:
                    return 0

        except depot_vide as e:

            raise depot_vide(e)

        """
            cette fonction va me permettre de 
            verifier si jai une date de depot dentré
        """

    def not_date_depot(self):

        if len(self.couleur_bleu) == 0:
            raise depot_vide("Vous devez entrez une date de depot")

        return 0


def enregistre_tp_venant_de_prof(file, if_group_create, request, mon_rouge, mon_bleu):

    for key, value in file.items():
        name = f"{request.user.email}-{key}-dep_exam-{value.name}"
        mon_dossier_complet = os.path.join(settings.MEDIA_ROOT, 'creation_tp_prof',
                                           name)

        reponse = recherche_nom_fichier('creation_tp_prof', name)
        if reponse:
            print("Cet element existe déjà ou vous voulez le surpasser")
            cache.delete('couleur_rouge')
            cache.delete('couleur_bleu')
            return JsonResponse({'file_exist': 'yes'})
            # cette partie n'est pas encore touché
        else:
            os.makedirs(os.path.dirname(mon_dossier_complet), exist_ok=True)
            print("Document à enregistrer")

            with open(mon_dossier_complet, 'wb') as f:

                for chunk in value.chunks():
                    f.write(chunk)

                print(key)


                #if len(mon_rouge) > 0:
                 #   veritable_jours_debut = normalise_date(mon_rouge)

                if len(mon_rouge) == 0:
                    mon_rouge = date.today().strftime('%d-%m-%Y')
                #veritable_jours_fin = normalise_date(mon_bleu)

            if_group_create.file_prof = ast.literal_eval(if_group_create.file_prof)
            if_group_create.file_prof[key]["file"] = value.name
            if_group_create.file_prof[key]['debut'] = mon_rouge
            if_group_create.file_prof[key]['fin'] = mon_bleu

            if_group_create.save()

            return 1


def help_affichage_pour_aide_td_pour_etudiant(element: dict):

    to_day = datetime.today()

    liste_finale = []
    for key, value in element.items():

        if value["file"] != "":
            temp_date = datetime.strptime(value["debut"], '%d-%m-%Y')

            reponse_dif = (temp_date - to_day).days

            if reponse_dif <= 0:
                liste_finale.append({key: value["file"]})

    return liste_finale

def convert_seconde_en_minute_heure(seconde):

    heure = seconde // 3600
    minute = (seconde % 3600) // 60
    secondes = seconde % 60

    return heure, minute, secondes

if __name__ == "__main__":

    """
         print(convert_seconde_en_minute_heure(3601))
    date = ["9.20.2024- - "]
    normalise_date(date)
    variable_essai = {'nene~50': {'file': 'HACK-FACEBOOK.pdf', 'debut': '25-10-2024', 'fin': '27-10-2024'}, 'baba~50': {'file': 'amisso_admission.pdf', 'debut': '13-9-2024', 'fin': '27-9-2024'}}

    mon_element_daffiche_logique = help_affichage_pour_aide_td_pour_etudiant({'nene~50': {'file': 'HACK-FACEBOOK.pdf', 'debut': '25-10-2024', 'fin': '27-10-2024'}, 'baba~50': {'file': 'amisso_admission.pdf', 'debut': '13-9-2024', 'fin': '27-9-2024'}})

    print(mon_element_daffiche_logique)

    """



    #print(reponse)


    reponse = recherche_nom_fichier('creation_tp_prof','koto@gmail.com-baba~50-dep_exam-1-Libellé du TP3.pdf')
    print(reponse)

    
   
    index = 0
    mon_dico = [{1: {'ETUDIANT': ['mamadou saidou diallo', 'nene an', ''], 'Note': [{'nene~50': ''}, {'baba~50': ''}], 'file': [{'nene~50': ''}, {'baba~50': ''}], 'limit': 2}},
                {2: {'ETUDIANT': ['nene', '', ''], 'Note': [{'nene~50': ''}, {'baba~50': ''}], 'file': [{'nene~50': ''}, {'baba~50': ''}], 'limit': 2}},
                {3: {'ETUDIANT': ['', 'Aminata', ''], 'Note': [{'nene~50': '50'}, {'baba~50': '50'}], 'file': [{'nene~50': ''}, {'baba~50': ''}], 'limit': 2}}]
    essaie_note = gere_note_groupe(mon_dico)

    ma_reponse = essaie_note.estnote("nene~50", "Aminata")


    print(ma_reponse)
    """
    essaie_note.ajout_fichier('bab.pdf', 2, 'baba~50')
    #essaie_note.ajout_fichier("saidou.pdf", 0, "baba~50")

    print(mon_dico)
    #essaie_note._help_add("saidou.pdf", 1, "file")
    #print(mon_dico)
    #rep = aide_recherche(["saidou", "kotoan", "baba"], "kotoan")

     """

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
