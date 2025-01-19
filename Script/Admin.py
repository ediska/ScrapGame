'''
    Script réserve pour l'administrateur afin de pouvoir :
        - Completer les informations des jeux scraper avec le site de référence (Jeuxvideo)
        - Vérifier les informations scraper et les modifier
        - Insérer les données dans la Base
        - Importer un script de scraping
        - Créer un fichier export excel (de la console visée pour un site visée ou all console pour un site(faire par classeur))
'''
from datetime import date
import Service.FileService as f_serve
import json
import shutil, os


def merge_info_games(filename_site, name_site, console):
    '''
        Permet de completer les informations des jeux commun entre le fichier reference et celui du site
        filename_site => nom du fichier du site
        console => nom de la console
        return  merge_game => dictionnaire contenant que les jeux concernés
    '''
    # Initialisation des variables
    # Compteur
    cpt_site = 1
    cpt_ref = 1
    # Dictionnaire
    merge_tmp = {}
    merge_game = {}

    # Lecture des fichiers Data/Json/Jeuxvideo/Nes_03-01-2025.json
    ref = f_serve.readJson(f"Data/Json/Jeuxvideo/{console}.json")
    site = f_serve.readJson(f"Data/Json/{name_site}/{filename_site}")

    # Boucle
    while cpt_site <= len(site[console]) and cpt_ref <= len(ref[console]):
        # Vérification de l'égalité des titres
        if ref[console][str(cpt_ref)]['title'].lower() == site[console][str(cpt_site)]['title'].lower():
            print("J'ai trouvé un jeu...")
            # title
            title = ref[console][str(cpt_ref)]['title'].lower()
            # editeur
            if ref[console][str(cpt_ref)]['editeur'] != site[console][str(cpt_site)]['editeur']:
                print("Editeur sont différent")
                if site[console][str(cpt_site)]['editeur'] == "":
                    editeur = ref[console][str(cpt_ref)]['editeur']
                else:
                    editeur = site[console][str(cpt_site)]['editeur']
            # genre
            if ref[console][str(cpt_ref)]['genre'] != site[console][str(cpt_site)]['genre']:
                print("Genre sont différent")
                if site[console][str(cpt_site)]['genre'] == "":
                    genre = ref[console][str(cpt_ref)]['genre']
                else:
                    genre = site[console][str(cpt_site)]['genre']
            # name_img
            if ref[console][str(cpt_ref)]['name_img'] != site[console][str(cpt_site)]['name_img']:
                print("Name_img sont différent")
                if site[console][str(cpt_site)]['name_img'] == "":
                    name_img = ref[console][str(cpt_ref)]['name_img']
                else:
                    name_img = site[console][str(cpt_site)]['name_img']
            # date_sortie
            if ref[console][str(cpt_ref)]['date_sortie'] != site[console][str(cpt_site)]['date_sortie']:
                print("Date_sortie sont différent")
                if site[console][str(cpt_site)]['date_sortie'] == "":
                    date_sortie = ref[console][str(cpt_ref)]['date_sortie']
                else:
                    date_sortie = site[console][str(cpt_site)]['date_sortie']
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
            print(merge_tmp)
            merge_game[cpt_site] = merge_tmp
            merge_tmp = {}
            cpt_site += 1
        else:
            # On passe au jeu suivant du site reference
            cpt_ref += 1
        # Cas si on arrive à la fin du fichier ref
        if cpt_ref >= len(ref[console]):
            cpt_site +=1    
            cpt_ref = 1

    return merge_game

def modif_file(dict_merge, filename_site, name_site, console):
    # initialisation de variable
    dict_tmp = {}
    dict_game = {}
    # lecture du fichier scraper du site
    site = f_serve.readJson(f"Data/Json/{name_site}/{filename_site}")
    
    # Boucle sur le fichier
    for key, game in site[console].items():
        for k, g in dict_merge.items():
            if key == str(k):
                print("J'ai la key")
                dict_tmp[key] = g 
            else:
                # sinon on le sauvegarde dans le dictionnaire
                dict_tmp[key] = game

    dict_game[console] = dict_tmp
    # retourne le dictionnaire  
    return dict_game

def completed_file(filename_site, site, console):
    # Initialisation des variables
    date_now = date.today().strftime("%d-%m-%Y")
    path_ref = "Data/Json/Jeuxvideo/"+console+".json"
    path_site = "Data/Json/"+site+"/"+filename_site
    # On fait merge_info_game(r,s,console)
    merge_info = merge_info_games(path_site, site, console)
    # on verifie le retour de la fonction
    if len(merge_info) > 0:
        modif_dict = modif_file(merge_info, path_site, site,console)
        print(modif_dict)
        # on verifie le retour de modif_retour
        if len(modif_dict[console]) > 0:
            # on creer le nouveau fichier
            with open('Data/Json/'+site+'/'+console+'_'+date_now+'.json', "w", encoding= 'utf-8') as file_json:
                json.dump(modif_dict, file_json, ensure_ascii = False, indent = 4)
                print("Le fichier : "+console+'_'+date_now+".json a été crée...")
            # on supprime l'ancien fichier
            print("L'ancien fichier a été supprimer...")
            os.remove('Data/Json/'+site+'/'+filename_site)
        else:
            # message pas de nouvelle modif
            print("Il n'y a pas de nouvelle modification")
    else:
        # message pas de jeu identique trouvé
        print("Aucun jeu commun avec le fichier de reference...")


def verification_data(console, site_a_vérifier):
    pass

def insert_games(console,site):
    pass

def import_script(name_script):
    pass

def export_excel(console, site):
    pass