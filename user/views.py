from pprint import pprint

from django.urls import reverse
from faker import Faker

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail, EmailMultiAlternatives
from django.db.models.query import QuerySet

from all.settings import EMAIL_HOST_USER
from .models import MyUser, Profile
from cours.models import Programme
# Create your views here.


class ControlPassword:

    def __init__(self, password):
        self.password = password
        self.said = {}

    def controlen(self):
        if len(self.password) < 6:
            self.said['lenf'] = "Password Court"
        else:
            self.said['lent'] = "Longueur verifié"

        return self.said

    def controlmaj(self):
        index = False
        for item in self.password:
            if item.isupper():
                index = True
                break
        if index:
            self.said['majt'] = "Majuscule ajouté"
        else:
            self.said['majf'] = "Ajouter au moins une majuscule"
        return self.said

    def digit(self):
        index = False
        for item in self.password:
            if item.isdigit():
                index = True
                break
        if index:
            self.said['digt'] = "Merci pour l'ajout du nombre"
        else:
            self.said['digf'] = "Veuillez ajouter au moins un nombre"

        return self.said
    def isalnumcharacter(self):
        index = False
        for item in self.password:
            if not item.isalnum():
                index = True
                break
        if index:
            self.said['spect'] = "Caractère special ajouté"
        else:
            self.said['specf'] = "Ajouter au moins une caractère special"

        return self.said


    def general(self):
        self.digit()
        self.controlen()
        self.controlmaj()
        self.isalnumcharacter()
        return self.said

    def __str__(self):
        return f"Le mot de passe est {self.password}"

#
def createuser(request):
    all_programme = Programme.objects.all()

    if request.method == 'POST':
        all_programmes = Programme.objects.all()
        liste = all_programme
        context_choix, non_respect_password_contrainte, context_confirmation, context_empty, context_password = {}, {}, {}, {}, {} #Ce sont des dict pour verifier si les données sont rempli ou pas, et le dict
        mykey = [] #verfier la qualite du mpt de passe
        choix = request.POST.get('choix')
        email = request.POST.get('email', '')
        name = request.POST.get('name', '')
        password = request.POST.get('password', '')
        confirmation = request.POST.get('confirmation', '')
        other_choice = request.POST.get('option')

        print(choix)
        print(other_choice)

        content = {'email': email, 'name': name, 'password': password, 'confirmation': confirmation}
        for key, value in content.items():
            if value == '':
                mykey.append(key)
                context_empty[key] = f'Veuillez entrez votre {key}'

        #Ce context_empty avec la clé all me permet d'ajouter les elements du programme dans ma page en cas d'erreur
        context_empty["all"] = all_programmes
        print(len(context_empty))
        if 1 < len(context_empty) <= 5:
                return render(request, 'user/createuser.html', context=context_empty)

        elif len(context_empty) == 1:
            if password != confirmation:    #Ce context verifie si les mots de passeses entrés sont les mêmes
                context_confirmation['confirmation'] = "Assurez vous d'avoir entré le même password"
                context_confirmation['all'] = all_programmes
                return render(request, 'user/createuser.html', context=context_confirmation)

            else:
                context_general = {}
                control = ControlPassword(password)
                context_password = control.general()
                for key, value in context_password.items():
                    if key.endswith('f'):
                        context_general[key] = value
                        mykey.append(value)

                #print(len(mykey))
                if len(mykey) != 0:
                    non_respect_password_contrainte['bien'] = mykey #il
                    non_respect_password_contrainte["all"] = all_programmes
                    for key, val in non_respect_password_contrainte.items():
                        print(key, val)
                    return render(request, 'user/createuser.html', context=non_respect_password_contrainte)
                else:
                    try:
                        if choix in ["charge_cours", "etudiant"] and other_choice is None:
                            context_choix["all"] = all_programmes
                            context_choix["entre"] = "Veuillez entrez votre choix"
                            return render(request, 'user/createuser.html', context=context_choix)

                        elif choix in ["charge_cours", "etudiant"] and other_choice is not None:
                            element = MyUser.objects.createuser(email=email, name=name, password=password)
                            Profile.objects.create(user=element, choices=choix, domaine_programme=other_choice)
                            return HttpResponse("<h2>Bonne Initiative</h2>")
                        else:
                            element = MyUser.objects.createuser(email=email, name=name, password=password)
                            Profile.objects.create(user=element, choices=choix, domaine_programme='')
                            return HttpResponse('<h3>Excellent mot de passe qui respecte tout les critères</h3>')

                    except Exception:
                        return HttpResponse('<h2>Ce mail dutilisateur existe dejà</h2>')

        return HttpResponseRedirect(request.path)

    return render(request, 'user/createuser.html', context={'all': all_programme})

#NB:A noter bien que les HttpResponse seront remplacés par des render avec des vues plus completes
def authentification(request):
    if request.method == 'POST':
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            user = MyUser.objects.get(email=email)
            the_profile = Profile.objects.get(user=user)
            #Je recupère le choix pour afficher une vue personnaliser au niveau du cours
            print(the_profile.choices)
            return redirect('cours:vue_user', domaine=the_profile.choices)
        elif user is None:
            return render(request, 'user/authenticate.html', context={'email': 'Verifiez bien le mail', 'password': 'Verifiez bien le password'})

        return HttpResponseRedirect(request.path)
    return render(request, 'user/authenticate.html')


def vue_general(request): #La première page du site elle dois servir de page d'attraction pour les user
    #La vue dois être la vue principal
    return render(request, 'user/vu_general.html')

@login_required
def deconnexion(request):
    logout(request)
    return redirect('user:general')


def modification_password(request):

    if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        email = request.POST.get('email')
        #print(request.POST)
        try:
            mon_utilisateur = MyUser.objects.get(email=email)

            fake = Faker()
            code_secret = fake.bothify('###-???;#')

            mon_utilisateur.code_secret = code_secret
            mon_utilisateur.save()

            subject, from_email, to = "hello", EMAIL_HOST_USER, "saidessai466@gmail.com"
            text_content = "This is an important message."
            html_content = f"""
                    <p>Votre de code de confirmation svp <strong>{code_secret}</strong> </p>"""
            
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()



            messages.success(request, "Code a bien été envoyé!")
            messages.success(request, "Verifié bien votre email")

            if request.method == "POST":
                code = request.POST.get("code")
                print(code)
            return JsonResponse({"success": True})


        except MyUser.DoesNotExist:
            messages.error(request, "Cet utilisateur na pas de compte dans notre BD!")
            return JsonResponse(
                {'success': False, 'message': "Cet utilisateur n'a pas de compte dans notre base de données!"})
    return render(request, 'user/modifie.html')


def user_email(request, ids):
    # update_session_auth_hash(request, mon_utilisateur)
    try:
        user = MyUser.objects.get(email=ids)
        if request.method == "POST":
            mot_de_passe = request.POST.get("password", "")
            confirmation = request.POST.get("confirmation", "")

            if mot_de_passe == "":
                messages.error(request, "Vous devez entrez votre mot de passe")
                return redirect(request.path)

            elif mot_de_passe != confirmation:
                messages.error(request, "Vous devez entrez le meme mot de passe au niveau de la confirmation")
                return redirect(request.path)

            else:
                control_erreur = {}
                control = ControlPassword(mot_de_passe)
                control = control.general()

                for key, value in control.items():
                    if key.endswith("f"):
                        control_erreur[key] = value

                if len(control_erreur) >= 1:
                    return render(request, 'user/receive_code.html', context={"erreur": control_erreur})

                else:
                    user.set_password(mot_de_passe)
                    update_session_auth_hash(request, user)
                    user.save()

        else:
            return render(request, "user/receive_code.html")

    except MyUser.DoesNotExist:
        pass

    return render(request, "user/receive_code.html")


def recupere_code(request):

    if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        email = request.POST.get('email')
        code = request.POST.get('code')

        try:
            my_user = MyUser.objects.get(email=email)

            if my_user.code_secret == code:
                return JsonResponse({'success': True, 'message': "Code validé avec succès!", 'redirect_url': reverse('user:connexion')})

            else:
                return JsonResponse({'success': False})


        except MyUser.DoesNotExist:
            pass

    return render(request, 'user/modifie.html')

