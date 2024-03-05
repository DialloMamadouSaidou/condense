from django.urls import path

from .views import load_lesson, all_chap_auteur, create_lesson, create_chap, programme_view, chapitre_programme, Module, lessons_chapitre, load_the_lesson_in_chapitre

app_name = 'cours'

urlpatterns = [
    path('lessons/<str:ids>', lessons_chapitre, name='lesson'),
    path('programme', programme_view, name='programme'),
    path('chap/<str:ids>', chapitre_programme, name='chapitre'),
    path('module/<str:ids>', Module, name='module'),
    path('create_chap', create_chap, name='create_chap'),
    path('create_lesson/<str:ids>', create_lesson, name='create_lesson'),
    path('chapitre/<str:ids>', all_chap_auteur, name='chapitre_auteur'),
    path('load_lesson', load_the_lesson_in_chapitre, name='load_lesson'),
    path('load/<str:ids>', load_lesson, name="load_lesson")
]