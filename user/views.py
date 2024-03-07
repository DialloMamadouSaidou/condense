from pprint import pprint

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect

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
            self.said['majf'] = "Ajouter une majuscule"
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
            self.said['digf'] = "Veuillez ajouter un nombre"

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
            self.said['specf'] = "Ajouter un caractère special"

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
        context_empty, context_password = {},{} #Ce sont des dict pour verifier si les données sont rempli ou pas, et le dict
        mykey = [] #verfier la qualite du mpt de passe
        choix = request.POST.get('choix')
        email = request.POST.get('email', '')
        name = request.POST.get('name', '')
        password = request.POST.get('password', '')
        confirmation = request.POST.get('confirmation', '')

        content = {'email': email, 'name': name, 'password': password, 'confirmation': confirmation}
        for key, value in content.items():
            if value == '':
                mykey.append(key)
                context_empty[key] = f'veuillez ajouter {key}'
        for key, value in context_empty.items():
            print(f'{key} : {value}')

        if 0 < len(context_empty) <= 4:
                return render(request, 'user/createuser.html', context=context_empty)

        elif len(context_empty) == 0:
            if password != confirmation:
                return render(request, 'user/createuser.html', context={'confirmations': 'confirmation '})

            else:
                context_general = {}
                control = ControlPassword(password)
                context_password = control.general()
                for key, value in context_password.items():
                    if key.endswith('f'):
                        context_general[key] = value
                        mykey.append(value)

                if len(mykey) != 0:
                    pprint(mykey)
                    return render(request, 'user/createuser.html', context={'bien': mykey})
                else:
                    try:

                        if choix == 'charge_crs' or choix == 'etudiant':
                            ids = "diallo"
                            return redirect(request.path)
                        else:
                            element = MyUser.objects.createuser(email=email, name=name, password=password)
                            Profile.objects.create(user=element, choices=choix)
                            return HttpResponse('<h3>Excellent mot de passe qui respecte tout les critères</h3>')
                    except Exception:
                        return HttpResponse('<h2>Ce mail dutilisateur existe dejà</h2>')

        return HttpResponseRedirect(request.path)

    return render(request, 'user/createuser.html', context={'all': all_programme})


def authentification(request):
    if request.method == 'POST':
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('user:general')
        elif user is None:
            return render(request, 'user/authenticate.html', context={'email': 'Verifiez bien le mail', 'password': 'Verifiez bien le password'})

        return HttpResponseRedirect(request.path)
    return render(request, 'user/authenticate.html')


def vue_general(request): #La première page du site elle dois servir de page d'attraction pour les user

    return render(request, 'user/vu_general.html')

@login_required
def deconnexion(request):
    logout(request)
    return redirect('user:general')


def choix_du_programme(request, email, name, choix, password):
    name, check = '', ''
    all = Programme.objects.all()
    if request.method == "POST":
        name = request.POST.get('option')
        print(name)
    return render(request, 'user/choix_programme.html', context={'all': all})