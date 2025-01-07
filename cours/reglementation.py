from pathlib import Path
import os
import re
from datetime import datetime
from collections import defaultdict
import time
import threading

dico = [
    "",
    ""
]


class help_me:
    def __init__(self, backup):
        self.backup = backup
        self.mon_dico = {
            "Programme": 0,
            "Module": 1,
            "Chapitre": 2,
            "Lesson": 3,
            "Note": 4,
            "Plannification": 5,
            "Commentaire": 6,
            "Choix_Cours": 7,
            "Payer": 8,
            "Create_Groupe": 9,
            "Historique": 10
        }
    def __str__(self):
        return self.backup

    def save_remove(self, context, concerne):
        #Le context genre si cest un cours ou un choix, le concerne cest le cours suprrimé
        mon_item = self.backup["Remove"]
        my_date = datetime.now().strftime("%d-%m-%Y")

        index = self.mon_dico.get(context)
        liste = []
        for key, value in mon_item[index].items():
            value.append({my_date: concerne})

    def save_modify(self):
        pass

    def all_traitement(self):
        pass


if __name__ == "__main__":
    backup = {  #Prototype de mon Backup
        "Remove": [
            {"Programme": [

            ]},
            {"Module": [

            ]},
            {"Chapitre": [

            ]},
            {"Lesson": [

            ]},
            {"Note": [

            ]},
            {"Plannification": [

            ]},
            {"Commentaire": [

            ]},
            {"Choix_Cours": [

            ]},
            {"Payer": [

            ]},
            {"Create_Groupe": [

            ]},
            {"Historique": [

            ]},

        ],
        "Modify": [
            {"Programme": [

            ]},
            {"Module": [

            ]},
            {"Chapitre": [

            ]},
            {"Lesson": [

            ]},
            {"Note": [

            ]},
            {"Plannification": [

            ]},
            {"Commentaire": [

            ]},
            {"Choix_Cours": [

            ]},
            {"Payer": [

            ]},
            {"Create_Groupe": [

            ]},
            {"Historique": [

            ]},
        ]
    }
    my_help = help_me(backup)
    my_help.save_remove("Module", 'koto')
    my_help.save_remove('Module', "Nene")
    my_help.save_remove('Programme', "Nene")
    print(backup)

