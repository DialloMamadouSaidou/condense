from datetime import datetime
import ast

import os
import django

# Configuration des paramètres Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'all.settings')
django.setup()

from django.db import models

from cours.models import *
from user.models import *

def add_horaire_to_file():
    mes_elements = Create_groupe.objects.all()
    temp_value = ""
    for item in mes_elements:
        temp_value = ast.literal_eval(item.file_prof)

        for key, value in temp_value.items():

            if "horaire" not in value.keys():
                value["horaire"] = ""

        temp_value = str(temp_value)
        item.file_prof = temp_value

        item.save()