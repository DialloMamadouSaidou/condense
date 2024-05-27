import string
from random import choice

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models

#from cours.models import Programme

# Create your models here.


class MyUserManager(BaseUserManager):

    def createuser(self, email, name, password):
        if not email:
            raise ValueError("L'email est nécessaire pour la creation dun compte")

        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def createsuperuser(self, email, name, password):
        user = self.createuser(email=email, name=name, password=password)

        user.is_staff = True
        user.admin = True
        user.save(using=self._db)
        return user


def trois_element(element):
    if len(element) > 3:
        return element[:3]

    else:
        return element


class MyUser(AbstractBaseUser):
    email = models.EmailField(blank=False, unique=True, max_length=50)
    name = models.CharField(blank=True, max_length=50)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    objects = MyUserManager()

    code_secret = models.CharField(max_length=15, blank=True)

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


class Profile(models.Model):
    identifiant = models.CharField(max_length=15, blank=True, unique=True)
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE)

    #choices = models.CharField(max_length=90, choices=choix, blank=False)
    choices = models.CharField(max_length=90, blank=True)
    domaine_programme = models.CharField(max_length=50, blank=True)#cette colonne me permettra
    #code_secret = models.CharField(max_length=15, blank=True)
    #dajouter le programme auquel letudiant ou le charger de cours doit enseigner
    #qui sera géré au niveau de la création de lutilisateur

    def save(self, *args, **kwargs):
       self.identifiant = ''.join([choice(string.ascii_letters + string.digits) for _ in range(3)]) + trois_element(self.user.name)

       super().save(*args, **kwargs)

    def __str__(self):
        return self.user.email

"""
    Le domaine_programme concerne le prof charger du cours et letudiant
    le domaine_module concerne le prof, le charger_td et letudiant.
"""

