import re, string


def donne_string(value: str):

    value = re.sub(",", '', value)
    return value

if __name__=='__main__':
    valeur = donne_string("('asma@gmail.com',)")
    print(valeur)