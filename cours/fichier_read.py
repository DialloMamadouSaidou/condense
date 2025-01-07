import pandas as pd
from pprint import pprint

def lecture_fichier(name_fichier, column):
    file = pd.read_csv(name_fichier, header=0, sep=";")

    if (name_fichier.split("/")[-1]).split(".")[-1] != 'csv' or name_fichier.split(".")[-1] != "csv":
        print("Desolé le fichier nest pas csv")

    else:

        try:
            if file[column].isna().sum() > 0:
                print("Cette colonne contient des valeurs non definis")

        except Exception:
            print("Cette colonne nexiste pas")

            print("Veuillez choisir une autre colonne qui ne contient pas de valeur non definis parmi les colonnes ci dessous ")
            for item in file.columns.tolist():
                print(f"Vous avez la colonne: {item}")

        else:

            try:
                print(f"Le Maximum est : {file[column].max()}")
                print(f"Le Minimum est : {file[column].min()}")
                print(f"La moyenne est : {file[column].mean()}")

            except Exception:
                print("La colonne ne contient pas de nombre")



if __name__ == "__main__":
    file = "/home/med/Downloads/climat.csv"

    lecture_fichier(f"{file}", "pointes_bonus")