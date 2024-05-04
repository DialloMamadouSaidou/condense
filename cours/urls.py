from django.urls import path

from .views import *
app_name = 'cours'

urlpatterns = [
    path('lessons/<str:ids>', lessons_chapitre, name='lesson'),     #pour lire une lesson dun chapitre
    path('programme', programme_view, name='programme'),    #pour afficher les programmes de ma BD
    path('chap/<str:ids>', chapitre_programme, name='chapitre'),    #Pour lire un chapitre en particulier
    path('module/<str:ids>', Module, name='module'),    #Pour lire un module(une matière) en particulier
    path('create_chap', create_chap, name='create_chap'),   #Pour crée un chapitre
    path('create_lesson/<str:ids>', create_lesson, name='create_lesson'),   #Pour crée une lesson à partir dun chapitre specifié
    path('chapitre/<str:ids>', all_chap_auteur, name='chapitre_auteur'),    #Tout les chapitres d'un professeur
    path('load_lesson', load_the_lesson_in_chapitre, name='load_lesson'),
    path('load/<str:ids>', load_lesson, name="load_lesson"),    #Pour lire une lesson
    path('choix', choix_cours, name="choix_cours"),         #Pour faire un choix de Cours
    ##Cette partie va contenir mes vues specifiés
    path('vue/<str:domaine>', vue_user, name='vue_user'),  #cette vue va contenir le traitement de tout mes types de profil elle sera auto
    #matiquement redirigé après la connexion d'un utilisateur
    path('detail_paiement/<str:etud>', detail_paiement, name='detail_paiement'),
    path('affiche/<str:matiere>', affiche_etudiant, name='affiche'), #Cette vue permet dafficher les eetudiant d'un prof par matiere et les notés
    path('planifie/<str:crs>', planifie_notation, name='planifie'),    #Cette vu permet à un professeur de planifier sa notation en fonction des pourcentages quil donne

    path('note', noter_etudiant, name='note_etudiant') #Cette vue consiste à noté mes etudiants
]