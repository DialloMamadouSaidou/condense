from datetime import datetime, date, time, timedelta
from pprint import pprint
from collections import defaultdict, deque
from PIL import Image, ImageEnhance
from io import BytesIO

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.mail import send_mail

from user.models import MyUser, Profile

from .models import *
from .fonction import *

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

"""


def programme_view(request):  # Pour afficher tout les modules
    all = Programme.objects.all()

    return render(request, 'cours/cours_general/programme.html', {'element': all})


def Module(request, ids):  # module contenu dans un programme
    all_element = module.objects.filter(programme__identifiant=ids)

    return render(request, 'cours/cours_general/module.html', context={'element': all_element})


def chapitre_programme(request, ids):  # Pour afficher les chapitres contenu dans un programme
    element = Chapitre.objects.filter(module__identifiant=ids)
    return render(request, 'cours/cours_general/chapitre.html', context={'element': element})


def lessons_chapitre(request, ids):  ##Pour afficher les lessons contenu dans un chapitre
    lesson = Lesson.objects.filter(chapitre__identifiant__icontains=ids)

    return render(request, 'cours/cours_general/lesson_chapitre.html', context={'lesson': lesson})


#######################################################################################################################
#Sa concerne le professeur


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
    element = Planification.objects.filter(professeur=professeur, matiere=mon_crs)
    if element.exists():
        return HttpResponse("Ce cours est déjà pondéré")

    if mon_crs.charge_crs.user.email == request.user.email:
        liste, liste_erreur = [], []
        quota = {}
        somme = 0
        if request.method == 'POST':
            data = request.POST

            for key, value in data.items():
                if key != 'csrfmiddlewaretoken' and key.startswith('ponde'):
                    if value == '':
                        liste_erreur.append(key)
                    else:
                        u = key[-1]
                        somme += int(value)
                        quota[u] = {f'exam{u}': value}
                        pass

            if len(liste_erreur) > 0:
                return HttpResponse("<h2>Toutes vos note doivent avoir une ponderation</h2>")

            if somme == 100:

                Planification.objects.create(professeur=professeur, matiere=mon_crs, ponderation=quota)
                return HttpResponse("Ponderation bien reçu!")
            else:
                return HttpResponse("La somme de vos pondération doivent être de 100%")

        return render(request, 'cours/prof/planifie_note.html')

    else:
        return HttpResponse("<h2>Vous n'êtes pas le charger de ce cours !<h2>")

    return render(request, 'cours/prof/planifie_note.html')


def noter_etudiant(request, mat):
    professeur = Profile.objects.get(user__email=request.user.email)
    mon_crs = module.objects.get(name=mat)
    element = Planification.objects.filter(professeur=professeur, matiere=mon_crs).first()

    majoration = Planification.objects.filter(professeur=professeur, matiere=mon_crs).values_list('majoration')

    print(majoration)

    if element:
        liste_ponderation, liste_ponderation2 = [], []

        element.ponderation = eval(element.ponderation)
        for ponderation in element.ponderation.values():
            for k, v in ponderation.items():
                liste_ponderation.append(f"{k}~{v}%")
                liste_ponderation2.append(v)

        all_cours = Choix_Cours.objects.all()
        liste_etudiant = Choix_Cours.objects.filter(cours__contains=mat).values_list('user__user__email', flat=True)

    else:
        return HttpResponse("Votre matiere nest pas pondéré pour être noté pour le moment!")

    if request.method == 'POST':
        liste_result = []
        data_majoration = {}
        data2 = defaultdict(list)
        data = request.POST
        data = dict(data)

        for key, valeur in data.items():
            if key != 'csrfmiddlewaretoken' and '@' in key:
                print(key)
                for item in valeur:
                    print(item)
                    data2[key].append(f"{key}~{item}")  #Cette ligne me permet de recuperer dans mon dictionnaire letudiant et ses notes.

            elif '@' not in key and key != 'csrfmiddlewaretoken':
                data_majoration[key] = valeur

        for item in data2.values():
            liste_result.append(list(zip(item, liste_ponderation2))) #liste_result me donnera juste letudiant sa note et le pourcentage de son examen

        print(liste_result)
    return render(request, 'cours/prof/noter_etudiant.html', context={'etudiant': liste_etudiant, 'ponde': liste_ponderation})



@login_required
def vue_user(request, domaine):
    #pour le charge de cours à revoir poour optimiser le code
    if domaine == 'charge_cours':
        all_cours = module.objects.filter(charge_crs__user__email=request.user.email)

        return render(request, 'cours/prof/first_vue_prof.html', context={'courses': all_cours})

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

        for key, value in context_cours.items():
            print(key, value)
            print("**" * 30)
        print(liste)

        return render(request, 'cours/vue_etudiant/first_vue.html',
                      context={'liste': liste, 'chapitre': context_cours, 'etudiant': request.user.email})
    return render(request, 'cours/cours_vue_user.html', context={'element': domaine})


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


def choix_cours(request):
    liste1_contient, liste1_not = [], []
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
        user = Profile.objects.get(user__email=email)  #il retourne l'utilisateur qui à le même profile

        for item in module_choices_name:
            if item in all_choices:
                liste1_contient.append(item)
            else:
                liste1_not.append(item)

        if request.method == "POST":
            val1 = request.POST.getlist('option')
            etudiant_principal = Profile.objects.get(user__email=email)
            print(etudiant_principal)
            pprint(val1)
            if len(val1) == 0:
                context_modules['module_choices_name'] = liste1_not
                context_modules['not_choice'] = liste1_contient
                context_modules['error'] = "Vous devrez donnez au moins un choix"
                return render(request, 'cours/choix_cours.html', context=context_modules)

            else:
                dict_union = {}
                matiere, montant_prix = '', ''
                #etudiant_principal = Profile.objects.get(user__user__email=email)
                for item in val1:
                    matiere = module.objects.get(name=item)
                    montant_prix = matiere.price.split("$")[0]
                    print(user)
                    print(matiere)
                    print(montant_prix)
                    current_month = datetime.now()
                    current_month = current_month.month
                    Payer.objects.create(modules=matiere, profile=user, montant=montant_prix, session="session automne")

                Choix_Cours.objects.create(user=user, cours=val1, groupe=1)

                #je dois crée sa facture de paiement ici aussi
                return redirect(request.path)

            return redirect(request.path)
        return render(request, 'cours/cours_general/choix_cours.html',
                      context={'module_choices_name': liste1_not, 'not_choice': liste1_contient})

    return HttpResponse("<h1>Vous ne pouvez pas faire de choix de cours car vous n'êtes pas etudiant</h1>")
