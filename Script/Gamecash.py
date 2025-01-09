'''
    File allowing you to retrieve information on video games from the site: www.jeuxvideo.com
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
import json
import os


def get_url_genres(dict_url):
    '''
        Allows you to retrieve genre urls for the target console
        dict_url: Dictionary containing the name of the console and its url
        return urls_genre: Dictionary containing all the urls of the genres
    '''
    print("Retrieving URLs for genres :")
    print("---------------------------")
    # Initialisation des variables
    html = ""
    url_base = "https://www.gamecash.fr"
    urls_genre = {}
    url_tmp = {}
    # Boucle sur le dictionnaire d'url
    for key, urlcible in dict_url.items():
        # Recuperation du nom de la console
        console = key
        print("For the console :  "+console)
        print("The url is :  "+urlcible)
        # Vérification si urlcible n'est pas vide
        if urlcible != "":    
            # Utilisation d'un navigateur CHRONIUM pour simuler l'utilisateur
            with sync_playwright() as playwright:
                # Lancer le navigateur
                browser = playwright.chromium.launch(headless=False)
                # Création de la page
                page = browser.new_page()
                # Navigation à partir de l'urlcible
                page.goto(urlcible)
                page.get_by_label("Accepter les cookies", exact=True).click()
                page.wait_for_timeout(2000)
                page.get_by_role("link", name="Voir plus d'éléments").click()
                page.wait_for_timeout(2000)
                html = page.content()
                browser.close()

            # Parser la response
            soup = BeautifulSoup(html, 'html.parser')
            bloc_container = soup.find("div", {"class": "list-container"})
            # Récupération du bloc contenant tous les genres
            links_genre = bloc_container.find_all("li")

            # Boucle sur les balise pour répérer le href
            for links in links_genre:
                # Récupération tous les balises a contenu dans le bloc
                link = links.find( "a", {"class" :"main-link"})
                if link != None:     
                    # Construction de l'url en concatenant l'url du site + celui de la page
                    url = link['href']
                    url_genre = url_base+url
                    # Récuperation du nom du genre
                    genre = link.text
                    # Ajout dans le dictionnaire tmp {genre: url}
                    url_tmp[genre] = url_genre
                    print("Genre is :  "+genre)
                    print("The url is :  "+ url_genre)

            # Ajout du dict tmp dans le dictionnaire de retour {console : {tmp}}
            urls_genre[console] = url_tmp
        else:
            print("No url available for console : "+console)    
    # Message pour dire que c'est terminée
    print("The recovery of urls for genres is complete...")
    # renvoi du dictionnaire
    return urls_genre


def get_url_pages(dict_genres):
    '''
        Allows you to retrieve the URLs of all game genre pages on the targeted console
        dict_genre: Dictionary coming from the get_url_genres() function
        return url_page_genres: Dictionary {console: {genre1: [url1, url2,..]}}
    '''
    print("Retrieving page URLs for genres :")
    print("--------------------------------")
    # Initialisation des variables
    html = ""
    url_base = "https://www.gamecash.fr"
    list_tmp = []
    page_genre = {}
    url_page_genres = {}
    # Boucle sur le dictionaire
    for key, dict_genre in dict_genres.items():
        # Récupération de la console
        console = key
        print("For the console :  "+console)
        # Boucle sur le dictionnaire genre
        for g, urlcible in dict_genre.items():
            # Récuperation du genre
            genre = g
            print("For the genre :  "+genre)
            print("The url is :  "+urlcible)
            # Utilisation d'un navigateur CHRONIUM pour simuler l'utilisateur
            with sync_playwright() as playwright:
                # Lancer le navigateur
                browser = playwright.chromium.launch(headless=False)
                # Création de la page
                page = browser.new_page()
                # Navigation à partir de l'urlcible
                page.goto(urlcible)
                page.wait_for_timeout(2000)
                page.get_by_label("Accepter les cookies", exact=True).click()
                page.wait_for_timeout(2000)
                html = page.content()
                browser.close()
            
            # Parser la response
            soup = BeautifulSoup(html, 'html.parser')
            # Récupération du blooc de pagination
            block_pagination = soup.find("a", {"class" : "jsPagingLink next goLast"})
            # Vérification si ! None
            if block_pagination != None:
                print("pagination present")
                # Récupératin du nb pages avec rel=
                rel = block_pagination['rel']
                nbpages = int(rel[0])
                # Récupération de l'url pour le template
                link_template = block_pagination['href']
                # Boucle sur le nb pages +1
                print("Lists of urls : ")
                print("---------------")
                for i in range(1, nbpages+1):
                    urltmp = link_template[:-9]
                    # construction de l'url urlsite+url_tmp+-p+i+.html
                    url_page_genre = url_base+urltmp+"-p"+str(i)+".html"
                    # Ajout dans la list list_tmp
                    list_tmp.append(url_page_genre)
                    print(url_page_genre)
                # Ajout des url dans le dictionnaire {genre:list_tmp}
                page_genre[genre] = list_tmp
                # Réinitialisation de liste_tmp à vide
                list_tmp = []
                print()
            else:
                print("pagination not present")
                # Ajout dans la list list_tmp
                list_tmp.append(urlcible)
                print("The url is :  ")
                print("----------- ")
                print(urlcible)
                print()
                # Ajout de l'url dans dictionnaire {genre:url}
                page_genre[genre] = list_tmp
                list_tmp = []
        # Ajout dans dict de retour {console: {dictionnaire genre}}
        url_page_genres[console] = page_genre
    # Message pour avertir que l'on a terminé
    print("The recovery of URLs of each genre is complete...")
    # Retourne le dictionnaire
    return url_page_genres


def get_url_games(dict_urlpages):
    '''
        Allows the retrieval of all game URLs by genre for the targeted console
        dict_urlpages: Dictionary coming from the get_url_pages() function
        return url_games: Dictionary {console: {genre: [urlgame1, urlgame2]}}
    '''
    print("Retrieving game URLS :")
    print("---------------------")
    # Initialisation des variables
    url_base = "https://www.gamecash.fr"
    html = ""
    list_games = []
    url_games_genre = {}
    url_games = {}
    # Boucle sur le dictionnaire pages
    for key_console, dict_pages in dict_urlpages.items():
        # Recuperation de la console
        console = key_console
        print("For the console :  "+console)
        # Boucle sur le dictionnaire genre
        for key_genre, list_url in dict_pages.items():
            # Récupération du genre
            genre = key_genre
            print("For the genre :  "+genre)
            # Vérification de la longueur de la list
            if len(list_url) > 1:
                print("I have more than one page like this")
                # Boucle sur la list url
                for link in list_url:
                    print("The url is :  "+link)
                    # Requête pour avoir le html
                    with sync_playwright() as playwright:
                        # Lancer le navigateur
                        browser = playwright.chromium.launch(headless=True)
                        # Création de la page
                        page = browser.new_page()
                        # Navigation à partir de l'urlcible
                        page.goto(link)
                        page.wait_for_timeout(2000)
                        page.get_by_label("Accepter les cookies", exact=True).click()
                        page.wait_for_timeout(3000)
                        html = page.content()
                        browser.close()
                    # Parser la reponse
                    soup = BeautifulSoup(html, "html.parser")
                    # Récuperation de tous les cards
                    block_games = soup.find_all("li", {"class" : "product-item"})
                    # Vérification si pas non vide
                    if block_games != None:
                        print("There are games on the page")
                        # Boucle sur la récupération
                        print("list of urls for this page : ")
                        print("---------------------------")
                        for game in block_games:
                            # Récupération du bloc stock
                            block_stock = game.find("div", {"class" : "stock noStock"})
                            # Vérification de l'existance du block_stock
                            if block_stock == None:
                                print("Games available")
                                # Récupération de la la balise a
                                bloc_link = game.find("a", {"class" : "title"})
                                # Récupération du href
                                url = url_base + bloc_link['href']
                                print(url)
                                # Ajout de l'url dans une liste
                                list_games.append(url)
                            else:
                                print("Games unavailable")
                        print()
            else:
                print("I only have one page for this type")
                print("The url is :  "+list_url[0])
                with sync_playwright() as playwright:
                    # Lancer le navigateur
                    browser = playwright.chromium.launch(headless=False)
                    # Création de la page
                    page = browser.new_page()
                    # Navigation à partir de l'urlcible
                    page.goto(list_url[0])
                    page.wait_for_timeout(2000)
                    page.get_by_label("Accepter les cookies", exact=True).click()
                    page.wait_for_timeout(3000)
                    html = page.content()
                    browser.close()
                # Parser la reponse
                soup = BeautifulSoup(html, "html.parser")
                # Récuperation de tous les cards
                block_games = soup.find_all("li", {"class" : "product-item"})
                # Vérification si pas non vide
                if block_games != None:
                    print("There are games on the page")
                    print("List of URLS for this page : ")
                    print("--------------------------------")
                    # Boucle sur la récupération
                    for game in block_games:
                        # Récupération du bloc stock
                        block_stock = game.find("div", {"class" : "stock noStock"})
                        # Vérification de l'existance du block_stock
                        if block_stock == None:
                            print("Game available")
                            # Récupération de la la balise a
                            bloc_link = game.find("a", {"class" : "title"})
                            # Récupération du href
                            url = url_base + bloc_link['href']
                            print(url)
                            # Ajout de l'url dans une liste
                            list_games.append(url)
                        else:
                            print("Game unavailable")
                    print()        
            # Ajout de la liste dans dictionnaire genre {genre: liste}
            url_games_genre[genre] = list_games
            # Réinitialisation de la liste à vide
            list_games = []
        # Ajout du dictionnaire genre dans le dictionnaire de retour {console: {dict_genre}}
        url_games[console] = url_games_genre
    # Message pour avertir que c'est terminé
    print("Retrieving URLs for games is complete...")
    return url_games


def get_info_games(dict_games, site):
    print("Retrieving game information :")
    print("----------------------------------------")
    # Initialisation des variables
    today = date.today()
    html = ""
    url_base = "https://www.gamecash.fr"
    info_games = {}
    info_console = {}
    cpt = 1
    # Création du dossier du site
    print("Creating the backup folder :")    
    if not os.path.exists("Data/Json/"+site+"/"):
        os.makedirs("Data/Json/"+site)
        print("    The backup folder has been created...")
    else:
        print("    Backup folder already exists...")
    
    # boucle sur le dictionnaire
    for key_console, dict_genre in dict_games.items():
        # Recuperation de la console
        console = key_console
        print("For the console  : "+console)
        # Boucle sur le dict_genre
        for key_genre, list_games in dict_genre.items():
            # Récupération du genre
            genre_g = key_genre
            print("For the genre :  "+genre_g)
            # Boucle sur la list_url
            print("The information is :  ")
            print("-----------------------")
            # Vérification de la list_games
            if len(list_games) > 0:
                for games in list_games:
                    print("The url is :  " + games)
                    sorti = "---"
                    editeur = "---"
                    genre = "---"
                    # Requête pour avoir le html
                    with sync_playwright() as playwright:
                        # Lancer le navigateur
                        browser = playwright.chromium.launch(headless=False)
                        # Création de la page
                        page = browser.new_page()
                        # Navigation à partir de l'urlcible
                        page.goto(games)
                        page.wait_for_timeout(2000)
                        page.get_by_label("Accepter les cookies", exact=True).click()
                        page.wait_for_timeout(2000)
                        html = page.content()
                        browser.close()
                    # Vérification du retour de la console
                    soup = BeautifulSoup(html, "html.parser")
                    # Récuperation du bloc titre
                    block_title = soup.find("h1", {"itemprop" : "name"})
                    # Récuperation du bloc image
                    block_image = soup.find("img", {"itemprop" : "image"})
                    # Récuperation du bloc description
                    block_description = soup.find("div", {"itemprop" : "description"})
                    # Récuperation du bloc price
                    block_price = soup.find("meta", {"itemprop" : "price"})
                    # Récuperation du bloc info
                    block_info = soup.find("div", {"class" : "blockInfos"})
                    # Récuperation des li depuis bloc info
                    all_li = block_info.find_all("li")
                    # Récupération du contenu des bloc
                    # TITLE
                    title = block_title.text
                    # PRICE
                    price = block_price['content']
                    # URL_IMG
                    if block_image == None:
                        url_img = "---"
                    else:
                        url_img = url_base + block_image['src']
                    for li in all_li:
                        label = li.find("span", {"class" : "label"})
                        if "Editeur" in label.text:
                            editeur_tmp = li.find("span", {"class" : "value"})
                            editeur = editeur_tmp.text
                        if "Genre" in label.text:
                            genre_tmp = li.find("span", {"class" : "value"})
                            genre = genre_tmp.text
                        if "Date de sortie" in label.text:
                            sortie_tmp = li.find("span", {"class" : "value"})
                            sorti = sortie_tmp.text
                    print("TITRE =>  " +title)
                    print("PRICE =>  " +price)
                    print("URL_IMG =>  " +url_img)
                    print("EDITEUR =>  " +editeur)
                    print("GENRE  => "+genre)
                    print("DATE SORTIE => " + sorti)
                    print("URL_GAME  =>  "+ games)
                    print()
                    # Ajout dans un dictionnaire {1: {les infos}}
                    info_games[cpt] = {"title" : title,
                                        "price" : price,
                                        "editeur" : editeur,
                                        "genre" : genre,
                                        "name_img" : "",
                                        "date_sortie" : sorti,
                                        "url_img" : url_img,
                                        "url_game": games
                                        }
                    cpt += 1
            else:
                print("No games for this genre")      
        # Ajout des jeux dans le dictionnaire de retour {console : {game}}
        info_console[console] = info_games
        date_now = date.today().strftime("%d-%m-%Y")
        with open("Data/Json/"+site+"/"+console+'_'+date_now+".json", "w", encoding = 'utf-8') as file_json:
            json.dump(info_console[console], file_json, ensure_ascii = False, indent = 4)
        print(f"Creation of {console} json completed")
        info_games = {}
        cpt = 1
        
    # Message pour avertir que c'est terminé
    print(f"Scraping is complete for the console : {console}")
    return info_console


def start_scrap(urls, site):
    print("Start of scraping for GAMECASH")
    # Récup des genres
    url_genres = get_url_genres(urls)
    # Vérification de la longueur du dictionnaire
    if len(url_genres) > 0:
        # Récuperation des pages
        url_page_genres = get_url_pages(url_genres)
        # Vérification de la longueur du dictionnaire
        if len(url_page_genres) > 0:
            # Récupération des games
            url_games = get_url_games(url_page_genres)
            # Vérification de la longueur du dictionnaire
            if len(url_games) > 0:
                infos = get_info_games(url_games, site)
                