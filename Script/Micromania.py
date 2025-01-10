from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import math


def get_url_pages(dict_url):
    # initialisation des variables
    html=""
    url_tmp = []
    dict_url_pages = {}
    # Boucle sur le dict_url
    for key_console, link in dict_url.items():
        # Récuperation de la console
        console = key_console
        # Vérification si la console posséde une url
        if link != "":
            # Utilisation de playwright
            with sync_playwright() as playwright:
                # lancer le navigateur
                browser = playwright.chromium.launch(headless=False)
                # Création de la page
                page = browser.new_page()
                page.goto(link, wait_until="domcontentloaded")
                # Pause pour laisser l'affichage se mettre en place
                page.locator('button.trustarc-agree-btn').click()
                html = page.content()
                browser.close()
            # parse la page 
            soup = BeautifulSoup(html, "html.parser")
            # Récuperation du nombre total
            block_nbtotal = soup.find("div", {"class" : "show-more-text"})
            tmp_nbtotal = block_nbtotal.text
            tmp_nbtotal = tmp_nbtotal.split('/')
            # On divise par 20 le nbtotal
            nbtotal = math.ceil(int(tmp_nbtotal[-1]) / 20)
            # On ajout la premiere page
            url_tmp.append(link)
            # on boucle sur le nb_total pour construire l'url en commence à 2
            for i in range(2,nbtotal+1):
                # Construction de l'url    
                url = link+'?page='+str(i)
                print(url)
                # on ajoute l'url dans url_tmp
                url_tmp.append(url)
        else:
            print(f"Aucune url de disponible pour la console : {console}")
        dict_url_pages[console] = url_tmp
        url_tmp = []
        print(f"La récupération des urls des pages pour {console} est terminée...")
    return dict_url_pages

def get_url_games(dict_url_page):
    # Initialisation des variables
    # Boucle sur dict_url_page
    # recuperation de la console
    # boucle sur les links
    # utilisation playwrigth
    # parse html
    # recuperation des urls
    # boucles sur les urls
    # ajout dans list_tmp
    # ajout dans le dictionnaire avec key = console
    pass


def get_info_games(dict_url_games):
    pass


def start_scrap(url, site):
    pass
