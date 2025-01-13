from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from datetime import date
import math
import json
import os


def get_url_pages(dict_url):
    '''
        Permet la récuperation des urls des pages de la console visée
        dict_url => Dictionnaire contenant le nom de la console et son url
        return url_pages_console => Dictionnaire contenant toutes les urls des pages de la console visée
    '''
    # Initialisation des varables
    html = ''
    url_tmp = []
    url_pages_console = {}
    print("Récupération des urls des pages : ")
    print("---------------------------------")
    # Boucle sur le dictionnaire
    for key_console, link in dict_url.items():
        # Récupération du nom de la console
        console = key_console
        print(f"Pour la console : {console}")
        print("----------------------------")
        if link != "":
            # Utilisation de playwright
            with sync_playwright() as playwright:
                # Lance le navigateur
                browser = playwright.chromium.launch(headless=False)
                # Création de la page
                page = browser.new_page()
                page.goto(link, wait_until="domcontentloaded")
                # Pause pour laisser l'affichage se mettre en place
                page.locator('button#onetrust-accept-btn-handler').click()
                html = page.content()
                browser.close()
            # Utilisation de beautifulSoup
            soup = BeautifulSoup(html, "html.parser")
            # Récupération de la pagination
            bloc_pagination = soup.find("ul", {"class" : "list-pagination listing-products"})
            # Récupération nombre de page total
            all_li = bloc_pagination.find_all("li")
            nb_page = int(all_li[-2].text)
            # Ajout l'url de la premier page
            url_tmp.append(link)
            print("Liste des urls : ")
            print('----------------')
            print(link)
            # Construction de l'url de chaque page
            for i in range(1,nb_page):
                # https://bons-plans.easycash.fr/jeux-video/nintendo/nes-2?filterType=searchResults&offset=15
                nb_end_url = i * 15
                url = link+"?filterType=searchResults&offset="+str(nb_end_url)
                url_tmp.append(url)
                print(url)
            # Ajout dans le dictionnaire
            url_pages_console[console] = url_tmp
            # Vide url_tmp
            url_tmp = []
        else:
            print("Aucune url pour cette console, vérifier le fichier dédié aux urls.")

    print()
    print(f"La récupération des urls des pages est terminée...")
    return url_pages_console


def get_url_games(dict_pages):
    '''
        Permet la récupération des urls des jeux vidéos pour la console visée
        dict_pages => Dictionnaire contenant les urls provenant de la fonction get_url_pages()
        return url_games => Dictionnaire contenant toutes les urls des jeux vidéo
    '''
    # Initialisation des variables
    html = ''
    url_tmp = []
    url_games = {}
    # Boucle sur le dictionnaire
    for key_console, list_page in dict_pages.items():
        console = key_console
        print("Récupération des urls des jeux :")
        print("--------------------------------")
        print(f"Pour la console :  {console}")
        # Boucle sur la list des urls
        for link in list_page:
            # Utilisation de playwright
            with sync_playwright() as playwright:
                # Lance le navigateur
                browser = playwright.chromium.launch(headless=False)
                # Création de la page
                page = browser.new_page()
                page.goto(link, wait_until="domcontentloaded")
                # Pause pour laisser l'affichage se mettre en place
                page.locator('button#onetrust-accept-btn-handler').click()
                html = page.content()
                browser.close()
            # Utilisation de beautifulSoup
            soup = BeautifulSoup(html, "html.parser")
            # Récupération des urls
            all_bloc_li = soup.find_all("li", {"class" : "clearfix block-link"})
            print("List des urls des jeux :")
            print("------------------------")
            for bloc in all_bloc_li:
                url = bloc['data-href']
                print(url)
                url_tmp.append(url)
        # Ajout dans le dictionnaire
        url_games[console] = url_tmp
        url_tmp = []

    print()
    print("La récupération des urls des jeux est terminée...")
    return url_games


def get_info_games(dict_games, site):
    pass


def start_scrap(dict_url, site):
    pass