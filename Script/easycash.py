'''
    File allowing you to retrieve information on video games from the site: www.easycash.com
    The following functions are used to:
        - get_url_genres(): Retrieves the genre urls for the target console
        - get_url_pages(): Retrieves the urls of pages of each genre for the targeted console
        - get_url_games(): Retrieves the game urls for each genre for the target console
        - get_info_games(): Retrieves information about each game by genre for the target console
        - start_scrap(): allows the sequence of previous functions for scraping the site
'''


from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from datetime import date
import math
import json
import os


def get_url_pages(dict_url):
    '''
        Allows the retrieval of URLs of the pages of the targeted console
        dict_url => Dictionary containing the name of the console and its url
        return url_pages_console => Dictionary containing all the urls of the pages of the targeted console
    '''
    # Initialisation des varables
    html = ''
    url_tmp = []
    url_pages_console = {}
    print("Retrieving page URLS : ")
    print("---------------------")
    # Boucle sur le dictionnaire
    for key_console, link in dict_url.items():
        # Récupération du nom de la console
        console = key_console
        print(f"For the console : {console}")
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
            print("List of URLS : ")
            print('-------------')
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
            print("No url for this console, check the file dedicated to urls")

    print()
    print(f"Retrieving page URLS is complete...")
    return url_pages_console


def get_url_games(dict_pages):
    '''
        Allows the recovery of video game URLs for the targeted console
        dict_pages => Dictionary containing the urls coming from the get_url_pages() function
        return url_games => Dictionary containing all video game urls
    '''
    # Initialisation des variables
    html = ''
    url_tmp = []
    url_games = {}
    # Boucle sur le dictionnaire
    for key_console, list_page in dict_pages.items():
        console = key_console
        print("Retrieving game URLS :")
        print("---------------------")
        print(f"For the console :  {console}")
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
            print("List of game URLS :")
            print("------------------")
            for bloc in all_bloc_li:
                url = bloc['data-href']
                print(url)
                url_tmp.append(url)
        # Ajout dans le dictionnaire
        url_games[console] = url_tmp
        url_tmp = []

    print()
    print("Retrieving game URLs is complete...")
    return url_games



def get_info_games(dict_games, site):
    '''
        Allows the recovery of information on video games on the targeted console
        games => Dictionary containing game information
        return infogames => Dictionary containing all the games on the target console
    '''
    print("Retrieving game information :")
    print("----------------------------")
    # Initialisation des variables
    html = ''
    games = {}
    infogames = {}
    cpt = 1
    date_now = date.today().strftime("%d-%m-%Y")
    # Creation du dossier de sauvegarde
    if not os.path.exists("Data/Json/"+site+"/"):
        os.makedirs("Data/Json/"+site+"/")
        print("Creating the backup folder successfully...")
    else:
        print("The backup folder already exists...")
    # Boucle sur le dictionnaire
    for key_console, link_game in dict_games.items():
        # Récupération du nom de la console
        console = key_console
        print(f"For the console : {console}")
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
                page.locator('button#onetrust-accept-btn-handler').click()
                html = page.content()
                browser.close()
            # Utilisation de  BeautifulSoup
            soup = BeautifulSoup(html, "html.parser")
            print(f"Url : {link}")
            # Le titre
            bloc_title = soup.find("h1", {"class" : "block-product--title"})
            title = bloc_title.text.replace("Jeux Vidéo", "").strip()
            
            # Le prix
            bloc_price = soup.find("span", {"class" : "price"})
            price = bloc_price.text
            
            # Récupération des caractéristiques (sauf pour Atari il n'y en a pas)
            table_info = soup.find("table", {"class" : "table-description"})
            all_tr = table_info.find_all("tr")
            # Vérification de la taille de all_tr si superieur à 1
            # Car si un seul tr c'est le nom de la console
            genre = ''
            date_sortie = ''
            if len(all_tr) > 1:
                for i in range(len(all_tr)):
                    # Genre
                    if "Genre" in all_tr[i].find('th').text:
                        td_content = all_tr[i].find('td')
                        genre = td_content.text.strip()
                    # Date de sortie
                    if "Date de sortie approximative" in all_tr[i].find('th').text:
                        td_content = all_tr[i].find('td')
                        date_sortie = td_content.text.strip()

            else:
                print("No features for this game..")
            # Sauvegarde des données
            games[cpt] = {
                "title" : title,
                "editeur" : "",
                "price" : price,
                "genre" : genre,
                "name_img" : "",
                "date_sortie" : date_sortie,
                "console" : console,
                "url_game" : link
            }

            print("Game Information : ")
            print("-----------------")
            print('Titre : '+title)
            print('Editeur : ')
            print('Price : '+price)
            print('Genre : '+genre)
            print('Name_img : ')
            print('Date_sortie : '+date_sortie)
            print('Console : '+console)

            cpt += 1
        # Sauvegarde dans un fichier json
        infogames[console] = games
        with open("../Data/Json/"+site+"/"+console+"_"+date_now+".json", "w", encoding = 'utf-8') as file_json:
            json.dump(games, file_json, ensure_ascii = False, indent = 4)
        games = {}
        cpt = 1
    print(f"Scraping of the site: {site} is finished...")
    return games


def start_scrap(dict_url, site):
    print("Start of Easycash scrapping")
    url_pages = get_url_pages(dict_url)
    if len(url_pages) > 0:
        url_games = get_url_games(url_pages)
        if len(url_games) > 0:
            info = get_info_games(url_games, site)
