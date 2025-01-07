import ast
import json
import logging
import calendar
import os
import re
from datetime import datetime, date, time, timedelta
from pathlib import Path
from pprint import pprint
from collections import defaultdict, deque

import pytz
from PIL import Image, ImageEnhance
from io import BytesIO

from logging.handlers import RotatingFileHandler

from django.db import transaction
from django.utils import timezone
from django.core.cache import cache
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.http import HttpResponse, FileResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse
from reportlab.lib.pagesizes import letter

from user.models import *

from .models import *
from .fonction import *
from .calendrier import *
from .reglementation import *
from .tasks import update_form
from .settings_all import dico

from all.settings import BASE_DIR

#Je me suis limité au niveau du vue de la note.
# Create your views here.
"""
Important Note : dans les templates de mes chapitres tout ce qui est lié au cours
les views des utilisateurs et professeurs sont gérés par les fichiers html qui 
se trouve dans le dossier cours
##################################################################################
le dossier empty_cours contiendra les vues en cas d'echec de telechargement ou de non respect
des principes de conception
##################################################################################
le fichier fonction.py contient des fonctions supplémentaire utilisés dans mes vues.
##################################################################################
Le système de notation sera toujours à bien revoir.
"""

logger = logging.getLogger("my_logger_cours")
logger.setLevel(logging.DEBUG)

max_bytes = 2000 * 1024 * 1024

handler = RotatingFileHandler('app_cours.log', maxBytes=max_bytes, backupCount=5)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

handler.setFormatter(formatter)

logger.addHandler(handler)


def programme_view(request):  # Pour afficher tout les modules
    all = Programme.objects.all()

    return render(request, 'cours/cours_general/programme.html', {'element': all})


def Module(request, ids):  # module contenu dans un programme
    all_element = module.objects.filter(programme__identifiant=ids)

    return render(request, 'cours/cours_general/module.html', context={'element': all_element})


#je te reviens dans pas longtemps toi aussi
def chapitre_programme(request, ids):  # Pour afficher les chapitres contenu dans un programme
    le_mois, le_year = '', ''
    mon_mois_normal = ""
    mes_mois = {"1": "Janvier", "2": "Février", "3": "Mars", "4": "Avril", "5": "Mai", "6": "Juin",
                "7": "Juillet", "8": "Août", "9": "Septembre", "10": "Octobre", "11": "Novembre", "12": "Decembre"}

    #gerer ici laspect de la securite du site

    #je dois mettre ce bloc dans un try et levé lexception SyntaxError
    if request.user.is_authenticated:
        element = Chapitre.objects.filter(module__identifiant=ids)
        ##Il me faut recupererer mon cours ici:
        mon_cours = module.objects.get(identifiant=ids)

        dico_lesson = {}
        dico_abr = []
        help,mon_calendrier = "", ""

        mon_profile = Profile.objects.get(user__email=request.user.email)
        #ma_note, name, dico_abr = "", "", ""
        liste_interm = []
        for item in element:
            dico_lesson[item] = Lesson.objects.filter(chapitre__name=item)

        if mon_profile.choices == "charge_cours":

            try:
                help = 1    ##-> sa veut dire que le cours à crée des groupes
                if_group_create = Create_groupe.objects.get(matiere=mon_cours)
                create_per_profile = Create_groupe.objects.get(professeur=mon_profile, matiere=mon_cours)

                create_per_profile.file_prof = ast.literal_eval(create_per_profile.file_prof)

                for key, value in create_per_profile.file_prof .items():
                    print(value["file"])
                    if value["file"] == "":
                        dico_abr.append(key)

                #print("le dico_abr est")
                #print(dico_abr)
                #name = [key for key in dico_abr.keys()]
                #print(dico_abr)
            ##le dico abrjedois le rajouter

                if_group_create.concerne = ast.literal_eval(if_group_create.concerne)


                interm = ast.literal_eval(if_group_create.file_prof)

                for key in interm.keys():  # ceci me permet de recupéré directement le champs concerné par le professeur
                        #print(interm[key]["file"])
                        liste_interm.append({key: interm[key]["file"]})

                #print(liste_interm)

                interesser = if_group_create.concerne[0]
                mes_key = list(interesser.values())
                ma_note = mes_key[0]['file']
                date_today = date.today()
                le_mois = date_today.month
                #mon_mois_normal = mes_mois[f"{le_mois}"]
                le_year = date_today.year

                mon_calendriers = Moncalendrier()
                mon_calendrier = mon_calendriers.cal_html(le_year, le_mois)

                #print(ma_note)

                #La couleur bleu indique la date de fin du projet
                #La couleur rouge indique la date de début du projet
                #La couleur desactive indique les dates qu'il a desactivé

                #faudrait là des variables de stock qui me permettront de suivre la passation de mois
                #afin dindiqué les mois cliqué au début et ceux pour la fin

                rouge_general = bleu_general = []

                test_rouge_cache = cache.get('couleur_rouge')
                test_bleu_cache = cache.get('couleur_bleu')

                if not test_rouge_cache:
                    cache.set('couleur_rouge', rouge_general, timeout=120)  #jai un mis un cache de 10mn je dois le diminué

                ##Pour le remettre 5mn
                if not test_bleu_cache:
                    cache.set('couleur_bleu', bleu_general, timeout=120)

                if request.method == "POST" and request.headers.get('x-requested-with') == "XMLHttpRequest":
                    #print(mon_profile)

                    data_post = request.POST

                    print(data_post)
                    #print("**"*20)
                    #print(data_post)
                    #print("**"*20)
                    #print(f"Mon horaire est : {data_post['horaire']}")
                    #print(data_post)
                    ## je dois recupéré les couleurs-rouges et les couleur-bleu

                    #tout ce code sera à mettre dans une fonction
                    reponse_dep = data_post.get('dep', "0")

                    #print("ma-vrai-couleur")

                    #print(data_post['couleur-rouge'])
                    #print(data_post['couleur-bleu'])

                    #print("//"*50)
                    data_post['couleur-rouge'].replace("[\]", '')
                    data_post['couleur-bleu'].replace("[\]", '')
                    mon_rouge = data_post["couleur-rouge"].split(',')
                    mon_bleu = data_post["couleur-bleu"].split(',')

                    test_rouge_cache = cache.get('couleur_rouge')
                    test_rouge_cache.extend(mon_rouge)

                    test_bleu_cache = cache.get('couleur_bleu')
                    test_bleu_cache.extend(mon_bleu)

                    test_rouge_cache = list(set(vide_liste(test_rouge_cache)))
                    test_bleu_cache = list(set(vide_liste(test_bleu_cache)))

                    temp_delete_color_red = data_post['delete-couleur'] #cest ici que je retourne mes elements à supprimé
                    temp_delete_color_red = temp_delete_color_red.replace("[\]", "")
                    temp_delete_color_red = temp_delete_color_red.split(',')

                    temp_delete_color_bleu = data_post['delete-couleur-bleu']
                    temp_delete_color_bleu = temp_delete_color_bleu.replace("[\]", "")
                    temp_delete_color_bleu = temp_delete_color_bleu.split(',')
                    """
                                            if len(test_rouge_cache) > 0:
                        for item in temp_delete_color:
                            if item in test_rouge_cache:
                                print(item)
                    """

                    #ici je crée des nouveaux cache au fure et à mesure que je fais des mises à jours.
                    cache.set('couleur_rouge', test_rouge_cache, 120)
                    cache.set('couleur_bleu', test_bleu_cache, 120)

                    #rouge_general.extend(intermediaire_rouge)

                    le_month = data_post.get('mois', "")
                    #mon_mois_normal = mes_mois[f"{le_month}"]
                    #print(mon_mois_normal)
                    #print(f"Mon mois est: {le_month}")

                    #cest ici que je traite la gestion de suppression de fichier que le user veut enlever
                    element_a_supprimer = data_post.get("consigne-delete")
                    element_a_supprimer = element_a_supprimer.split("-")[0]

                    contenant_modification = []

                    for key in data_post.keys():

                       if key.split("_")[-1] == "date":
                            temp = f"{key.split('_')[0]}_{key.split('_')[1]}"
                            contenant_modification.append(temp)


                    print("Le tableau des contenant")
                    print(contenant_modification)
                    print("--"*10)

                    new_chapitre = []
                    for key, value in data_post.items():
                        if "create-chapitre" in key:

                            new_chapitre.append(value)


                    if len(new_chapitre) != 0:

                        print("Jai un chapitre à crée")
                        mon_url = reverse('cours:chapitre', kwargs={'ids': ids})
                        return JsonResponse({"create_chap": "Creation chapitre", "redirection_chapitre": mon_url})

                    if len(new_chapitre) == 0:
                        print("Vous devez entrez un chapitre!")

                        print("Mon mois est : ", le_month)

                    if element_a_supprimer != "":
                        temporaire_create = create_per_profile.file_prof.get(element_a_supprimer, "")
                        #print(element_a_supprimer)
                        #print(temporaire_create)
                        #print(request.user.email)

                        if temporaire_create != "":
                            mon_dossier_a_suprimer = request.user.email +'-'+element_a_supprimer + '-dep_exam-' + temporaire_create.get("file")
                            dir_final = BASE_DIR / 'mediafiles' / 'creation_tp_prof' / mon_dossier_a_suprimer

                            #print(dir_final)
                            #print(mon_dossier_a_suprimer)
                            temporaire_create = {key: "" for key in temporaire_create.keys()}
                            create_per_profile.file_prof[element_a_supprimer] = temporaire_create
                            dir_final.unlink()
                            create_per_profile.save()
                            #print("Le fichier à bien été supprimé!")

                            mon_url_de_redirection = reverse('cours:chapitre', kwargs={'ids': ids})
                            return JsonResponse({'yes_supprime': 'on ma supprimer', 'redirection': mon_url_de_redirection})
                        #print(temporaire_create)


                    if len(contenant_modification) != 0:
                        print("Traitement du tableau commence")
                    """ 
                    if len(element_a_supprimer) != 0:

                        #ici je dois verifier esque le contenu n'a pas été modifier
                        #directement par le html

                        print("une mise de controle ici")
                        for item in element_a_supprimer:
                            print(item)
                    """

                    if le_mois != "":
                        le_id = data_post.get('rewind-id')
                        le_vrai_id = f"{le_id.split('-')[-1]}-calendrier-{le_id.split('-')[0]}"

                        try:
                            le_month = int(le_month)

                            print(le_month)
                            if reponse_dep != "1":      #reponse_dep me permet de savoir si je fais un dépot ou cest juste un
                                #click dun boutton par hasard que jai faite

                                mon_calendrier = mon_calendriers.cal_html(le_year, le_month)
                                #print(test_bleu_cache)
                                """
                                    print(test_rouge_cache)
                                print("######"*5)
                                print("Mes elements à supprimé sont : ")
                                print(temp_delete_color)
                                """
                                test_rouge_cache = [item for item in test_rouge_cache if item not in temp_delete_color_red]
                                test_bleu_cache = [item for item in test_bleu_cache if item not in temp_delete_color_bleu]
                                cache.set('couleur_rouge', test_rouge_cache, timeout=600)
                                cache.set('couleur_bleu', test_bleu_cache, timeout=600)

                                #le_rouge = cache.get('couleur_rouge')
                                #le_bleu = cache.get('couleur_bleu')
                                #print(mes_mois[f"{le_mois}"])
                                return JsonResponse({'html': mon_calendrier, 'le_vrai_id': le_vrai_id,
                                                     "my_blood": test_rouge_cache, "my_blue": test_bleu_cache})

                            else:

                                le_rouge = cache.get('couleur_rouge')
                                le_bleu = cache.get('couleur_bleu')

                                traitement_date = depot_fichier(le_rouge, le_bleu)

                                try:
                                    date_exact_debut, date_exact_final = traitement_date.verif_logique()

                                    if len(request.FILES) > 0:
                                        print(request.FILES)
                                        print(data_post["horaire"])
                                        reponse_depot = enregistre_tp_venant_de_prof(request.FILES, if_group_create,
                                                                                     request, date_exact_debut, date_exact_final)

                                        if reponse_depot == 1:
                                            cache.delete('couleur_rouge')
                                            cache.delete('couleur_bleu')
                                            mon_url_correct = reverse('cours:chapitre', kwargs={'ids': ids})
                                            return JsonResponse({'url_correct': mon_url_correct})

                                    else:

                                        return JsonResponse({'obli_entrez_fichier': 'oui'})

                                except ValueError:
                                    print("je suis là Mamadou Saidou diallo")

                                except confus_date as e:
                                    cache.delete('couleur_rouge')
                                    cache.delete('couleur_bleu')

                                    print(str(e))
                                    return JsonResponse({'strong_length': 'oui', 'mon_mois': mon_mois_normal})

                                except confus_month as e:
                                    cache.delete('couleur_rouge')
                                    cache.delete('couleur_bleu')
                                    print(e)

                                except depot_vide as e:
                                    cache.delete('couleur_rouge')
                                    cache.delete('couleur_bleu')
                                    return JsonResponse({'not_depot': str(e), 'mon_mois': mon_mois_normal})

                                except confus_day as e:
                                    print(e)
                                    return JsonResponse({'conf_day': 'oui', 'mon_mois': mon_mois_normal})

                                mon_url_correct = reverse('cours:chapitre', kwargs={'ids': ids})
                                return JsonResponse({'mon_url1': mon_url_correct, 'mon_mois': mon_mois_normal})


                        #le except qui est là est donné lorsque j'utilise pas de boutton next ou preview
                        #Ici ce passera une patie de la logique de lajout de document par le professeur
                        except ValueError:  #dans ce cas je vais lutilisé si mon user na pas utilisé de bouton next ou preview

                            print("je suis là")
                            mon_rouge = [item for item in mon_rouge if item != ""]
                            mon_bleu = [item for item in mon_bleu if item != ""]

                            print(mon_rouge)
                            print(mon_bleu)
                            print("----" * 30)

                            try:
                                mon_traitement_date = depot_fichier(mon_rouge, mon_bleu)
                                mon_rouge, mon_bleu = mon_traitement_date.verif_logique()
                                print(data_post["horaire"])
                                if len(request.FILES) > 0:
                                    print("--"*20)
                                    print(request.FILES)
                                    reponse_depot = enregistre_tp_venant_de_prof(request.FILES, if_group_create, request, mon_rouge, mon_bleu)

                                    if reponse_depot == 1:
                                        mon_url_correct = reverse('cours:chapitre', kwargs={'ids': ids})
                                        return JsonResponse({'url_correct': mon_url_correct})
                                    else:
                                        #cela veut juste dire que jai eu une erreur dans lajout de mon fichier tp
                                        pass

                                else:

                                    return JsonResponse({'obli_entrez_fichier': 'oui'})

                            except depot_vide as e:     #cest lerreur qui dois sortir lorsque la personne
                                #nentre pas une date de depot

                                return JsonResponse({'not_depot': str(e), 'mon_mois': mon_mois_normal})

                            except confus_date as e:
                                #cette erreur sera levé lorsque la personne entre deux date de debut ou de fin
                                message = str(e)
                                return JsonResponse({'strong_length': message, 'mon_mois': mon_mois_normal})

                            #jai pas besoin de la loique de confus_month ici
                            except confus_month as e:
                                print(e)

                            except confus_day as e:

                                return JsonResponse({'error_date': str(e), 'mon_mois': mon_mois_normal})

            except Create_groupe.DoesNotExist:
                help = 2    #--> sa veut dire que le cours na pas de groupe crée

        elif mon_profile.choices == "etudiant":
            help = 0
            mon_cours = module.objects.get(identifiant=ids)
            if_group_create = Create_groupe.objects.get(matiere=mon_cours)

            nom_professeur = if_group_create.professeur

            valeur_temp = ast.literal_eval(if_group_create.file_prof)

            liste_a_afficher = help_affichage_pour_aide_td_pour_etudiant(valeur_temp)

            mes_files = [{value: f"{nom_professeur}-{key}-dep_exam-{value}"}for item in liste_a_afficher for key, value in item.items()]
            print("Les files sont : ")
            print(mes_files)
#http://127.0.0.1:8000/cours/readme/creation_tp_prof/koto@gmail.com-dep_exam-nene~50-2-insertion-de-donn%C3%A9es.sql
            return render(request, 'cours/cours_general/chapitre.html',
                          context={'element': element, 'lesson': dico_lesson, "index": help, "ids": ids,
                                   "ma_note": liste_interm, "calendrier": mon_calendrier, "le_mois": le_mois,
                                   "dico_abrs":  mes_files})



        print(mes_mois[f"{le_mois}"])
        print(dico_abr)
        print(liste_interm)
        return render(request, 'cours/cours_general/chapitre.html',
                      context={'element': element, 'lesson': dico_lesson, "index": help, "ids": ids,
                               "ma_note": liste_interm, "calendrier": mon_calendrier, "le_mois": le_mois,
                               'lanne': le_year, 'dico_abr': dico_abr, 'timestamp': int(datetime.now().timestamp()), 'mois_actuel': mes_mois[f"{le_mois}"]})

    else:
        return HttpResponse("hello mamadou")


def traitement_modif_date(request):

    if request.method == "POST":
        print("je suis ici")
        print(request.POST)
        print("--"*20)
    return HttpResponse("<h2>Hello Mamadou Saidou</h2>")


def time_stamp(request):

    return render(request, 'cours/other/time_stamp.html', context={'timestamp': int(datetime.now().timestamp())})



def calendar_view(request, year, month):
    cal = Moncalendrier()
    html_cal = cal.cal_html(int(year), int(month))
    if request.method == "POST":
        month = request.POST.get("month")
        le_year, le_mois = month.split('-')

        #return HttpResponse("hi world,")
        mon_url = reverse('cours:calendar', kwargs={"year": str(le_year), "month": str(le_mois)})
        return redirect(mon_url)
        #return reverse('cours:calendar', kwargs={"year": str(le_year), "month": str(le_mois)})
    else:
        return render(request, 'cours/cours_general/calendar.html', context={'calendar': html_cal, 'year': year, 'month': month})


def lessons_chapitre(request, ids):  ##Pour afficher les lessons contenu dans un chapitre
    lesson = Lesson.objects.filter(chapitre__identifiant__icontains=ids)

    return render(request, 'cours/cours_general/lesson_chapitre.html', context={'lesson': lesson})


#######################################################################################################################
#Sa concerne le professeur


#cette vue est à modifié après ou supprimé
def all_chap_auteur(request, ids):  # Pour tout les chapitres crées par un auteur
    liste_content = []
    context1 = {}
    auteur = Chapitre.objects.filter(auteur__identifiant__icontains=ids)
    for item in auteur:
        if item.module.name in liste_content:
            continue
        else:
            liste_content.append(item.module.name)

    return render(request, 'cours/cours_general/all_chap_auteur.html',
                  context={'auteur': auteur, 'first': liste_content[0]})


##NB, il me reste ici à racommoder le chapitre au programme choisi
def create_chap(request):  ##Pour creer un chapitre par un professeur
    ##NB: il me reste comment donnez la possibilité à un prof de modifier le nom dun chapitre ou de le supprimer
    liste = []
    if request.user.is_authenticated and request.user.profile.choices == "charge_cours":

        name = request.POST.get('name', '')
        email = request.user.email
        auteur = Profile.objects.get(user__email=email)
        mymodule = module.objects.filter(charge_crs=auteur)
        if len(mymodule) > 0:
            if name != '':
                name = name
                try:
                    matiere = request.POST.get('module')  #module de lenseignant
                    matiere = module.objects.get(name=matiere)
                    Chapitre.objects.create(name=name, auteur=auteur, module=matiere)
                    return redirect('cours:chapitre_auteur', ids=auteur.identifiant)
                except:
                    element = Chapitre.objects.get(name=name)
                    print(element.identifiant)
                    return render(request, 'not_respect/chap_exist.html', context={"element": element})
            else:
                return render(request, 'cours/cours_general/create_chap.html',
                              context={'module': mymodule, 'contraint': "Veuillez entrez le nom du chapitre"})
        else:
            return HttpResponse("<h2>Vous navez pas choisi votre module denseignement</h2>")
    return HttpResponse("<h3>veuillez vous connecter à votre compte pour avoir cette permission</h3>")


##Faut aussi tenir compte de la  situation où les formats d'image, de video, et des doc ne sont pas respectés
def create_lesson(request, ids):  #Pour creer une lesson
    chapitre = Chapitre.objects.get(identifiant=ids)
    if request.user.is_authenticated and request.user.profile.choices == "charge_cours":
        if request.method == "POST":
            verifie = ''
            context, context2 = {}, {}
            image_1, pdf_1, video_1 = '', '', ''
            image, pdf, video = 'm.png', 'm.pdf', 'm.mp4'
            name = request.POST.get('name', '')
            description = request.POST.get('description', '')
            if name == '':
                context['name'] = "Entrez le nom de la lesson car il est obligatoire"
            if description == '':
                context['description'] = "Entrez le description de la leçon elle est obligatoire"

            if request.FILES != 0:
                image = request.FILES.get('image')
                if image is None:
                    image = 'empty.png'

                image_1 = str(image)
                pdf = request.FILES.get('pdf')
                if pdf is None:
                    pdf = 'empty.pdf'
                pdf_1 = str(pdf)

                video = request.FILES.get('video')
                if video is None:
                    video = 'empty.mp4'
                video_1 = str(video)
                verifie = file_verify(image_1, video_1, pdf_1)
                context2 = verifie.general()
                for keys, value in context2.items():
                    context[keys] = value

            #print(len(context))
            if len(context) > 0:
                return render(request, 'cours/cours_general/create_lesson.html', context=context)

            else:

                element = Profile.objects.get(user__email=request.user.email)
                last = Chapitre.objects.last()
                Lesson.objects.create(auteur=element, chapitre=chapitre, name=name, description=description,
                                      image_lesson=image, pdf_lesson=pdf, video_lesson=video)
                return redirect(request.path)
            return redirect(request.path)

        else:
            return render(request, 'cours/cours_general/create_lesson.html')

    else:
        return HttpResponse(
            "<h2>Vous navez pas droit de crée une lesson ou veuillez vous connectez svp.</h2>")


#Pour lire une lesson
#Mais en tenant compte aussi de la succession des lessons genre en passant au suivant ou en revenant en arrière.
#pdf de la lesson dois contenir dans une page unique pour voir lentiereté


def load_lesson(request, ids):
    element = Lesson.objects.get(identifiant=ids)
    title = element.name
    description = element.description
    try:
        video = element.video_lesson.url
        pdf = element.pdf_lesson.url
        print(video)
        print(pdf)
        if video != '/media/empty.mp4':

            print(element.video_lesson.url)
            return render(request, 'cours/cours_general/load_lesson_with_video.html',
                          context={'title': element.name, 'description': element.description, 'video': video})
        else:
            return render(request, 'cours/cours_general/load_lesson.html',
                          context={'title': title, 'description': description})

    except:
        print('La video de ce cours pas disponible')
    return render(request, 'cours/cours_general/load_lesson.html', context={'title': title, 'description': description})


#Remarque pour cette vue on il manque la redirection pour la lecture dela page html
#when user click on the pdf icon


def load_the_lesson_in_chapitre(request):
    return render(request, 'cours/cours_general/load_lesson_with_video.html')


##Vue pour l'espace de chaque membre

#Pas achevé cette vue

def load_chapter(request):
    pass


#Pour afficher les notes inscrits dans un professeur
def affiche_etudiant(request, matiere):
    all_cours = Choix_Cours.objects.all()
    liste_etudiant = []
    for item in all_cours:
        item.cours = eval(item.cours)
        for element in item.cours:
            if element == matiere:
                liste_etudiant.append(item.user.user.email)

    return render(request, 'cours/prof/affiche_etudiant.html', context={'etudiant': liste_etudiant})


def planifie_notation(request, crs):
    professeur = Profile.objects.get(user__email=request.user.email)
    mon_crs = module.objects.get(name=crs)
    element = Planification.objects.get(professeur=professeur, matiere=mon_crs)
    if element.ponderation != '':
        return HttpResponse("Ce cours est déjà pondéré")

    else:

        if mon_crs.charge_crs.user.email == request.user.email:
            liste, liste_erreur = [], []
            quota = defaultdict(list)
            somme = 0
            if request.method == 'POST' and request.headers.get('x-requested-with') == "XMLHttpRequest":
                data = request.POST
                for key, value in data.items():
                    if key != 'csrfmiddlewaretoken':
                        name, index = key.split("~")

                        if name.startswith('n'):
                            quota[index].append({"Nom": value})
                        else:
                            quota[index].append({"ponderation": value})

                quota = dict(quota)

                reponse = verifi_dico_in_planifie(quota)
                liste_content = reponse.inverse_manque()
                reponse = reponse.recherche_manque()
                #print(reponse)
                if reponse != -1:
                    if len(liste_content) > 0:

                        return JsonResponse({"mon_erreur": reponse, 'content': liste_content})
                    else:

                        return JsonResponse({"mon_erreur": reponse.recherche_manque()})

                else:
                    somme = 0
                    liste_quota, liste_erreur = [], []
                    quota1 = {}
                    for k, v in quota.items():

                        try:
                            somme += int(v[1]['ponderation'])
                        except ValueError:
                            liste_erreur.append(k)

                        quota1[k.strip()] = {v[0]['Nom'].strip(): v[1]['ponderation'].strip()}
                        liste_quota.append({v[0]['Nom']: v[1]['ponderation']})

                    if len(liste_erreur) > 0:
                        logger.critical(f"{request.user.email} dossier à suivre, il a tenté de modifié le type dans la plannification")
                        return JsonResponse({"big_error": "Vous devrez accepter notre fomulaire comme telle"})

                    else:
                        if somme != 100:
                            return JsonResponse({"mon_erreur": "La somme de vos ponderation doit etre de 100"})
                        else:
                            print(quota1)
                            print(liste_quota)
                            element.ponderation = quota1
                            element.save()
                            #je dois recupéré tout les elèves de ce cours pour leur donné une forme de note, ceci ce fera dans mon task.py
                            mon_url = reverse("cours:ponde", kwargs={'mod': crs})
                            return JsonResponse({"mon_url": mon_url})
                    print(liste_quota)
                    print(somme)
                    return JsonResponse({"not_error": "Pas derreur"})
            #une fonction de controle si mon dico est vraiment rempli -> verifi_dico_in_planfie


    return render(request, 'cours/prof/planifie_note.html', context={'cours': crs})


def update_planification(request):
    pass


def give_note_max(request, mod):

    try:
        verifie = Planification.objects.get(matiere__name=mod)
        liste, dico, error_type = [], [], []
        professeur = get_object_or_404(Profile, user__email=request.user.email)
        mon_crs = get_object_or_404(module, name=mod)
        #print(professeur)
        majoration = Planification.objects.get(professeur=professeur, matiere=mon_crs)
        mon_dico = eval(majoration.ponderation)
        mon_dico = decortique(mon_dico)  # =>justificatif donné dans le fichier fonction.py

        if request.method == 'POST' and request.headers.get("x-requested-with") == "XMLHttpRequest":
            data = request.POST

            for key, value in data.items():
                if key != 'csrfmiddlewaretoken':

                    if value == '':
                        dico.append(key)
                    else:
                        try:
                            liste.append(value)
                            note_maxi = int(value)

                        except ValueError:
                            error_type.append(key)

            if len(dico) > 0:
                print(dico[0])
                return JsonResponse({"mon_erreur": dico})
            else:

                if len(error_type) > 0:
                    logger.critical(f"{request.user.email}, il a tenté de changé un type au niveau de donner une note maxi des modules.")
                    return JsonResponse({"error_type": "Le type de linput à été changé!"})
                else:
                    majoration.majoration = liste
                    majoration.save()
                    mon_url = reverse('cours:note_etudiant', kwargs={'mat': mod})
                    return JsonResponse({"mon_url": mon_url})
        return render(request, 'cours/prof/majoration.html', context={'mes_exam': mon_dico, 'nom': mod})

    except Planification.DoesNotExist:
        return HttpResponse("<h2>Votre matière nest pas planifié dabord pour donnez des notes! </h2>")


def update_note_max(request, mod):
    pass

def noter_etudiant(request, mat):
    verifie = Planification.objects.filter(matiere__name__contains=mat)
    if verifie:
        dico_note, liste_etudiant, ponderation_finale, liste_ponderation2 = {}, [], {}, []
        professeur = Profile.objects.get(user__email=request.user.email)
        mon_crs = module.objects.get(name=mat)
        element = Planification.objects.filter(professeur=professeur, matiere=mon_crs).first()

        majoration = Planification.objects.filter(professeur=professeur, matiere=mon_crs).values_list(
            'majoration').first()
        majoration = list(majoration)

        if majoration[0] is None:  # Cette condition permet de donner une note maximale dans les examesn
            print(element.ponderation)
            print("Pas de majoration pour le moment")
            return redirect('cours:ponde', mod=mat)

        if element:
            liste_ponderation, liste_ponderation2 = [], []

            element.ponderation = eval(element.ponderation)

            for ponderation in element.ponderation.values():
                for k, v in ponderation.items():
                    liste_ponderation.append(
                        f"{k}~{v}%")  # Liste ponderation renvoie juste la ponderation avec son repartition
                    liste_ponderation2.append(v)  # Celle ci renvoie juste le pourcentage de chaque examen

            ponderation_finale = {key: value for key, value in
                                  zip(liste_ponderation, eval(majoration[0]))}  # Celle ci renvoie juste chaque examen
            # son pourcentage et sa note maximale

            for item in ponderation_finale.keys():
                print(item)

            all_cours = Choix_Cours.objects.all()
            liste_etudiant = Choix_Cours.objects.filter(cours__contains=mat).values_list('user__user__email', flat=True)
            liste_etudiant_note = Note.objects.filter(module__name__contains=mat).values_list('etudiant__user__email',
                                                                                              'note')

            #print(liste_etudiant_note)
            # dico_note = {k: v for k, v in liste_etudiant_note}
            for k, v in liste_etudiant_note:

                    dico_note[k] = eval(v)

            print("mondico note est")
            print(dico_note)
        if request.method == 'POST' and request.headers.get('x-requested-with') == "XMLHttpRequest":
            error = []
            dict_bd = defaultdict(list)
            liste_result = []
            data_majoration = {}
            data2 = defaultdict(list)
            data = request.POST
            data = dict(data)

            for key, valeur in data.items():
                if key != 'csrfmiddlewaretoken':
                    #print(key, valeur)
                    email_etudiant, exam = key.split()

                    if valeur[0]:
                        if float(ponderation_finale[exam]) < float(valeur[0]):
                            error.append(key)

                        else:
                            dict_bd[email_etudiant].append({exam: valeur[0]})

            for key, value in dict_bd.items():

                for item in value:
                    if item != '':
                        print(f"{key} contient des choses")

            if len(error) > 0:
                return JsonResponse({"big_error": "Attention de ne pas dépassé la note maximale"})
            else:
                mon_mois = datetime.now().month
                session = ''
                if 7 <= mon_mois <= 9:
                    session = f"Automne {datetime.now().year}"
                if mon_mois == 12 or mon_mois == 1:
                    session = f"Hiver {datetime.now().year}"
                if mon_mois == 4 or mon_mois == 5:
                    session = f"Ete {datetime.now().year}"
                for key, value in dict_bd.items():
                    mon_etudiant = Profile.objects.get(user__email=key)
                    ma_note = Note.objects.get(etudiant=mon_etudiant, session=session, module=mon_crs)
                    liste1 = eval(ma_note.note)
                    print(mon_etudiant)
                    help_note = regroupe_synchronise(liste1, value)
                    ma_note.note = str(help_note)
                    print(ma_note.note)
                    ma_note.save()

                mon_url = reverse('cours:note_etudiant', kwargs={"mat": mat})
                return JsonResponse({"validate": mon_url})

        else:
            return render(request, 'cours/prof/noter_etudiant.html',
                      context={'etudiant': liste_etudiant, 'ponde': ponderation_finale, 'note': dico_note,
                               'cours': mat})
    else:
        return HttpResponse("<h2>Cette matière n'a pas été pondéré dabord pour donner une note </h2>")

def update_note_etudiant(request):
    pass


def vue_user(request, domaine):
    #pour le charge de cours à revoir poour optimiser le code
    if not request.user.is_authenticated:
        return redirect('user:connexion')
    if domaine == 'charge_cours':
        redirect_url = cache.get('saidou')

        if not redirect_url:
            print("je nai rien pour le moment")

        all_cours = module.objects.filter(charge_crs__user__email=request.user.email)

        ma_redirection = reverse('user:connexion')


        ma_redirection1 = reverse('cours:chapitre', kwargs={'ids': 'gDJ-Element de Programmation'})
        mon_cache_redirect = cache.get('redirection1')
        if not mon_cache_redirect:
            cache.set('redirection1', mon_cache_redirect, timeout=30000)
        else:
            ma_redirection1 = mon_cache_redirect
        return render(request, 'cours/prof/first_vue_prof.html', context={'courses': all_cours, 'redirect': ma_redirection1})

    elif domaine == "charger_financier":

        #Gestion des erreurs qui reste !
        all_paiement = Payer.objects.all()
        context_renseignement = defaultdict(list)

        for item in all_paiement:
            email = item.identifiant.split('+')[0].strip()
            session = item.identifiant.split('+')[1].strip()
            matiere = item.identifiant.split('+')[-1].strip()
            context_renseignement[matiere].append({f"{email}": {session: item.montant}})

        context_renseignement = dict(
            context_renseignement)  #ON a retourné sous forme de dict pour pouvoir faire une bonne affichage dans ma page html

        if request.method == "POST":
            data = request.POST
            for key, value in data.items():
                if key != 'csrfmiddlewaretoken':
                    concerne, session, matiere = key.split('+')
                    concerne = Profile.objects.get(user__email=concerne.strip())
                    session = session.strip()
                    matiere = matiere.strip()

                    matiere = module.objects.get(name=matiere)
                    my_id = f"{concerne} + {session} + {matiere}"
                    element = Payer.objects.get(identifiant=my_id)
                    if element.montant >= float(value):
                        element.montant = element.montant - eval(value)
                        element.save()

            print(data)
            return redirect(request.path)

        return render(request, 'cours/vue_etudiant/vu_charger_financier.html', context={'note': context_renseignement})

    elif domaine == "etudiant":

        liste = []
        context_cours = {}
        mon_etudiant = Profile.objects.get(user__email=request.user.email)
        all_cours = Choix_Cours.objects.filter(user=mon_etudiant)
        for item in all_cours:
            item.cours = eval(item.cours)
            for index in item.cours:
                matiere = module.objects.get(name=index)
                context_cours[matiere] = Chapitre.objects.filter(module__name=index)
                liste.append(matiere)

        print(liste)

        return render(request, 'cours/vue_etudiant/first_vue.html',
                      context={'liste': liste, 'chapitre': context_cours, 'etudiant': request.user.email})
    return render(request, 'cours/cours_vue_user.html', context={'element': domaine})


def releve_note(request, ids):
    try:

        choix = Profile.objects.get(user__email=ids)

        if choix.choices == "etudiant":
            validate_email(ids)
            info_etudiant = {}
            moyenne = 0
            mes_notes = Note.objects.filter(etudiant__user__email="saidessai466@gmail.com")

            info_etudiant = {item.module: eval(item.moyenne) for item in mes_notes}

            moyenne = round(sum(info_etudiant.values()) / len(info_etudiant), 5)

            return render(request, 'cours/vue_etudiant/releve_note.html',
                          context={"info": info_etudiant, "moyenne": moyenne, "email": request.user.email})

        else:
            return HttpResponse("Vous navez pas de releve de note à verifier")

    except Profile.DoesNotExist:
        return HttpResponse("Ce profile nexiste pas!")

    except ValidationError:
        return HttpResponse("Entrez un mail valide!")


def serve_pdf(request, name):
    pdf_path = os.path.join(settings.MEDIA_ROOT, name)
    #pdf_path = os.path.join(pdf_path, name)
    if not os.path.exists(pdf_path):
        return HttpResponse("Le fichier PDF n'existe pas.", content_type='text/plain')
    return FileResponse(open(pdf_path, 'rb'), content_type='application/pdf')


def detail_only_note(request, email, name):
    try:
        mon_user = Profile.objects.get(user__email=request.user.email)
        print(mon_user.choices)
        matiere = name
        etudiant_email = email

        try:
            #Pour recuperer la note de letudiant Problematique letudiant, qui aura redouble en ajoutant la session
            matieres = Planification.objects.get(matiere__name=matiere)
            note_etudiant = Note.objects.get(
                identifiant=f"{Profile.objects.get(user__email=etudiant_email)} {module.objects.get(name=matiere)}")
            #print(note_etudiant.note)
            #print(note_etudiant.moyenne)
            liste_data = []

            liste = [[k, v] for dico in eval(note_etudiant.note) for k, v in dico.items()]
            liste = deque(liste)
            liste.appendleft(['Examen', 'Note'])
            liste.append(["Moyenne", note_etudiant.moyenne])
            #print(liste)
            liste = list(liste)
            pdf_path = create_pdf(name, liste)

            return render(request, 'cours/vue_etudiant/only_note.html', context={"pdf_path": pdf_path, "name": name})

        except Planification.DoesNotExist:
            return HttpResponse("le quota de cette matière nest pas donné encore")
        except Note.DoesNotExist:
            return HttpResponse("Letudiant na pas de note dans cette matiere dabord!")

    except Profile.DoesNotExist:
        return HttpResponse("Vous navez pas de compte!")  #Code à rectifier

    name = f"{email}~{name}.pdf"
    return render(request, 'cours/vue_etudiant/only_note.html', {"name": name})


#Pause de développement pour finir d'abord avec le choix de cours pour les étudiants.
#######################################################################################################################


#detail_note prof
def detail_note(request):
    pass


def calcul_somme(mon_dict: dict) -> float:
    somme = 0
    for key, value in mon_dict.items():
        somme += float(value.split('$')[0])

    return somme


def detail_paiement(request, etud):
    if request.user.is_authenticated and request.user.profile.choices == 'etudiant':

        mes_cours = Choix_Cours.objects.filter(user__user__email=etud)
        print(mes_cours)
        context_cours = {}
        for item in mes_cours:
            #item.cours = eval(item.cours)
            for index in eval(item.cours):
                price = module.objects.get(name=index).price
                context_cours[index] = price

        context_cours['frais_document'] = '120$'
        context_cours['assurance'] = '300$'
        context_cours['frais_sup'] = '200$'
        context_cours['somme'] = f'{calcul_somme(context_cours)}$'
        for key, value in context_cours.items():
            print(key, value)
        return render(request, 'cours/vue_etudiant/detail_paiement.html', context={'cours': context_cours})

    else:
        return HttpResponse("<h3>Vous navez pas droit à cette vue </h3>")


"""
    Pour l'etudiant:
    ~Cette partie contiendra le choix de son programme
    ~le choix de ses modules
    ~Et aussi penser à configurer la page pour que chaque personne voit ses choix
"""


#Dans le choix des cours ou des modules à étudiés en fonction de son domaine lutilisateur
#choose courses personnally ou en tenant compte de son cycle


@transaction.atomic
def choix_cours(request):
    liste1_contient, liste1_not = [], []
    #print(request.user.email)
    if request.user.is_authenticated and request.user.profile.choices == "etudiant":
        #print(request.user.profile.domaine_programme)
        all_choices = []  #recupéré tout les choix d'un utilisateur
        val1 = ''
        context_modules = {}
        domaine = request.user.profile.domaine_programme.title()

        module_choices_name = module.objects.filter(
            programme__name=domaine)  #il va me retourner le nom des modules en formats chaine de caractère dans un type django.models.query.set
        module_choices_name = [item.name for item in module_choices_name]  #j'ai converti le type de sorti en class list
        email = request.user.email  #Recuperer le mail de l'utilisateur pour mieux chercher son profil
        all_element = Choix_Cours.objects.filter(
            user__user__email=email)  #Pour retrouver tout les choix de mon  utilisateur dans ma BD

        for item in all_element:  #le all_element est une liste qui contient que des strings
            item.cours = eval(item.cours)  #j'evalue les items de cet all_element pour les convertir facilement en liste
            all_choices.extend(item.cours)  #à chaque item retrouvé  je letend dans ma dictionnaire que javais déclaré

        all_choices = list(
            set(all_choices))  #Pour chaque element  de ma liste je le set pour eviter la repetition, qui va retourner un set puis le list pour renvoyer une liste

        for item in module_choices_name:
            if item in all_choices:
                liste1_contient.append(item)
            else:
                liste1_not.append(item)

        mon_url = reverse("cours:choix_cours")
        if request.method == "POST" and request.headers.get('x-requested-with') == "XMLHttpRequest":
            val1 = request.POST.getlist('option')
            val2 = request.POST.get('recupere')
            print("Mon val1 est: ")
            print(val1)
            print("$$$"*30)
            val2 = val2.split("\n")  #Je recupere tout mes éléments à modifier
            val2 = [item.replace('\r', '') for item in val2]  #Les elements sont ensuite classé dans une liste
            del val2[-1]  #je supprime le dernier element de ma liste car il est vide ''

            etudiant_principal = Profile.objects.get(user__email=email)
            print(etudiant_principal.choices)
            if len(val1) == 0 and len(val2) == 0:
                context_modules['module_choices_name'] = liste1_not
                context_modules['not_choice'] = liste1_contient
                context_modules['error'] = "Vous devrez donnez au moins un choix"
                return JsonResponse({"error": "Vous devez donnez au moins un choix"})
                #return render(request, 'cours/cours_general/choix_cours.html', context=context_modules)

            else:
                dict_union = {}
                le_mois = datetime.now().month
                year = datetime.now().year
                session = ""
                if 7 <= le_mois <= 9:
                    session = f"Automne {year}"

                if le_mois == 1 or le_mois == 12:
                    session = f"Hiver {year}"

                if le_mois == 4 or le_mois == 5:
                    session = f"Été {year}"

                matiere, montant_prix = '', ''
                #etudiant_principal = Profile.objects.get(user__user__email=email)
                backup, mon_element = {}, ""
                all_historique = Historique.objects.all().values("identifiant")
                all_historique = [value for item in all_historique for key, value in item.items()]
                all_historique = list(set(all_historique))
                le_mois = datetime.now().month
                print(le_mois)
                print(datetime.now().year)
                for index in all_historique:
                    dates, user, code = index.split("~")
                    if user == request.user.email:
                        mon_elements = Historique.objects.get(identifiant=index)
                        mon_element = mon_elements.backup
                        backup = help_me(mon_element)
                        print("mon val2 est")
                        print(val2)
                        print("$$"*30)

                        if len(val2) > 0:
                            for item in val2:

                                cours = item.split('~')[-1]
                                mon_module = module.objects.get(name=cours)
                                backup.save_remove("Choix_Cours", cours)

                                ma_note = Note.objects.filter(module=mon_module, etudiant=etudiant_principal, session=session).first()
                                #Je supprime la note ici
                                if ma_note:
                                    ma_note.delete()

                            #print(ma_note)
                                mes_paiements = Payer.objects.filter(profile=etudiant_principal, modules=mon_module,
                                                              session=session).first()
                                if mes_paiements:
                                    mes_paiements.delete()

                            mes_elements = Choix_Cours.objects.filter(user=etudiant_principal)
                            for content in mes_elements:
                                content.cours = eval(content.cours)
                                print(content.cours)
                                reponse = aide_recherche(content.cours, cours)
                                if reponse != -1:  # Ici cest pour la suppression dun choix de cours
                                    del content.cours[reponse]
                                        # si je supprime la matiere si le champs cours
                                        # contient encore dautre cours si oui laisser les autres en vie
                                    content.save()
                                    break

                                        # La continuité de ce qui suit est dans mon tasks.py
                                        # content.delete()    #si non supprimer directement meme lidentifiant
                                        # print(f"Le {cours} est dans le {content.identifiant}")

                                        # print(mes_elements)
                            backup.save_remove("Note", cours)
                            backup.save_remove("Payer", cours)

                                        # print(mon_element)
                            mon_elements.save()

                        if len(val1) > 0:
                            for item in val1:
                                matiere = module.objects.get(name=item)
                                montant_prix = matiere.price.split("$")[0]

                                current_month = datetime.now().month
                                current_year = datetime.now().year
                                professeur = matiere.charge_crs.user.email
                                professeur = Profile.objects.get(user__email=professeur)

                                Note.objects.create(professeur=professeur, etudiant=etudiant_principal,
                                        module=matiere)  #Cette ligne permet de créer une note automatique pour letudiant
                                Payer.objects.create(modules=matiere, profile=etudiant_principal, montant=montant_prix,
                                         session=session)

                            Choix_Cours.objects.create(user=etudiant_principal, cours=val1, groupe=1)
                            #Lenvoyer un mail de son choix de cours
                #je dois crée sa facture de paiement ici aussi

                        if (len(val1) > 0 and len(val2) > 0) or (len(val1) == 0 and len(val2) > 0) or (len(val2) == 0 and len(val1) > 0):
                            return JsonResponse({"mon_url": mon_url})

            return redirect(request.path)
        return render(request, 'cours/cours_general/choix_cours.html',
                      context={'module_choices_name': liste1_not, 'not_choice': liste1_contient})

        return HttpResponse("<h1>Vous ne pouvez pas faire de choix de cours car vous n'êtes pas etudiant</h1>")
    else:
        return redirect('user:connexion')


##dans cette vue je dois penser à remettre le try pour les etudiants non connectés
def creation_group(request, crs):
    user = Profile.objects.all()

    user2 = Profile.objects.get(user__email=request.user.email)

    matiere = crs  #Elle sera à supprimé par après

    mon_module = module.objects.get(name=crs)  #Je recupère ma vrai matière

    #Jai juste à le mettre dans un try except
    create_concerne = Create_groupe.objects.filter(professeur=user2).filter(matiere=mon_module)

    les_concerne = Choix_Cours.objects.filter(cours__contains=matiere).values("user__user__email") #Là je vois que si mon etudiant à dejà faire ce choix de cours!

    #print(les_concerne)
    #mes_etudiants = [value for item in les_concerne for key, value in item.items()]

    if user2.choices == "etudiant":
        le_cours = crs

        mes_cours = Choix_Cours.objects.filter(
            user__user__email=request.user.email)  #Là je recupère les choix de cours de mon utilisateur
        #ma_matiere = module.objects.get(name="Element de Programmation")
        my_all_group = Create_groupe.objects.all().values("matiere__name")
        my_all_group = [value for item in my_all_group for key, value in
                        item.items()]  #là je recupère toute les matières qui demandes des creations de groupe

        if le_cours in my_all_group:  #Là je vois juste que si le cours possède des demandes de groupe

            groupe_concerne = Create_groupe.objects.get(matiere=mon_module)
            #print(groupe_concerne.concerne)
            groupe_concerne.concerne = eval(groupe_concerne.concerne)

            reponse = gere_note_groupe(groupe_concerne.concerne).rechercher_etudiant(request.user.email)

            if reponse != -1:  #verif_display = -1 veut juste dire que  letudiant à un groupe
                verif_display, index = gere_note_groupe(groupe_concerne.concerne).rechercher_etudiant(request.user.email)
                gestions = gere_note_groupe(groupe_concerne.concerne)
                mes_limites = gestions.place_limite_and_available()
                print(mes_limites)
                return render(request, "cours/vue_etudiant/affiche_only_group_etud.html",
                              context={"all": groupe_concerne.concerne, 'code': verif_display, "limite": mes_limites})

            else:  #Le else qui est là cest quand l'etudiant na pas de groupe d'abord
                ajout_total = 0
                gestions = gere_note_groupe(groupe_concerne.concerne)
                #verif_display, index = gere_note_groupe(groupe_concerne.concerne).rechercher_etudiant(
                    #request.user.email)
                if request.method == "POST" and request.headers.get("x-requested-with") == "XMLHttpRequest":
                    data = request.POST

                    if len(data) == 2:
                        for key in data:
                            if key != 'csrfmiddlewaretoken':

                                gestions.ajout_etudiant(int(key), request.user.email)

                        groupe_concerne.save()
                        mon_url = reverse('cours:create_group', kwargs={"crs": crs})
                        return JsonResponse({"mon_url": mon_url})
                    else:
                        return JsonResponse({"valeur": "Vous ne pouvez faire partir que dun seul groupe à la fois!"})
                limite = gestions.place_limite_and_available()

                return render(request, "cours/vue_etudiant/affiche_only_group_etud.html",
                              context={"all": groupe_concerne.concerne, "code": reponse, "limite": limite, "crs": crs})

        else:  #En cas si le cours n'as pas une requête de création de groupe dabord
            return HttpResponse("Ce groupe na pas de choix dami à faire dabord!")
        #return render(request, 'cours/vue_etudiant/affiche_only_group_etud.html')

    elif user2.choices == "charge_cours":
        if len(create_concerne) > 0:
            help_remove = ""
            help_update = defaultdict(list)
            create_concerne[0].concerne = eval(create_concerne[0].concerne)
            ################################################celui là est pour ajouter des information au concernés###################
            if request.method == "POST" and request.headers.get("x-requested-with") == "XMLHttpRequest":
                data = dict(request.POST)
                help_get_data = defaultdict(
                    list)  #Ce dico va juste me permettre de de recupéré mes élments à ajouter dans ma liste
                help_extend_get_data = defaultdict(
                    list)  #Ce dico sera pour moi le dico qui va me permettre de recupéré mes éléments à étendre
                repere = 0
                temporary_help = gere_note_groupe(create_concerne[0].concerne)
                for key, value in data.items():
                    if key != 'csrfmiddlewaretoken':

                        if not key.startswith("r") and key.startswith("n"):     #->ici pour mes données ordinaires genres normale
                            name, index = key.split('~')
                            for valeur in value:
                                if valeur != "":
                                    help_get_data[index].append(valeur)

                        elif key == "remove":   #->ICI pour mes données à supprimé
                            value = value[0]

                            help_remove = value.split(',')
                            del help_remove[-1] #->celui là me permet de supprimer le dernier element de ma liste car elle est vide
                            help_remove = list(set(help_remove))

                        elif key.startswith("ajoute"):   #->ici pour mes données dont les cases ont été vidés puis renvoyé
                            nom, groupe = key.split('-')
                            help_update[groupe].append(value)

                        else:           #->ici pour mes données qui vont dépassé la limite qui était prévu
                            name, index = key.split('~')

                            for valeur in value:
                                help_extend_get_data[index].extend(valeur)

                help_update = {key: value[0] for key, value in help_update.items()}

                for key, value in help_update.items():
                    help_update[key] = [item for item in value if item != ""]

                help_get_data = dict(help_get_data)
                help_extend_get_data = dict(help_extend_get_data)

                try:

                    if len(help_get_data) > 0:
                        for key, value in help_get_data.items():

                            for index in value:
                                temporary_help.ajout_etudiant(int(key), index)  #--> cest ici que jajoute mon étudiant

                    ##---> cest ici aussi que je dois supprimé mes étudiants coché

                    if len(help_remove) > 0:
                        help_remove = [item.replace("remove", "") for item in help_remove]
                        for item in help_remove:
                            print(item)
                            temporary_help.supprimer_etudiant(item)

                    if len(help_extend_get_data) > 0:
                        for key, value in help_extend_get_data.items():
                            temporary_help.rajout_longueur_etudiant(int(key), list(value))

                    ## --> ici est pour enregistrer les modifications des données pur les enregistrés encore

                    if len(help_update) > 0:
                        for key, value in help_update.items():
                            if len(value) > 0:
                                for content in value:
                                    print(type(key), content)
                                    temporary_help.ajout_etudiant(int(key), content)

                except Etudiant_Exist as e:
                    erreur = str(e)
                    print(erreur)
                    erreur = erreur.split(' ')[-1]
                    print(erreur)
                    return JsonResponse({"erreur": "Message derreur", "errno": erreur})
                    repere = 1

                if repere == 0:
                    create_concerne[0].concerne = create_concerne[0].concerne
                    #print(create_concerne[0].concerne)
                    create_concerne[0].save()
                    mon_url = reverse("cours:create_group", kwargs={"crs": crs})
                    return JsonResponse({"Confirmation": "Votre étudiant à bien été enregistré", "mon_url": mon_url})

            return render(request, 'cours/prof/affiche_only_group_prof.html',
                          context={"mes_elements": create_concerne[0].concerne, "crs": crs})

        else:  #Cest ici que je fais la création de mon groupe
            mes_planifier = Planification.objects.get(matiere=mon_module)
            ###code a modifier a partir dici
            recap = []
            try:
                for key, value in eval(mes_planifier.ponderation).items():
                    for k, v in value.items():
                        recap.append(f"{k}~{v}")

            except SyntaxError:
                return HttpResponse("Ce cours n'est pas planifié dabord!")

            #########################################################cest ici ce fait la création du groupe######################################
            if request.method == "POST" and request.headers.get("x-requested-with") == "XMLHttpRequest":
                nb = ""  # nbre de personne
                nb_groupe = ""  # nbre de groupe
                data = request.POST
                short_list = ["csrfmiddlewaretoken", "name", "nb_chap"]
                liste_exam = []
                for key, value in data.items():
                    if key not in short_list:
                        liste_exam.append(key)

                nb = data.get("name", "")
                nb_groupe = data.get("nb_chap", "")
                print(len(liste_exam))
                try:
                    nb = int(nb)
                    nb_groupe = int(nb_groupe)
                except ValueError:
                    message_error = "Entrez le bon type svp"
                    return JsonResponse({"error": message_error})

                if nb_groupe > int(len(user)) / 2:
                    return JsonResponse({"attention": "Verifié bien le nombre de personne par groupe"})

                elif nb_groupe * nb > len(user):
                    return JsonResponse(
                        {"error_nbre": "Le nombre de tout les etudiants par groupe doit pas depasser le nmbre total"})

                else:

                    if len(liste_exam) > 0:
                        concerne = []
                        etudiant = ["" for _ in range(nb + 1)]
                        file = [{item: ""} for item in liste_exam]
                        for i in range(nb_groupe):
                            concerne.append({i: {"ETUDIANT": etudiant, "Note": [{item: ""} for item in liste_exam],
                                                 "file": file, "limit": int(nb)}})

                        try:

                            Create_groupe.objects.create(professeur=user2, matiere=mon_module, concerne=str(concerne))
                            mon_url = reverse("cours:create_group", kwargs={"crs": crs})
                            return JsonResponse({"contenu": "Informations bien reçu!", "mon_url": mon_url})

                        except Planification.DoesNotExist:
                            return HttpResponse("Votre matière n'est pas modifié dabord!")

                    else:
                        return JsonResponse({"exam": "Vous devez choisir votre examen svp et cest obligé!"})

            return render(request, 'cours/prof/group_create.html',
                          context={"mes_user": user, "longueur": len(user), "recap": recap, "crs": crs})

    else:
        return HttpResponse("CE COURS NA PAS DE GROUPE POUR LE MOMENT!")

def update_creation_groupe(request):
    pass

def ajout_note_groupe(request):
    #return render(request, "")

    return render(request, "cours/prof/affiche_only_group_prof.html")


#cette fonction est à réecrie à ne pas oublié
def ajout_etudiant(request, matiere):
    if request.user.is_authenticated:

        mon_module = module.objects.get(name=matiere)
        if_exist_in_groupe = Create_groupe.objects.filter(matiere=mon_module)

        if len(if_exist_in_groupe) > 0:
            mon_concerne = if_exist_in_groupe[0]
            mon_concerne.concerne = eval(mon_concerne.concerne)

            return render(request, "cours/prof/affiche_only_group_prof.html",
                          context={"mes_elements": mon_concerne.concerne})

        return render(request, "cours/prof/affiche_only_group_prof.html")

    else:
        return redirect("user:connexion")


#Il faut que je rajoute mon examen ici
def ajout_work_groupe_per_etudiant(request, matiere, exam):
    my_element = Profile.objects.get(user__email=request.user.email)

    if request.user.is_authenticated and my_element.choices == "etudiant":
        pass
        try:
            mon_pdf, ajout = "", 0
            mon_module = module.objects.get(name=matiere)
            mon_module = Create_groupe.objects.get(matiere=mon_module)

            mon_module.concerne = eval(mon_module.concerne)
            print("--"*30)
            temp_file_prof = ast.literal_eval(mon_module.file_prof)

            print("Le file du  prof est: ")
            date_fin = temp_file_prof[exam]["fin"]
            horaire_fin = temp_file_prof[exam]["horaire"]
            print(horaire_fin)
            date_fin = date_fin.split('-')
            date_fin.reverse()
            if horaire_fin != "":
                date_fin = f"{'-'.join(date_fin)}-{horaire_fin}"
            else:
                date_fin = '-'.join(date_fin)

            gere = gere_note_groupe(mon_module.concerne)
            reponse, indexis = gere.rechercher_etudiant(request.user.email)
            notation_temporaire = gere.estnote(exam, request.user.email)
            #reponse me retourne la cle de mon element dans mon le sous dic de mon_element.concerne
            #indexis retourne lindex de mon element dans ma liste

            if request.method == "POST":

                my_pdf = request.FILES.get('pdf', '')
                print(my_pdf)
                file_path = os.path.join(settings.MEDIA_ROOT, 'depot_note', my_pdf.name)

                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                print(file_path)

                with open(file_path, 'wb') as f:
                    for chunk in my_pdf.chunks():
                        f.write(chunk)

                gere.ajout_fichier(my_pdf.name, reponse, exam)
                #print(mon_module.concerne)
                mon_module.save()

                return redirect(request.path)

            else:
                return render(request, 'cours/vue_etudiant/depot_note.html', context={'pdf': mon_pdf, 'grp': indexis,
                                            'statut': 'Pas noté', 'delai_restant': '', 'commentaire': 'commentaire',
                                            'nom_exam': exam, 'date_fin': date_fin, 'estnote': notation_temporaire})

        except module.DoesNotExist:
            return HttpResponse("<h2>Ce cours na pas de compte dabord</h2>")
        except group_Exist:
            return HttpResponse("<h2>Le groupe nexiste pas</h2>")
    else:
        return HttpResponse("vous ne pouvez pas déposé de note ici")


def add_work_per_prof(request):

    try:
        profile = Profile.objects.get(user__email=request.user.email)
        if profile.choices == "charge_cours":

            return render(request, 'cours/prof/depot_file.html')
        else:
            return HttpResponse("vous navez pas le droit")

    except Profile.DoesNotExist:
        return redirect('user:connexion')


def get_work_group(request):
    pass


#cette fonction je dois la remodifié pour ladapter bien
def lecture_pdf(request, dir, name):

    mon_element = recherche_nom_fichier(dir, name)

    reponse = 0

    print(mon_element)
    if mon_element:
        reponse = 1

    link = f"/mediafiles/{dir}/{name}"

    return render(request, 'cours/load/load_pdf.html', context={'link': link, 'reponse': reponse})


def lecture_pdf_per_prof(request, name_pdf):
    pass


def suppression_fichier_tp_prof(request):
    pass


def count_down(request, calcul_date):
    #maintenant = datetime.now()
        date_entrer = calcul_date.split('-')

        if len(date_entrer) < 3:
            print("je suis au niveau de lentrer ici ")
            return JsonResponse({'erreur': "Votre format de date nest pas respecté!"})

        else:
            horaire_temporaire, minute_temporaire, seconde_temporaire = 23, 59, 59

            # Vérification de la longueur de date_entrer pour ajuster les valeurs
            if len(date_entrer) >= 4:
                horaire_temporaire = int(date_entrer[3])

            if len(date_entrer) >= 5:
                minute_temporaire = int(date_entrer[4])

            if len(date_entrer) == 6:
                seconde_temporaire = int(date_entrer[5])

            date_temp = datetime(int(date_entrer[0]), int(date_entrer[1]), int(date_entrer[2]), horaire_temporaire,  minute_temporaire, seconde_temporaire)

            canada_tz = pytz.timezone('Canada/Eastern')
            maintenant = datetime.now(canada_tz)

            date_temp = canada_tz.localize(date_temp)

            reponse = date_temp - maintenant

            print(f"La reponse est {reponse}")

            resultat_heure, resultat_minute, resultat_seconde = convert_seconde_en_minute_heure(reponse.seconds)

            print(reponse.days)
            if reponse.days < 0:
                print("Je suis au niveau de cette date")
                return JsonResponse({
                    "depassement_date": "yes"
                })

            else:
                return JsonResponse({
                    "days": reponse.days,
                    'hours': resultat_heure,
                    'minutes': resultat_minute,
                    'seconds': resultat_seconde,
                    'calcul_date': calcul_date
                })


def gestion_prof(request):

    if request.method == "POST" and request.headers.get('x-requested-with') == "XMLHttpRequest":

        mon_nom = request.POST.get("nom")
        print(mon_nom)

        return render(request, 'cours/affiche_autre/affiche_date.html')
    else:
        return render(request, 'cours/affiche_autre/affiche_date.html')