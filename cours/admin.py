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
        'price'
    )

@admin.register(Note)
class Note(admin.ModelAdmin):
    list_display = (
        'identifiant',
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