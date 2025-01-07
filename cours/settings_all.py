import os
from collections import defaultdict

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "all.settings")

django.setup()

mon_dico = defaultdict(list)

#Les permissions sont donnés par les
#chargés de cours
#le chargé de cours reçois ces permission aussi du chef de prgramme


dico = {

    "charger_cours": [
        {
            "Ajouter etudiant": "Oui",
            "Ajouter Note": "Oui",
            "Corriger Copie": "Oui",
            "Retirer_permisssion": "Oui",
            "Ajouter Copie": "Oui"
        }
    ],

    "charger_td": [

        {
            "Ajouter Etudiant": "Non",
            "Ajouter Note": "Oui/Non",
            "Corriger Copie": "Oui/Non",
            "Retirer_permisssion": "Non"
        }
    ],

    "correction_td": [

        {
            "Ajouter etudiant": "Oui",
            "Ajouter Note": "Oui",
            "Corriger Copie": "Oui",
            "Retirer_permisssion": "Oui"
        }
    ],

    "Etudiant": [

        {
            "Ajouter etudiant": "Oui",
            "Ajouter Note": "Oui",
            "Corriger Copie": "Oui",
            "Retirer_permisssion": "Oui"
        }
    ]
}

Note = {

    "[NZOE19079909]": "[83, ]",
    "[BLAS15628405]": "[74, ]",
    "[Andrilla Savard]": "[90, ]",
    "[Mamadou Samba]": "[78, ]",
    "[Adama Diouf]": "[88.5, ]",
    "[abdou samad Fall]": "[72, ]",
    "[KOUA18090300(94), NGAM18580200, DIAI19040301(95)]": "[94, ]",
    "[LOXS23010400(96), MAAO04110100(96)]": "[99, ]",
    "[RAKM23110200(55), RANR301101011(50), HARE22610300(90)]": "[93]",
    "[Cédric Montcalm(100), Maxime Bradette(78), Khaled Hamdaoui(97)]": "[80, ]",
    "[David Tremblay(73)]": "[94.5]",
   "[DIOA085196(50)]": "",
    "[TEMA25089500(45)]": "",
    "[SAMM02039509(45)]": "",


    "[RANI19560500(98), NAZA20019802(90), CONT03040200(80)]": "[88]"
}