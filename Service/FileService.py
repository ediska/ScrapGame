'''
   File bringing together all the functions for using a file 
   or displaying it in the console.
'''

import json
import os


def readJson(path_file):
    '''
        Allows reading a json file.
        path_file => path where the file to read is located.
        data      => returns all data contained in the file.
    '''
    file_listen = open(path_file, 'r')
    json_read = file_listen.read()
    data = json.loads(json_read)

    return data


def calculate_space(width, str):
    '''
        Allows you to calculate empty spaces on a line.
        width => display length.
        str   => phrase or word of the line.
    '''
    return ((width - len(str)) // 2)-1


def create_header():
    '''
        Allows the application header to be displayed in the console.
    '''
    width = 121
    height = 10
    stars = "*"
    empty = " "
    title = "Scrap_Game"
    ph1 = "To find out the commands, type: help or -H "
    ph2 = "To exit the program, type: exit or quit"

    space_title = calculate_space(width, title)
    space_ph1 = calculate_space(width, ph1)
    space_ph2 = calculate_space(width, ph2)
    line_empty   = stars+(width-2)*empty+stars

    for line in range(0, height):
        match line:
            case 0:
                print(stars*width)
            case 5:
                print(stars+(empty*space_title)+title+(empty*space_title)+empty+stars)
            case 7:
                print(stars+(empty*space_ph1)+ph1+(empty*space_ph1)+stars)
            case 8:
                print(stars+(empty*space_ph2)+ph2+(empty*space_ph2)+stars)
            case 9:
                print(stars*width)
            case _:
                print(line_empty)


def help():
    '''
        Permet l'affichage des commandes disponibles dans l'application
    '''
    print()
    print("  Description des commandes disponible sur Scrap_Game  :")
    print("  --------------------------------------------------")
    print()
    print("    [HELP - help - -H]   =>   Affiche toutes les commandes de l'application.")
    print()
    print("    [LIST - list]        =>   Affiche la liste des sites ciblés pour le scraping.")
    print()
    print("    [SCRAP - scrap]      =>   Lance le programme du scrapping, au début il faudra rentre le chemin pour le dossier de sauvegarde ")
    #print("                  sans le nom du site. Après vient le choix de la source à rentrer si c'est une URL ou un FICHIER")
    #print("                  - Si URL vous devrez rentrer l'url visée")
    #print("                  - Si FICHIER vous devrez rentrer le chemin où se trouve le fichier. Seul les fichiers .txt ou .json")
    #print("                   sont accéptés. Ensuite le script se lance est vous devrez voir défiler les informations, à la fin ")
    #print("                  du scraping on vous demandera si vous voulez une sauvegarde en fichier .xlsx et en suite vous ")
    #print("                  pouvez recommencer le scrape avec une URL ou FICHIER différent.")
    print()
    print("    [Admin - admin]      =>   Permet l'administration des données.")
    print()
    print("    [QUIT - quit]        =>   Permet de sortir du programme")
    print()
    print("    [EXIT - exit]        =>   Permet de sortir du programme")
    print()