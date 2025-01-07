from pprint import pprint
from pathlib import Path

from .fonction import *


def essai_conformite(liste1, liste2):

    if key_dict(liste1) == key_dict(liste2):
        return True

    return False

def verifie_path():
    pass
#une fonction qui va essayer de me lire le contenu de mes_dossier

ma_note = essai_conformite([{'nenean~60%': ''}, {'baba~40%': ''}], [{'nenean~60%': ''}, {'baba~40%': ''}])

#################################################################################"
mon_dico = {'0': [{'Nom': ''}, {'ponderation': 30}], '1': [{'Nom': ''}, {'ponderation': '"hym'}]}
essai_decortique = decortique({'0': {'saodp': '80'}, '1': {'saidou ene': '20'}})
mon_dico1 = key_dict([{0: {'ETUDIANT': ['', '', ''], 'Note': [{'exam1~50': ''}], 'file': [{'exam1~50': ''}], 'limit': 2}}, {1: {'ETUDIANT': ['', '', ''], 'Note': [{'exam1~50': ''}], 'file': [{'exam1~50': ''}], 'limit': 2}}, {2: {'ETUDIANT': ['', '', ''], 'Note': [{'exam1~50': ''}], 'file': [{'exam1~50': ''}], 'limit': 2}}])
print(mon_dico1)
###################################Verification des fonctions regroupe_synchronise #######
first_list = [{"exam1~50": ''}, {"exam2~50": ""}]
second_list = [{"exam2~50": 40}]
list_final = regroupe_synchronise(first_list, second_list)
#print(list_final)
##############################################################################
