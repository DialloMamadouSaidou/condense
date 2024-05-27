from django.urls import path

from .views import *

app_name = 'user'
urlpatterns = [
    path('create', createuser, name='create'),
    path('general', vue_general, name='general'),
    path('connexion', authentification, name='connexion'),
    path('deconnexion', deconnexion, name='deconnexion'),
    path('modifie', modification_password, name='update'),
    path('recode/<str:ids>', user_email, name="receive"),

    path('recupere', recupere_code, name="recupere")
    #path('^choix_programme/(?P<str:email>)/(%%<str:name>)/($&<str:choix>)/(&&<str:password>)/$', choix_du_programme, name='choix_du_programme')
]