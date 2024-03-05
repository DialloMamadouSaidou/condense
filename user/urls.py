from django.urls import path

from .views import createuser, vue_general, authentification, deconnexion

app_name = 'user'
urlpatterns = [
    path('create', createuser, name='create'),
    path('general', vue_general, name='general'),
    path('connexion', authentification, name='connexion'),
    path('deconnexion', deconnexion, name='deconnexion')
]