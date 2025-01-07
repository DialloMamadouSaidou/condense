import requests
from bs4 import BeautifulSoup

#name text-muted text-decoration-none text-center pt-1

mon_url = "https://icons.getbootstrap.com/"

reponse = requests.get(mon_url)
reponse.raise_for_status()

soup = BeautifulSoup(reponse.text, 'html.parser')

icon_name = soup.findAll('div', class_='name text-muted text-decoration-none text-center pt-1')

with open('bootstrap_icon.txt', 'w') as f:
    for item in icon_name:
        f.write(item.text + '\n')