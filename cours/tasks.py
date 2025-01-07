from celery import shared_task
import time
import ast
from collections import defaultdict
from .essai_fonction import essai_conformite

from pprint import pprint
from datetime import datetime
from .models import *
from user.models import *
from .settings_cours import add_horaire_to_file


#celui là est pour la création d'une hoistorique de Backup pour tout mes users
@shared_task
def my_periodic_task():
    print("Mamamdou Saidou")
    print("hello world")
    liste_general = []
    mes_profiles = Profile.objects.all()
    mes_profiles = [item.user.email for item in mes_profiles]
    all_historique = Historique.objects.all().values("identifiant")
    all_historique = [value for item in all_historique for key, value in item.items()]
    for item in all_historique:
        date, user, code = item.split("~")
        liste_general.append(user)

    print(mes_profiles)
    print(liste_general)

    for item in mes_profiles:
        if item not in liste_general:
            interesser = Profile.objects.get(user__email=item)
            Historique.objects.create(interesser=interesser,
                                      backup={  # Prototype de mon Backup
                                          "Remove": [
                                              {"Programme": [

                                              ]},
                                              {"Module": [

                                              ]},
                                              {"Chapitre": [

                                              ]},
                                              {"Lesson": [

                                              ]},
                                              {"Note": [

                                              ]},
                                              {"Plannification": [

                                              ]},
                                              {"Commentaire": [

                                              ]},
                                              {"Choix_Cours": [

                                              ]},
                                              {"Payer": [

                                              ]},
                                              {"Create_Groupe": [

                                              ]},
                                              {"Historique": [

                                              ]},

                                          ],
                                          "Modify": [
                                              {"Programme": [

                                              ]},
                                              {"Module": [

                                              ]},
                                              {"Chapitre": [

                                              ]},
                                              {"Lesson": [

                                              ]},
                                              {"Note": [

                                              ]},
                                              {"Plannification": [

                                              ]},
                                              {"Commentaire": [

                                              ]},
                                              {"Choix_Cours": [

                                              ]},
                                              {"Payer": [

                                              ]},
                                              {"Create_Groupe": [

                                              ]},
                                              {"Historique": [

                                              ]},
                                          ]
        })

#celui  là est pour la suppression automatique des choix de cours une fois que
#letudiant à décidé de retiré tout les elements il efface meme le id du choix
@shared_task
def enregistre_choix():
    print("hello world im here again")
    all_choices = Choix_Cours.objects.all()

    for item in all_choices:
        item.cours = eval(item.cours)
        if len(item.cours) == 0:
            item.delete()
        #for index in item.cours:
         #   print(index)

@shared_task
def update_because_planification():
    mes_profiles = Profile.objects.filter(choices='charge_cours')
    mes_planifies = Planification.objects.all().values("identifiant")
    mes_planifies = [value for item in mes_planifies for key, value in item.items()]

    dico = defaultdict(list)
    for item in mes_profiles:
        user = item.user
        for enseignant in module.objects.all():
            if enseignant.charge_crs.user == user:
                dico[user].append(enseignant.name)

    dico = dict(dico)
    #print(mes_planifies)

    for key, value in dico.items():
        #print(key, value)
        for item in value:
            my_identifiant = f"{key} ~ {item}"
            if my_identifiant not in mes_planifies:
                mon_user = Profile.objects.get(user__email=key)
                cours = module.objects.get(name=item)
                Planification.objects.create(
                    professeur=mon_user,
                    matiere=cours,
                    ponderation=''
                )

@shared_task
def update_note_etudiant():
    module_planifie = Planification.objects.all()
    module_concerne = [item for item in module_planifie if item.ponderation != '']
    all_choices_this_module = ''    #-> là je recupère tout les étudiants qui sont inscrist dans ce cours
    mon_mois, session = datetime.now().month, ''

    if 7 <= mon_mois <= 9:
        session = f"Automne {datetime.now().year}"
    if mon_mois == 12 or mon_mois == 1:
        session = f"Hiver {datetime.now().year}"
    if mon_mois == 4 or mon_mois == 5:
        session = f"Ete {datetime.now().year}"

    for item in module_concerne:
        liste_note = []
        #item.ponderation
        #print(item.ponderation)
        for key, value in eval(item.ponderation).items():

            for k, v in value.items():
               liste_note.append({f"{k}~{v}%": ""})

        #print(liste_note)
        all_choices_this_module = Choix_Cours.objects.filter(cours__contains=item.matiere.name)
        print(len(all_choices_this_module))
        for index in all_choices_this_module:
            user = index.user
            cours = item.matiere
            ma_note = Note.objects.get(etudiant=user, module=cours, session=session)
            ma_note.note = f"{ma_note.note}"
            ma_note.note = ast.literal_eval(ma_note.note)
            print(type(ma_note.note))
            if ma_note.note is not None:
                reponse = essai_conformite(liste_note, ma_note.note)
                if not ma_note.note or not reponse:
                    ma_note.note = liste_note
            else:
                ma_note.note = liste_note
            ma_note.save()
        del liste_note[:]
    #print(all_choices_this_module)

@shared_task
def update_planification():
    mes_all_groupe = Create_groupe.objects.all()
    mes_all_groupe = [item for item in mes_all_groupe if item.file_prof == "" or not item.file_prof]
    for index in mes_all_groupe:

        index.concerne = ast.literal_eval(index.concerne)
        interesser = index.concerne[0]
        mes_key = list(interesser.values())
        ma_note = mes_key[0]['file']

        dico_prof = {}
        for item in ma_note:
            for key in item.keys():
                dico_prof[key] = {"file": "", "debut": "", "fin": "", "afficher": "Non"}

        index.file_prof = dico_prof
        index.save()


@shared_task
def update_form():

    add_horaire_to_file()


##cest ici que je vais géré tout mes supprimes