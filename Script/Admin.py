'''
    Script réserve pour l'administrateur afin de pouvoir :
        - Completed_file() => Permet de completer les informations des jeux d'une console et un site donnée.
          Il recrée un fichier json avec le même nom du fichier passé en paramêtre
            Cette fonction utilise :
                - merge_info_games() => Complete les informations du jeux
                - update_file() => Créer un dictionnaire avec toutes les informations
        - Verification_data() => Permet de valider les données scraper d'une console visée
        - Export_excel_by_console() => Permet la création d'un fichier excel à partir de la console donnée
        - Export_excel_all() => Permet la création d'un fichier excel avec toutes les console du site donnée.
'''
from datetime import date
import Service.FileService as f_serve
import shutil, os
import xlsxwriter
import json


def merge_info_games(filename_site, name_site, console):
    '''
        Permet de trouver les jeux en commun avec le site de référence et retourne un dictionnaire
        contenant les jeux en commun avec les informations modifier
        filename_site => nom du fichier à completer
        name_site => nom du site visé
        console => nom de la console visée
        return : merge_game => le dictionnaire contenant les jeux modifiés
    '''
    print(f"Début de la recherche de jeux en commun pour la console :  {console}")
    # Initialisation des variables
    # Compteur
    cpt_site = 1
    cpt_ref  = 1
    # Dictionnaire
    merge_tmp  = {}
    merge_game = {}

    # Lecture des fichiers (fichier référence et celui du site)
    ref  = f_serve.readJson(f"Data/Json/Jeuxvideo/{console}.json")
    site = f_serve.readJson(f"Data/Json/{name_site}/{filename_site}")

    # Boucle
    while cpt_site <= len(site[console]) and cpt_ref <= len(ref[console]):
        # Vérification de l'égalité des titres
        if ref[console][str(cpt_ref)]['title'].lower() == site[console][str(cpt_site)]['title'].lower():
            print(f"Jeux commun :  {ref[console][str(cpt_ref)]['title']}")
            # Titre
            title = ref[console][str(cpt_ref)]['title']
            # Editeur
            if ref[console][str(cpt_ref)]['editeur'] != site[console][str(cpt_site)]['editeur']:
                print("Editeur sont différent")
                if site[console][str(cpt_site)]['editeur'] == "":
                    editeur = ref[console][str(cpt_ref)]['editeur']
                else:
                    editeur = site[console][str(cpt_site)]['editeur']
            # Genre
            if ref[console][str(cpt_ref)]['genre'] != site[console][str(cpt_site)]['genre']:
                print("Genre sont différent")
                if site[console][str(cpt_site)]['genre'] == "":
                    genre = ref[console][str(cpt_ref)]['genre']
                else:
                    genre = site[console][str(cpt_site)]['genre']
            # Name img
            if ref[console][str(cpt_ref)]['name_img'] != site[console][str(cpt_site)]['name_img']:
                print("Nom de l'image sont différent")
                if site[console][str(cpt_site)]['name_img'] == "":
                    name_img = ref[console][str(cpt_ref)]['name_img']
                else:
                    name_img = site[console][str(cpt_site)]['name_img']
            # Date de sortie
            if ref[console][str(cpt_ref)]['date_sortie'] != site[console][str(cpt_site)]['date_sortie']:
                print("La Date de sortie sont différent")
                if site[console][str(cpt_site)]['date_sortie'] == "":
                    date_sortie = ref[console][str(cpt_ref)]['date_sortie']
                else:
                    date_sortie = site[console][str(cpt_site)]['date_sortie']
            # Ajout dans le dictionnaire temporaire
            merge_tmp = {
                "title" : title,
                "price" : site[console][str(cpt_site)]['price'],
                "editeur" : editeur,
                "genre" : genre,
                "name_img" : name_img,
                "date_sortie" : date_sortie,
                "etat" : site[console][str(cpt_site)]['etat'],
                "url_img" : "",
                "url_game" : site[console][str(cpt_site)]['url_game']
            }
        
            print("Nouvelle donnée du jeu :")
            print("------------------------")
            print(merge_tmp)
            # Ajoute dans le dictionnaire
            merge_game[cpt_site] = merge_tmp
            merge_tmp = {}
            # Incrementation du compteur site
            cpt_site += 1
        else:
            # On passe au jeu suivant du site reference
            cpt_ref += 1
        # Cas si on arrive à la fin du fichier ref
        if cpt_ref >= len(ref[console]):
            cpt_site +=1    
            cpt_ref = 1
    
    return merge_game


def update_file(dict_merge, filename_site, name_site, console):
    '''
        Permet de reconstruire le dictionnaire correspondant au fichier json passé en paramêtre.
        dict_merge => dictionnaire provenant de la fonction merge_info_game()
        filename_site => nom du fichier de la console du site visé
        name_site => nom site visé
        console => nom de la console
        return : dict_game => dictionnaire contenant tous les jeux
    '''
    # Initialisation des variables
    dict_tmp  = {}
    dict_game = {}

    # Lecture du fichier passé en paramêtre
    site = f_serve.readJson(f"Data/Json/{name_site}/{filename_site}")

    # Boucle sur le fichier et sur dict_merge
    for key, game in site[console].items():
        for k, g in dict_merge.items():
            # Vérification de l'égalité de key
            if key == str(k):
                print("On a une correspondance")
                dict_tmp[key] = g
            else:
                # Pas d'égalité alors on sauvegarde le jeu du fichier
                dict_tmp[key] = game
    
    # Sauvegarde dans le dictionnaire
    dict_game[console] = dict_tmp

    return dict_game


def completed_file(filename_site, name_site, console):
    '''
        Permet l'ecriture du nouveau fichier json avec les nouvelles informations des jeux
        On utilise merge_info_games() et update_file()
    '''
    # Initialisation des variables
    date_now = date.today().strftime("%d-%m-%Y")
    # Recherche des jeux en commun
    merge_info = merge_info_games(filename_site, name_site, console)
    # Vérification du retour de la fonction
    if len(merge_info[console]) > 0:
        # Création du dictionnaire avec tous les jeux
        dict_update = update_file(merge_info, filename_site, name_site, console)
        # Vérification du retour de la fonction
        if len(dict_update[console]) > 0:
            print(f"Création du nouveau fichier :  {console}_{date_now}.json")
            with open('Data/Json/'+name_site+'/'+console+'_'+date_now+'.json', "w", encoding= 'utf-8') as file_json:
                json.dump(dict_update, file_json, ensure_ascii = False, indent = 4)
            # Supprime l'ancien fichier
            print("L'ancien fichier a été supprimer...")
            os.remove(f"Data/Json/{name_site}/{filename_site}")
        else:
            # message pas de nouvelle modif
            print("Il n'y a pas de nouvelle modification")
    else:
        # message pas de jeu identique trouvé
        print("Aucun jeu commun avec le fichier de reference...")


def validated_data(filename_site, name_site, console):
    '''
        Permet la validation ou la modification des données scraper pour un console visée.
        filename_site => nom du fichier json de la console
        name_site => nom du site visé
        console => nom de la console
        créer un nouveau fichier json avec le même nom du fichier passé en parametre
    '''
    print(f"Début de la vérification et validation des données pour la console :  {console}")
    # Initialisation des dictionnaires
    dict_tmp   = {}
    dict_games = {}
    # Lecture du fichier
    data_site = f_serve.readJson(f"Data/Json/{name_site}/{filename_site}")
    # Boucle sur le dictionnaire
    for key, game in data_site[console].items():
        # Initialisation des variables
        title = ""
        genre = ""
        editeur = ""
        price = ""
        date_sortie = ""

        # Titre
        print(f"L'url :  {game['url_game']}")
        print(f"Nom du jeu :  {game['title']}")
        input_title = input("Voulez-vous modifier le titre ? [yes - no]  ")
        if input_title == "yes":
            new_title = ""
            while new_title == "":
                print("Le titre ne peut pas etre vide...")
                new_title = input("Entrez le nouveau titre  ")
            title = new_title
        else:
            title = game["title"]
        # Genre
        print(f"Genre du jeu : {game['genre']}")
        input_genre = input("Voulez-vous modifier le genre ? [yes - no]  ")
        if input_genre == "yes":
            new_genre = input("Entrez le nouveau genre  ")
            genre = new_genre
        else:
            genre = game["genre"]
        # Editeur
        print(f"Editeur du jeu : {game['editeur']}")
        input_editeur = input("Voulez-vous modifier le nom de l'editeur ? [yes - no]  ")
        if input_editeur == "yes":
            new_editeur = input("Entrez le nouveau nom  ")
            editeur = new_editeur
        else:
            editeur = game["editeur"]
        # Price
        print(f"Prix du jeu : {game['price']}")
        input_price = input("Voulez-vous modifier le prix ? [yes - no]  ")
        if input_price == "yes":
            new_price = input("Entrez le nouveau prix  ")
            price = new_price
        else:
            price = game["price"]
        # Date_sortie
        print(f"Date de sortie du jeu : {game['date_sortie']}")
        input_date = input("Voulez-vous modifier la date sortie ? [yes - no]  ")
        if input_date == "yes":
            new_date = input("Entrez la nouvelle date  ")
            date_sortie = new_date
        else:
            date_sortie = game["date_sortie"]
        # etat
        print(f"Etat du jeu : {game['etat']}")
        input_etat = input("Voulez-vous modifier l'etat du jeu ? [yes - no]  ")
        if input_etat == "yes":
            new_etat = input("Entrez le nouveau etat  ")
            etat = new_etat
        else:
            etat = game["etat"]
        # Ajout dans le dict temporaire
        dict_tmp[key] = {
            "title" : title,
            "price" : price,
            "editeur" : editeur,
            "genre" : genre,
            "date_sortie" : date_sortie,
            "etat" : etat,
            "url_img" : "",
            "url_game" : game["url_game"]
        }
    # Ajout des données dans le dictionnaire final
    dict_games[console] = dict_tmp
    # On supprime le fichier
    print("L'ancien fichier a été supprimer...")
    os.remove('Data/Json/'+name_site+'/'+filename_site)
    # On crée le nouveau fichier avec les données modifiées
    with open('Data/Json/'+name_site+'/'+filename_site, "w", encoding= 'utf-8') as file_json:
        json.dump(dict_games, file_json, ensure_ascii = False, indent = 4)
    print("Le fichier : "+filename_site+" a été crée...")


def insert_games(console,site):
    pass

def import_script(name_script):
    pass

def export_excel_simple(console, site):
    pass

def export_excel_all(console, site):
    pass