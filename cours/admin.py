from django.contrib import admin

from .models import *

@admin.register(Programme)
class Programme(admin.ModelAdmin):
    list_display = (
        'name',
        'identifiant'
    )

@admin.register(Lesson)
class Lesson(admin.ModelAdmin):
    list_display = (
        'name',
        'identifiant',
        'auteur'
    )

@admin.register(module)
class Module(admin.ModelAdmin):
    list_display = (
        'name',
        'identifiant',
        'price',
        'charge_crs'
    )

@admin.register(Note)
class Note(admin.ModelAdmin):
    list_display = (
        'identifiant',
        'etudiant',
        'module',
        'note',

    )

@admin.register(Chapitre)
class Chapitre(admin.ModelAdmin):
    list_display = (
        'name',
        'module'
    )

@admin.register(Choix_Cours)
class ChoixCours(admin.ModelAdmin):
    list_display = (
        'identifiant',
        'user',
        'date'
    )

@admin.register(Payer)
class Payer(admin.ModelAdmin):
    list_display = (
        'identifiant',
        'profile',
        'modules',
        'montant'
    )

@admin.register(Planification)
class Planifier(admin.ModelAdmin):
    list_display = (
        'identifiant',
        'professeur',
        'matiere',
        'session'
    )