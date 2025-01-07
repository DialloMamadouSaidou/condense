from cachetools import cached, LRUCache
import functools
from calendar import HTMLCalendar, Calendar
from collections import defaultdict, deque

class Moncalendrier(HTMLCalendar):

    def day_in_month(self, year, month):
        mon_dico_date = defaultdict(list)
        mes_elements = self.itermonthdays2(year, month)
        #print(mes_elements)
        for item in mes_elements:
            item = list(item)

            if item[0] != 0:
                if item[1] == 0:
                    mon_dico_date["Lundi"].append(item[0])

                elif item[1] == 1:
                    mon_dico_date["Mardi"].append(item[0])

                elif item[1] == 2:
                    mon_dico_date["Mercredi"].append(item[0])

                elif item[1] == 3:
                    mon_dico_date["Jeudi"].append(item[0])

                elif item[1] == 4:
                    mon_dico_date["Vendredi"].append(item[0])

                elif item[1] == 5:
                    mon_dico_date["Samedi"].append(item[0])

                elif item[1] == 6:
                    mon_dico_date["Dimanche"].append(item[0])

        dict_final = {}
        liste = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
        for item in liste:
            dict_final[item] = mon_dico_date[item]

        dict_final = reconfigure_liste(dict_final)
        return dict_final

    def cal_html(self, year, month):

       mon_dico = self.day_in_month(year, month)

       premier_jours = ""

       for key in mon_dico.keys():
           if mon_dico[key][0] == 1:
               premier_jours = key

       ma_table = "<table class='table' id='tableau'>\n"

       ma_table += "<thead>\n"
       ma_table += "<tr>"
       for key in mon_dico.keys():
           ma_table += f"<th>{key}</th>\n"
       ma_table += "</tr>\n"
       ma_table += "</thead>\n"

       ma_table += "<tbody>\n"
       if premier_jours != "Dimanche":
            for i in range(5):
                ma_table += "<tr>"
                for key in mon_dico.keys():
                    date = mon_dico[key][i]
                    if date != '':
                        ma_table += f"<td class='date' data-index='{month}.{date}.{year}'>{date}</td>"
                    else:
                        ma_table += f"<td class='vide'>{date}</td>"
                ma_table += "</tr>\n"
            ma_table += "</tbody>"
            ma_table += "</table>"
       else:
           for i in range(6):
               ma_table += "<tr>"
               for key in mon_dico.keys():
                   date = mon_dico[key][i]

                   ma_table += f"<td class='date' data-index='{month}.{date}.{year}'>{date}</td>"
               ma_table += "</tr>\n"
           ma_table += "</tbody>"
           ma_table += "</table>"
       return ma_table


#def good_comp(dico: dict):
 #   return dict

#Il me permet de reconfigurer ma liste pour afficher un bon calendrier
def reconfigure_liste(ma_liste: dict):

    mes_cle = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
    premier_jours, left_liste, rigth_liste = "", [], []
    liste_debut_jours = list(range(8))
    for key in ma_liste.keys():
        if ma_liste[key][0] == 1:
            premier_jours = key
            break
    if premier_jours != "Lundi" and premier_jours != "Dimanche":
        mon_index = mes_cle.index(premier_jours)
        left_liste, right_liste = mes_cle[0: mon_index], mes_cle[mon_index+1: 7]
        for key in ma_liste.keys():
            if key in left_liste:
                if ma_liste[key][0] in liste_debut_jours:
                    petite = deque(ma_liste[key])
                    petite.appendleft('')
                    ma_liste[key] = list(petite)

                if len(ma_liste[key]) < 5:
                    for _ in range(5 - len(ma_liste[key])):
                        ma_liste[key].append('')
            if key in right_liste:
                if len(ma_liste[key]) < 5:
                    for _ in range(5 - len(ma_liste[key])):
                        ma_liste[key].append('')
    elif premier_jours == "Dimanche":

        for key in ma_liste.keys():
            if key != "Dimanche":
                petite = deque(ma_liste[key])
                petite.appendleft("")
                ma_liste[key] = list(petite)

            if len(ma_liste[key]) < 6:
                for _ in range(6 - len(ma_liste[key])):
                    ma_liste[key].append('')

    elif premier_jours == "Lundi":

        for key in ma_liste.keys():
            if len(ma_liste[key]) < 5:
                ma_liste[key].append('')

    return ma_liste


cal = Moncalendrier()
calendrier = cal.day_in_month(2024, 9)
print(calendrier)

"""
ma_liste = {'Lundi': [5, 12, 19, 26],
            'Mardi': [6, 13, 20, 27],
            'Mercredi': [7, 14, 21, 28],
            'Jeudi': [1, 8, 15, 22, 29],
            'Vendredi': [2, 9, 16, 23, 30],
            'Samedi': [3, 10, 17, 24, 31],
            'Dimanche': [4, 11, 18, 25]}
"""

#repet= reconfigure_liste(ma_liste)
#print(repet)
