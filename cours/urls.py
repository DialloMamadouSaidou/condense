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
    path('calendrier/<str:year>/<str:month>', calendar_view, name='calendar'),

    path('traitement_form2', traitement_modif_date, name='traitement_form2'),
    ##Cette partie va contenir mes vues specifiés
    path('vue/<str:domaine>', vue_user, name='vue_user'),  #cette vue va contenir le traitement de tout mes types de profil elle sera auto
    #matiquement redirigé après la connexion d'un utilisateur
    path('detail_paiement/<str:etud>', detail_paiement, name='detail_paiement'),
    path('affiche/<str:matiere>', affiche_etudiant, name='affiche'), #Cette vue permet dafficher les eetudiant d'un prof par matiere et les notés
    path('planifie/<str:crs>', planifie_notation, name='planifie'),    #Cette vu permet à un professeur de planifier sa notation en fonction des pourcentages quil donne

    path('note/<str:mat>', noter_etudiant, name='note_etudiant'),    #Cette vue consiste à noté mes etudiants
    path('ponde/<str:mod>', give_note_max, name='ponde'),
    path('releve_note/<str:ids>', releve_note, name="releve"),
    path('only/<str:email>/<str:name>', detail_only_note, name="only"),

    #path('generate-pdf/<str:name>', generate_pdf_view, name='generate_pdf'),
    path('serve-pdf/<str:name>', serve_pdf, name='serve_pdf'),

    path('create/<str:crs>', creation_group, name='create_group'),
    path('ajout_grp/<str:matiere>', ajout_etudiant, name="add_student_in_grp"),
    path('add_work', add_work_per_prof, name="add_work_per_prof"),
    path('ajout_work/<str:matiere>/<str:exam>', ajout_work_groupe_per_etudiant, name="add_work"),

    path('readme/<str:dir>/<str:name>', lecture_pdf, name='lecture'),

    #####################################################################
    #cette affichage sera juste pour la date des request

    path('gestion_prof', gestion_prof, name='affiche_date'),

    path('update_count_date/<str:calcul_date>', count_down, name='count_date')
]

#http://127.0.0.1:8000/cours/serve-pdf/creation_tp_prof/koto@gmail.com-nene~50-dep_exam-explication.pdf