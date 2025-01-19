'''
    File allowing you to retrieve information on video games from the site: www.jeuxvideo.com
    The following functions are used to:
        - get_url_pagination => allows you to retrieve the urls of all the pages present in the pagination
        - get_url_games => allows you to retrieve the urls of the games present in each page of the targeted console
        - get_info_games => allows the recovery of information for each game for the targeted console
        - start_scrap => allows the sequence of previous functions for scraping the site
'''

from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from datetime import date
import requests
import re
import os
import json
import math

url_base = "https://www.jeuxvideo.com"

def get_url_pagination(url_list):
    '''
        Allows retrieval of the urls of each page according to the pagination present.
        url_list => list containing the target urls.
        url_pages_consoles => Returns a DICT containing all its urls per console.
    '''
    # Initialisation des variables
    html = ""
    url_pages_consoles = {}
    url_tmp = []
    # On parcours la list des urls
    for key_console, link in url_list.items():
        # Recuperation de la console
        console = key_console
        print("For the console  : "+console)
        print("------------------------------")
        # Vérification si link est vide ou pas
        if link != "":
            # Utilisation de playwright
            with sync_playwright() as playwright:
                # lancer le navigateur
                browser = playwright.chromium.launch(headless=False)
                # Création de la page
                page = browser.new_page()
                page.goto(link, wait_until="domcontentloaded")
                # Pause pour laisser l'affichage se mettre en place
                page.locator('button.jad_cmp_paywall_cookies').click()
                html = page.content()
                browser.close()
            # Utilisation de  BeautifulSoup
            soup = BeautifulSoup(html, "html.parser")
            # Recuperation du nombre de jeux Total
            bloc_nb_game = soup.find("span", {"class" : "cardListHeader__count"})
            nb_game = bloc_nb_game.text
            # Vérifier que nb_game soit bien formater (2 291 => 2291)
            if " " in nb_game:
                nb_game = nb_game.replace(" ", "")
            print("Total number of games =>  "+bloc_nb_game.text)
            # Vérification si nb_game superieur à 20
            if int(nb_game) > 25:
                # Ajout url principal
                nb_pages = math.ceil(int(nb_game) / 25)
                print("Total number of pages =>  "+str(nb_pages))
                print("The urls :")
                print("-----------")
                url_tmp.append(link)
                print(link)
                for i in range(2, nb_pages+1):
                    url_created = link +"?p="+ str(i)
                    url_tmp.append(url_created)
                    print(url_created)
            else:
                # Ajout de l'url directement
                url_tmp.append(link)
                print(link)
            # Sauvegarde des urls de la console dans un Dictionnaire
            url_pages_consoles[console] = url_tmp 
            # Vide url_tmp
            url_tmp = []
    print()
    print("The recovery of pagination URLs is complete...")
    return url_pages_consoles


def get_url_games(url_pagination_dict):
    '''
        Allows retrieval of game URLs for each console
        Returns a dictionary containing all game URLs.
        url_pagination_dict => Dictionary containing all page urls relating to the console
        url_games_dict => Returns dictionary
    '''
    # Initialisation des variables
    html = ""
    url_tmp = []
    url_games_dict = {}
    # Parcours le Dictionnaire
    for key_console, list_page in url_pagination_dict.items():
        console = key_console
        print("RETRIEVING GAME URLS:")
        print("---------------------")
        print("For the console  : "+ console)
        # Boucle sur la liste des urls
        for link in list_page:
            # Utilisation de playwright
            with sync_playwright() as playwright:
                # lancer le navigateur
                browser = playwright.chromium.launch(headless=False)
                # Création de la page
                page = browser.new_page()
                page.goto(link, wait_until="domcontentloaded")
                # Pause pour laisser l'affichage se mettre en place
                page.locator('button.jad_cmp_paywall_cookies').click()
                html = page.content()
                browser.close()
            # Utilisation de  BeautifulSoup
            soup = BeautifulSoup(html, "html.parser")
            # Récuperation des urls
            bloc_link_games = soup.find_all("a", {"class" : "cardGameList__gameTitleLink"})
            for bloc_a in bloc_link_games:
                url = url_base + bloc_a['href']
                url_tmp.append(url)
                print(url)   
            # Sauvegarde des urls des jeux par console
        url_games_dict[console] = url_tmp
        url_tmp = []

    print()
    print("Retrieving game URLs is complete...")   
    return url_games_dict


def get_info_games(url_game_dict, site):
    '''
        Allows the recovery of information from each game.
        Creation of a json save file for each console
        url_game_dict => Dictionary which contains all the urls of console games
        site => site targeted for scraping
        games => Return dictionary containing all information
    '''
    print("RECOVERY OF GAMES INFORMATION :")
    print("------------------------------")
    # Initialisation des variables
    html = ""
    games = {}
    infogame = {}
    editeur = ""
    date_sortie = ""
    genre = ""
    cpt = 1
    date_now = date.today().strftime("%d-%m-%Y")
    # Boucle sur le Dictionnaire
    for key_console, link_game in url_game_dict.items():
        # Récupération de la console
        console = key_console
        print("For the console :  "+console)
        # Création des dossiers sauvegarde des images et info game
        if not os.path.exists("Data/Img/"+console):
            os.makedirs("Data/Img/"+console)
            print("Creating the folder for the imgs...")
        else :
            print("The file already exists...")    
        if not os.path.exists("Data/Json/"+site+"/"):
            os.makedirs("Data/Json/"+site)
            print("Creating the folder for the jsons...")
        else :
            print("The file already exists...")
        # Boucle sur la list des urls
        for link in link_game:
            # Utilisation de playwright
            with sync_playwright() as playwright:
                # lancer le navigateur
                browser = playwright.chromium.launch(headless=False)
                # Création de la page
                page = browser.new_page()
                page.goto(link, wait_until="domcontentloaded")
                # Pause pour laisser l'affichage se mettre en place
                page.locator('button.jad_cmp_paywall_cookies').click()
                html = page.content()
                browser.close()
            # Utilisation de  BeautifulSoup
            soup = BeautifulSoup(html, "html.parser")
            print('URL : '+link)
            # Titre
            bloc_title = soup.find("a", {"class" : "gameHeaderBanner__title"})
            title = bloc_title.text
            # Image & Download
            # utilisation de regex et remplace par " " tous caracteres speciaux sauf l'espace => re.sub(r'[^a-zA-Z0-9\s]', ' ', texte)
            title_img = re.sub(r'[^a-zA-Z0-9\s]', ' ', title)
            bloc_img = soup.find("img", {"class" : "gameCharacteristicsMain__coverImage"})
            if bloc_img['alt'] != "pas d'image":
                url_img = bloc_img['src']
                url_img_list = url_img.split(".")
                extension = url_img_list[-1]
                name_img = title_img+'.'+extension
                # Download img
                f = open("Data/Img/"+console+"/"+name_img, "wb")
                reponse = requests.get(url_img)
                f.write(reponse.content)
                f.close()
            else :
                url_img = ""
                name_img = ""
            # Description
            
            # Caracterisque
            tr = soup.find_all("div", {"class": "gameCharacteristicsDetailed__tr"})
            for i in range(len(tr)):
                # Editeur
                if "Editeur" in tr[i].find('div', {'class': 'gameCharacteristicsDetailed__td--th'}).text:
                    td_content = tr[i].find_all('div', {'class': 'gameCharacteristicsDetailed__td'})
                    edit = td_content[1].text.strip()
                    editeur = ' '.join(edit.split()) # suppprime les espace inutile
                # Sortie
                if "Sortie France" in tr[i].find('div', {'class': 'gameCharacteristicsDetailed__td--th'}).text:
                    td_content = tr[i].find_all('div', {'class': 'gameCharacteristicsDetailed__td'})
                    if td_content[1].text.strip() == "Date de sortie inconnue" :
                       date_sortie = "" 
                    else:
                        date_sortie = td_content[1].text.strip()
                # Genre
                if "Genre" in tr[i].find('div', {'class': 'gameCharacteristicsDetailed__td--th'}).text:
                    td_content = tr[i].find_all('div', {'class': 'gameCharacteristicsDetailed__td'})
                    gen = td_content[1].text.strip()
                    genre = ' '.join(gen.split())
            infogame[cpt] = {
                "title" : title,
                "editeur" : editeur,
                "genre" : genre,
                "name_img" : name_img,
                "date_sortie" : date_sortie,
                "console" : console
            }
            print("Game Information : ")
            print("-----------------")
            print('Titre : '+title)
            print('Editeur : '+editeur)
            print('Genre : '+genre)
            print('Name_img : '+name_img)
            print('Date_sortie : '+date_sortie)
            print('Console : '+console)
            cpt += 1
        # Sauvegarde dans un fichier json
        games[console] = infogame
        with open("Data/Json/"+site+"/"+console+".json", "w", encoding = 'utf-8') as file_json:
            json.dump(games, file_json, ensure_ascii = False, indent = 4)
        infogame = {}
        cpt = 1
    print("Scraping of the site: JEUXVIDEO is finished...")
    return games


def start_scrap(path_file, site):
    '''
        Allows the chaining of functions to be able to scrape the site
    '''
    print("Start of scraping for JEUXVIDEO")
    url_pagination = get_url_pagination(path_file)
    if len(url_pagination) > 0:
        url_games = get_url_games(url_pagination)
        if len(url_games) > 0:
            infogames = get_info_games(url_games, site)