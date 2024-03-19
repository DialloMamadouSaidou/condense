from pprint import pprint

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.mail import send_mail

from user.models import MyUser, Profile

from .models import Programme, Chapitre, module, Lesson, Choix_Cours, Note
from .fonction import file_verify


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

    return render(request, 'cours/programme.html', {'element': all})


def Module(request, ids):  # module contenu dans un programme
    all_element = module.objects.filter(programme__identifiant__icontains=ids)

    return render(request, 'cours/module.html', context={'element': all_element})


def chapitre_programme(request, ids):  # Pour afficher les chapitres contenu dans un programme
    element = Chapitre.objects.filter(module__identifiant__icontains=ids)
    return render(request, 'cours/chapitre.html', context={'element': element})


def lessons_chapitre(request, ids):  ##Pour afficher les lessons contenu dans un chapitre
    lesson = Lesson.objects.filter(chapitre__identifiant__icontains=ids)

    return render(request, 'cours/lesson_chapitre.html', context={'lesson': lesson})



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

    return render(request, 'cours/all_chap_auteur.html', context={'auteur': auteur, 'first': liste_content[0]})


##NB il me reste ici à racommoder le chapitre au programme choisi
def create_chap(request):##Pour creer un chapitre par un professeur
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
                    matiere = request.POST.get('module') #module de lenseignant
                    matiere = module.objects.get(name=matiere)
                    Chapitre.objects.create(name=name, auteur=auteur, module=matiere)
                    return redirect('cours:chapitre_auteur', ids=auteur.identifiant)
                except:
                    element = Chapitre.objects.get(name=name)
                    print(element.identifiant)
                    return render(request, 'not_respect/chap_exist.html', context={"element": element})
            else:
             return render(request, 'cours/create_chap.html', context={'module': mymodule, 'contraint': "Veuillez entrez le nom du chapitre"})
        else:
            return HttpResponse("<h2>Vous navez pas choisi votre module denseignement</h2>")
    return HttpResponse("<h3>veuillez vous connecter à votre compte pour avoir cette permission</h3>")


##Faut aussi tenir compte de la  situation où les formats d'image, de video, et des doc ne sont pas respectés
def create_lesson(request, ids):#Pour creer une lesson
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
                verifie = file_verify(image_1,  video_1, pdf_1)
                context2 = verifie.general()
                for keys, value in context2.items():
                    context[keys] = value


            #print(len(context))
            if len(context) > 0:
                return render(request, 'cours/create_lesson.html', context=context)

            else:

                element = Profile.objects.get(user__email=request.user.email)
                last = Chapitre.objects.last()
                Lesson.objects.create(auteur=element, chapitre=chapitre, name=name, description=description, image_lesson=image, pdf_lesson=pdf, video_lesson=video)
                return redirect(request.path)
            return redirect(request.path)

        else:
            return render(request, 'cours/create_lesson.html')

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
            return render(request, 'cours/load_lesson_with_video.html', context={'title': element.name, 'description': element.description, 'video': video})
        else:
            return render(request, 'cours/load_lesson.html', context={'title': title, 'description': description})

    except:
            print('La video de ce cours pas disponible')
    return render(request, 'cours/load_lesson.html', context={'title': title, 'description': description})
#Remarque pour cette vue on il manque la redirection pour la lecture dela page html
#when user click on the pdf icon


def load_the_lesson_in_chapitre(request):

    return render(request, 'cours/load_lesson_with_video.html')

##Vue pour l'espace de chaque membre

#Pas achevé cette vue

@login_required
def vue_user(request, domaine):
    if domaine == 'charge_cours':
        #Recupéré tout les étudiants inscrits sur ce cours
        dico, dico1, dico2 = {}, {}, {}
        liste_users, counter = {}, {} #counter comme son nom l'indique il comptera etudiant dans un module
        liste_recupere, liste_user, liste, liste_set = [], [], [], []
        #liste va me servir pour recuperer le nombre d'etudiant inscrit dans un cours
        all_choix = Choix_Cours.objects.all()
        mail_user = request.user.email #je recupère le mail de l'enseignant connecté
        all_choices = Choix_Cours.objects.all()
        liste_recupere = [item.name for item in module.objects.all() if item.charge_crs.user.email == mail_user] #je recupère tout les modules du charger de cours
        all_note = Note.objects.all()
        mykey = [] #Cette liste servira à contenir toutes les clés de ma future table

        for item in all_note:
            mykey.append(item.module.name)

        mykey = list(set(mykey))
        for item in mykey:
            dico1[item] = []


        for item in all_choices:
            item.cours = eval(item.cours) #je recupere la liste des cours
            for element in item.cours:
                if element in liste_recupere:
                    liste.append(element)

        liste_set = list(set(liste))

        for item in liste_set:
            dico[item] = []

        for item in liste_set:
            counter[item] = liste.count(item) #Pour compter le nombre d'etudiant d'une classe


        for item in all_note:
            if item.module.name in liste_recupere:
                for element in dico1:
                            if item.module.name == element:
                                        dico1[element].append({item.etudiant.user.email: item.note})

        for key, value in dico1.items():
            print(f"{key}~{value}")

        print("--"*25)
        for item in all_choices: #jitere sur tout les élements de la table Choix_Cours
            for element in item.cours: #J'itère sur les élements de cours
                if element in liste_recupere: #Je verifie sur le cours appartient au modules enseignés par l'enseignant
                                        for key in dico:
                                                if key == element: #je verifie si la clé de mon dico est égal à mon element trouver
                                                        dico[key].append(item.user.user.email)#j'ajoute cet élément dans mon dico

        for key, value in dico.items():
            print(key, value)
        all_etudiant = ''
        my_cours = ''
        obligation = ["Create a chapter", "Create a lesson", "Create a td"]
        facultatifs = ["create an evaluation", "Create a group", "Create an evaluation/group work", "Put a deposit option"]
        #context_etudiant = {"obligatoires": obligation, "facultatif": facultatifs, "user": liste_user}
        context_etudiant = {"dico": dico}
        return render(request, 'cours/cours_vue_user.html', context=context_etudiant)

    elif domaine == "charger_financier":
        obligation = ["Payé/Etudiant", "Non_payé/Etudiant", "Payé/Prof", "Not Paie/Prof"]

        context_finance = {'obligation': obligation}
        return render(request, 'cours/cours_vue_user.html', context=context_finance)

    elif domaine == "etudiant":
        return HttpResponse("Bienvenu je suis un étudiant !")
    return render(request, 'cours/cours_vue_user.html', context={'element': domaine})
#Pause de développement pour finir d'abord avec le choix de cours pour les étudiants.
#######################################################################################################################

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
        all_choices = [] #recupéré tout les choix d'un utilisateur
        val1 = ''
        context_modules = {}
        domaine = request.user.profile.domaine_programme.title()
        module_choices_name = module.objects.filter(programme__name=domaine)#il va me retourner le nom des modules en formats chaine de caractère dans un type django.models.query.set
        module_choices_name = [item.name for item in module_choices_name]#j'ai converti le type de sorti en class list
        email = request.user.email #Recuperer le mail de l'utilisateur pour mieux chercher son profil
        all_element = Choix_Cours.objects.filter(user__user__email=email)#Pour retrouver tout les choix de mon  utilisateur dans ma BD

        for item in all_element: #le all_element est une liste qui contient que des strings
            item.cours = eval(item.cours) #j'evalue les items de cet all_element pour les convertir facilement en liste
            all_choices.extend(item.cours)#à chaque item retrouvé  je letend dans ma dictionnaire que javais déclaré

        all_choices = list(set(all_choices)) #Pour chaque element  de ma liste je le set pour eviter la repetition, qui va retourner un set puis le list pour renvoyer une liste
        user = Profile.objects.get(user__email=email)#il retourne l'utilisateur qui à le même profile

        for item in module_choices_name:
            if item in all_choices:
                liste1_contient.append(item)
            else:
                liste1_not.append(item)

        if request.method == "POST":
            val1 = request.POST.getlist('option')
            pprint(val1)
            if len(val1) == 0:
                context_modules['module_choices_name'] = liste1_not
                context_modules['not_choice'] = liste1_contient
                context_modules['error'] = "Vous devrez donnez au moins un choix"
                return render(request, 'cours/choix_cours.html', context=context_modules)

            else:
                Choix_Cours.objects.create(user=user, cours=val1, groupe=1)
                return redirect(request.path)

            return redirect(request.path)
        return render(request, 'cours/choix_cours.html', context={'module_choices_name': liste1_not, 'not_choice': liste1_contient})

    return HttpResponse("<h1>Vous ne pouvez pas faire de choix de cours car vous n'êtes pas etudiant</h1>")