'''
    File allowing you to retrieve information on video games from the site: www.micromania.com
    The following functions are used to:
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
    print("Retrieving page URLS :")
    print("---------------------")
    # initialisation des variables
    html=""
    url_tmp = []
    dict_url_pages = {}
    # Boucle sur le dict_url
    for key_console, link in dict_url.items():
        # Récuperation de la console
        console = key_console
        print(f"For the console : ")
        print("------------------")
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
            print("List of URLS :")
            print("--------------")
            # On ajout la premiere page
            url_tmp.append(link)
            print(link)
            # on boucle sur le nb_total pour construire l'url en commence à 2
            for i in range(2,nbtotal+1):
                # Construction de l'url    
                url = link+'?page='+str(i)
                print(url)
                # on ajoute l'url dans url_tmp
                url_tmp.append(url)
        else:
            print(f"No URL available for the console : {console}")
        dict_url_pages[console] = url_tmp
        url_tmp = []
        print(f"Retrieving page URLs for {console} is complete...")
    return dict_url_pages


def get_url_games(dict_url_page):
    print("Retrieving game URLS :")
    print("---------------------")
    # Initialisation des variables
    url_tmp = []
    dict_url_games = {}
    # Boucle sur dict_url_page
    for key_console, links in dict_url_page.items():
        # recuperation de la console
        console = key_console
        print(f"For the console : {console}")
        # boucle sur les links
        for link in links:
            # utilisation playwrigth
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
            # recuperation des urls
            blocks_link = soup.find_all("span", {"class" : "url"})
            print("List of URLS :")
            print("-------------")
            # boucles sur les urls
            for block in blocks_link:
                url = block.text
                # ajout dans list_tmp
                url_tmp.append(url)
                print(url)
        # ajout dans le dictionnaire avec key = console
        dict_url_games[console] = url_tmp
        url_tmp = []
    print(f"Retrieving game URLs for {console} is complete...")
    return dict_url_games


def get_info_games(dict_url_games, site):
    print("RECOVERY OF GAMES INFORMATION :")
    print("------------------------------")
    # Initialisation des variables
    games = {}
    infogame = {}
    cpt = 1
    html = ''
    date_now = date.today().strftime("%d-%m-%Y")
    # Création du dossier sauvegarde
    if not os.path.exists("Data/Json/"+site+"/"):
        os.makedirs("Data/Json/"+site+"/")
        print("Creating the folder for the jsons...")
    else:
        print("The file already exists...")
        
    # boucle sur dict_url_games
    for key_console, links in dict_url_games.items():
        console = key_console
        print(f"For the console :  {console}")
        # boucle sur links
        for link in links:
            # utilisation de playwright
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
            print('URL : '+link)
            # Récupération du titre
            block_title = soup.find("h1", {"class" : "pdp-product-name mm-m-b-5 mb-lg-2 fs-14 color-light-navy futura-demi-font-family"})
            title_tmp = block_title.text
            title_tmp = title_tmp.split("-")
            title = title_tmp[0].strip()
           
            # Récuperation du prix
            block_price = soup.find("span", {"class" : "value"})
            price = block_price['content']

            # Recuperation des caractéristiques
            bloc_info = soup.find("div", {"id" : "detailTabCharacteristics"})
            table_info = bloc_info.find("table" , {"class" : "table table-striped w-100"})
            tr = table_info.find_all("tr")

            # Boucle sur les tr
            for i in range(len(tr)):
                if "Éditeur" in tr[i].find('td', {'class': 'text-uppercase font-fdemi color-dark-gray fs-10 pl-2 pr-2 pl-md-3 pr-md-0 py-2'}).text:
                    td_content = tr[i].find('td', {'class': 'font-eregular'})
                    editeur = td_content.text
                    if editeur == "PRODUITS RECYCLES":
                        editeur = ""
                    
                if "DATE DE SORTIE" in tr[i].find('td', {'class': 'text-uppercase font-fdemi color-dark-gray fs-10 pl-2 pr-2 pl-md-3 pr-md-0 py-2'}).text:
                    td_content = tr[i].find('td', {'class': 'font-eregular'})
                    date_sortie = td_content.text
                    
                if "GENRE" in tr[i].find('td', {'class': 'text-uppercase font-fdemi color-dark-gray fs-10 pl-2 pr-2 pl-md-3 pr-md-0 py-2'}).text:
                    td_content = tr[i].find('td', {'class': 'font-eregular'})    
                    genre = td_content.text
            
            # Ajoute dans le dictionnaire
            infogame[cpt] = {
                "title" : title,
                "editeur" : editeur,
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
            print('Editeur : '+editeur)
            print('Price : '+price)
            print('Genre : '+genre)
            print('Name_img : ')
            print('Date_sortie : '+date_sortie)
            print('Console : '+console)

            cpt += 1
        # Sauvegarde dans un fichier json
        games[console] = infogame
        with open("Data/Json/"+site+"/"+console+"_"+date_now+".json", "w", encoding = 'utf-8') as file_json:
            json.dump(games, file_json, ensure_ascii = False, indent = 4)
        infogame = {}
        cpt = 1
    print("Scraping of the site: JEUXVIDEO is finished...")
    return games


def start_scrap(url, site):
    '''
        Allows the chaining of functions to be able to scrape the site
    '''
    print(f"Start of scraping for {site}")
    url_pages = get_url_pages(url)
    if len(url_pages) > 0:
        url_games = get_url_games(url_pages)
        if len(url_games) > 0:
            infogames = get_info_games(url_games, site)
