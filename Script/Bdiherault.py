'''
    File allowing you to retrieve information on video games from the site: www.jeuxvideo.com
    The following functions are used to:
      - get_url_pages : Retrieves all video game page URLS for the targeted console
      - get_url_games : Retrieves all video game URLs for the targeted console
      - get_info_game : Retrieves information from all video games for the targeted console
      - start_games   : allows the sequence of previous functions for scraping the site 
'''

from bs4 import BeautifulSoup
from datetime import date
import Service.FileService as f_serve
import requests
import math
import json
import os


def get_url_pages(dict_url):
    '''
        Allows retrieval of URLs of all pages of the targeted console
        dict_url => Dictionary containing console name => url
        return urls_pages_consoles => Dictionary containing all urls
    '''
    print("Retrieving page URLs :")
    print("---------------------")
    # Initialisation des variables
    urls_pages_console = {}
    url_tmp = []
    # Boucle sur le dictionnaire
    for key_console, link in dict_url.items():
        console = key_console
        print("For the console :  "+console)
        # Vérification si link n'est pas vide
        if link != "":
            response = requests.get(link)
            # Vérification du retour de la requête
            if response.ok:
                # Parsement de la page
                soup = BeautifulSoup(response.text, "html.parser")
                # Récupération du bloc pagination
                block_paginate = soup.find("select", {"class" : "custom-select custom-select-sm w-auto mx-2"})
                # Vérification si on a bien block_paginate
                if block_paginate:
                    print("Pagination present")
                    # recuperation du nombre de jeux total
                    block_content_ref = soup.find("div", {"class" : "col-lg-6 mb-3 mb-lg-0"})
                    block_nb_ref = block_content_ref.find("span", {"class" : "font-size-1 ml-1"})
                    ref_array = block_nb_ref.text.split(" ")
                    # diviser par 64 car il y a 64 jeu par page
                    nb_ref = math.ceil(int(ref_array[0]) / 64)
                    # Recuperation de la reference console dans l'url (link) 
                    # 'https://bdi-herault.com/?sc[]=101' ici 101
                    ref_console_array = link.split("=")
                    ref_console = ref_console_array[1]
                    # Ajout de la premiere page dans url_tmp
                    url_tmp.append(link)
                    print("LIST OF URLS : ")
                    print("----------------")                    
                    # Construction des urls selon le nb_ref
                    for nb in range(2, nb_ref + 1):
                        # Multiplication de i par 64 puis on enleve les 64 présent sur la page
                        nb_tmp = (nb * 64) - 64
                        url = "https://bdi-herault.com/?sc[]="+ref_console+"&from="+str(nb_tmp)
                        url_tmp.append(url)
                        print(url)
                    print()
                else: 
                    print("No pagination present")
                    print("LIST OF URLS  : ")
                    print("-----------------")
                    # On ajoute l'url courante
                    url_tmp.append(link)
                    print(link)
                    print()
                urls_pages_console[console] = url_tmp
            else:
                # Problème d'url ou erreur de la requete
                print("Problem with method or url")
                print("Error  : "+str(response.status_code))
        else:
            # Pas d'url recensé pour la console
            print("I don't have a URL for this console :    "+console)
    print("RECOVERY OF PAGE URLS COMPLETED...")

    return urls_pages_console


def get_url_games(dict_pages):
    '''
        Retrieves all video game URLs for the targeted console
        dict_pages   : Dictionary coming from the get_url_pages function
        return games : Dictionary containing the urls of games for the console
    '''
    print("RECOVERY OF GAME URLS BY CONSOLE :")
    print("---------------------------------")
    # INITIALISATION DES VARIABLES
    urltmp = []
    games = {}
    # Boucle du le dictionnaire des pages
    for key_console, list_pages in dict_pages.items():
        console = key_console
        print("For the console :    "+console)
        print("------------------------------")
        # Boucle sur la list d'url
        for link in list_pages:
            response = requests.get(link)
            # Vérification du retour de la requête
            if response.ok:
                soup = BeautifulSoup(response.text, "html.parser")
                # Récupération des card des jeux
                blocks_body = soup.findAll("div", {"class" : "card-body pt-4 px-4 pb-0"})
                print("LIST OF URLS :")
                print("-------------")
                # Boucle sur les cards
                for block in blocks_body:
                    block_a = block.find("a", {"class" : "text-inherit"})
                    url = block_a['href']
                    urltmp.append(url)
                    print(url)
                print()
            else:
                # Problème avec l'url ou la méthode
                print("Problem with url or method")
                print("Error : "+str(response.status_code))
        games[console] = urltmp
        urltmp = []
    
    print("RECOVERY OF GAME URLS COMPLETED...")
    return games


def get_info_game(dict_games, site):
    '''
        Allows the recovery of information from all video games on the targeted console.
        Create a data backup json file in order to validate by the administrator
        dict_games   : Dictionary from the get_url_games function
        site         : Name of the targeted site
        return games : Dictionary containing information about games on the target console
    '''
    print("RETRIEVING GAME INFORMATION :")
    print("----------------------------")
    # Initialisation des variables
    games = {}
    infogame = {}
    cpt = 1
    date_now = date.today().strftime("%d-%m-%Y")
    # Boucle sur le dictionnaire urls jeux
    for key_console, list_games in dict_games.items():
        console = key_console
        # Création du dossier du site
        if not os.path.exists("Data/Json/"+site):
            os.makedirs("Data/Json/"+site)
            print("Created backup folder successfully...")
        else:
            print("Backup folder already exists...")
        
        print("For the console :  "+console)
        print("-----------------------------")
        print("GAME INFORMATION :  ")
        for link in list_games:
            etat = " "
            print("The URL of the game :  "+link)
            print("-----------------------------")
            response = requests.get(link)
            # Vérification de la requete
            if response.ok:
                soup = BeautifulSoup(response.text, "html.parser")
                # titre
                title_tmp = soup.find("h1", {"class" : "h2"})
                title_tmp = title_tmp.text.lstrip()
                # Etat
                list_title = title_tmp.split(" ")
                if list_title[-1] == "ntsc":
                    list_etat = list_title[-4:]
                    etat = list_etat[1]
                    title = " ".join(list_title[0:-4])
                if list_title[-1] == '(IMPORT)':
                    list_etat = list_title[-3:]
                    etat = list_etat[1]
                    title = " ".join(list_title[0:-3])
                if list_title[-1] == 'Loose' or list_title[-1] == 'Boite':
                    list_etat = list_title[-2:]
                    etat = list_etat[1]
                    title = " ".join(list_title[0:-2])
                else:
                    title = " ".join(list_title)
                # image
                image_tmp = soup.find("img", {"class" : "img-fluid w-100 rounded"})
                if image_tmp == None:
                    image = " "
                else:
                    image = image_tmp['src']
                # prix
                price_tmp = soup.find("span", {"class" : "text-dark font-size-2 font-weight-bold"})
                price = price_tmp.text
                price = price.replace(" €", "")   

                print("TITLE  =>  "+title)
                print("PRICE  =>  "+price)
                print("URL_IMG  =>  "+image)
                print("EDITEUR  =>  ")
                print("NAME_IMG  =>  ")
                print("GENRE  => ")
                print("DATE SORTIE => ")
                print("ETAT => ")
                print("URL_GAME  =>  "+ link)
                infogame[cpt]  = {
                    "title" : title, 
                    "price" : price,
                    "editeur" : "",
                    "genre" : "",
                    "name_img" : "",
                    "date_sortie" : "",
                    "etat" : etat,
                    "url_img" : "",
                    "url_game" : link
                    }
                cpt += 1
            else:
                print("Problem with url or method")
                print("Error :  "+str(response.status_code))
        games[console] = infogame
        infogame = {}
        cpt = 1
    with open("Data/Json/"+site+"/"+console+"_"+date_now+".json", "w", encoding = 'utf-8') as file_json:
            json.dump(games, file_json, ensure_ascii = False, indent = 4)
    print("Creation of backup file for the "+console+" completed")
    print("RECOVERY OF COMPLETED INFORMATION...")
    return games


def start_scrap(urls, site):
    print("Start of scraping for BDIHERAULT")
    # Début du scraping    
    url_pages = get_url_pages(urls)
    if len(url_pages) > 0:
        url_games = get_url_games(url_pages)
        if len(url_games) > 0:
            info = get_info_game(url_games, site)
            print(info)
            