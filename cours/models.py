import string
from random import choice

from django.db import models
from django.db.models import F
from django.core.validators import MaxValueValidator, MinValueValidator

from user.models import Profile

# Create your models here.
"""
    Dans mes models qu'est ce que je dois avoir:
     -une table de domaine ou des programmes exemple Math, Info,
     -on met pas de cyles ici je dois juste mettre en sorte que les cours sois 
     en fonction des choix du programme
     -une table de leçon où prof pourra dispenser et etudiant peut suivre
     *le prof peut donner des  cours devoir ou meme crée des QCM devaluation
     *le prof peut aussi donner des devoirs en donnant la possibilités de les rendres
     *dans un format defini et surtout donner la possibilité de deposer ou pas
     //////////////////////////////////////////////////////////////////////
     *letudiant peut etre evaluer et dans son portail pourra les consulter
     
     -une table de commentaire et de reponse mais reponse dois heriter de (commentaire)
     **une table note pour evaluer les profs et les etudiants en fonction du programme et les etudiants
     sa dois facilement leur donner accès à leur dossier etudiant
     //////////////////////////////////////////////////////////////////////////////////////////////////////
     A noter que la table note dois permettre juste de recuperer directement
     les notes d'un user et aussi faire l'evaluation du niveau des eleves dans ce module
     //////////////////////////////////////////////////
     Module c'est comme une matiere qui sera contenu dans un programme qui contiendra des 
     chapitres et aussi ces chapitrses qui contiendra des leçons
     exemple de module Element de  Programmation en tenant compte aussi des groupes
"""


def trois_element(element):
    if len(element) > 3:
        return element[:3]

    return element


class Programme(models.Model):#Programme
    identifiant = models.CharField(unique=True, max_length=50, blank=True)
    name = models.CharField(max_length=50, blank=False, unique=True)
    dp = models.OneToOneField(Profile, on_delete=models.SET_NULL, null=True, verbose_name='directeur_programme')
    image_programme = models.ImageField(upload_to='image/programme', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Programme'
        verbose_name_plural = 'Programmes'

    def save(self, *args, **kwargs):
        self.identifiant = ''.join([choice(string.ascii_letters + string.digits) for _ in range(3)]) + '-' + trois_element(self.name)
        super().save(*args, **kwargs)


class module(models.Model):     #Matiere
    identifiant = models.CharField(max_length=110, unique=True, blank=True)
    name = models.CharField(max_length=100, unique=True)
    charge_crs = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    programme = models.ForeignKey(Programme, on_delete=models.SET_NULL, null=True, blank=True)
    price = models.CharField(max_length=9, blank=True)
    image_module = models.ImageField(upload_to='Image/module', blank=True, null=True)

    class Meta:
        verbose_name = 'Module'
        verbose_name_plural = 'Modules'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.identifiant = ''.join([choice(string.ascii_letters + string.digits) for _ in range(3)]) + '-' + self.name
        super().save(*args, **kwargs)


class Chapitre(models.Model):   #Chapitre
    identifiant = models.CharField(max_length=200, unique=True, blank=True)
    name = models.CharField(max_length=200, unique=True)
    module = models.ForeignKey(module, on_delete=models.SET_NULL, null=True)
    auteur = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        unique_together = ('name', 'module')
        ordering = ['module']
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.identifiant = ''.join([choice(string.ascii_letters + string.digits) for _ in range(3)]) + trois_element(self.name)
        super().save(*args, **kwargs)


class Lesson(models.Model):#Lesson
    identifiant = models.CharField(max_length=30, blank=True, unique=True)
    auteur = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    chapitre = models.ForeignKey(Chapitre, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=40, blank=False, unique=True)
    description = models.TextField(blank=True)

    image_lesson = models.ImageField(upload_to='image_crs/', blank=True, null=True)
    pdf_lesson = models.FileField(upload_to='pdf_crs/', blank=True, null=True)
    video_lesson = models.FileField(upload_to='video_crs/', blank=True, null=True)

    def save(self, *args, **kwargs):
        self.identifiant = ''.join([choice(string.ascii_letters + string.digits) for _ in range(3)]) + trois_element(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}~{self.auteur}'

#Elle va entrez en action lorque l'etudiant choisira ces cours.


class Note(models.Model):#Note
    identifiant = models.CharField(max_length=100, blank=True, unique=True)

    etudiant = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    module = models.ForeignKey(module, on_delete=models.SET_NULL, null=True)
    note = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(20)])
    commentaire = models.CharField(max_length=500, default='')


    def save(self, *args, **kwargs):
        self.identifiant = self.etudiant.user.email + '~' + self.module.name
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'note'
        verbose_name_plural = "Note Etudiant"
        ordering = ['note']
        unique_together = ('module', 'etudiant')

    def __str__(self):
        return f"{self.etudiant} {self.module}"
#Une table pour le choix Où un etudiant pourra chosir ses cours en fonctions de ses besoins
#Et surtout en fonction de son domaine


class Commentaire(models.Model):
    identifiant = models.CharField(max_length=20, blank=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    content = models.CharField(max_length=500, blank=False)

    def save(self, *args, **kwargs):
        self.identifiant = ''.join([choice(string.ascii_letters + string.digits) for _ in range(5)]) + '-' + trois_element(self.user.email)
        super().save(*args, **kwargs)

#Choix_du_cours_Pour_letudiant && aussi du module pour le prof && aussi du td


class Choix_Cours(models.Model):
    identifiant = models.CharField(max_length=10, unique=True, blank=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    cours = models.CharField(max_length=500)
    groupe = models.PositiveIntegerField(default=1)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.identifiant

    class Meta:
        verbose_name = 'COURS&Etudiant'
        verbose_name_plural = 'COURS&Etudiants'


    def save(self, *args, **kwargs):
        self.identifiant = ''.join([choice(string.ascii_letters + string.digits) for _ in range(5)])
        super().save(*args, **kwargs)


class Payer(models.Model):
    identifiant = models.CharField(max_length=400, unique=True, blank=True)
    modules = models.ForeignKey(module, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    montant = models.PositiveIntegerField()
    session = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Paiement"
        verbose_name_plural = "Paiements"
        unique_together = ('modules', 'profile', 'session')

    def __str__(self):
        return f"{self.profile} + {self.modules}"

    def save(self, *args, **kwargs):
        self.identifiant = f"{self.profile} + {self.session} + {self.modules}"
        super().save(*args, **kwargs)