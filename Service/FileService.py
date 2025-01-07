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
        Allows the display of commands available in the application
    '''
    print()
    print("  Description of commands available on Scrap_Game  :")
    print("  --------------------------------------------------")
    print()
    print("    [HELP - help - -H]   =>   Shows all application commands.")
    print()
    print("    [LIST - list]        =>   Displays the list of sites targeted for scraping.")
    print()
    print("    [SCRAP - scrap]      =>   Launch the scrapping program, at the beginning you will have to choose the name of the targeted site and the name of the targeted console. ")
    print()
    print("    [ADMIN - admin]      =>   Allows you to launch the part reserved for the admin.")
    print()
    print("    [QUIT - quit]        =>   Allows you to exit the program.")
    print()
    print("    [EXIT - exit]        =>   Allows you to exit the program.")
    print()


def get_console(source, site):
    '''
        Allows you to recover all the consoles of the targeted site
    '''
    list_key = []
    # Key recovery
    for k in source[site].keys():
        list_key.append(k)

    return list_key


def get_site(source):
    '''
       Allows you to recover all sites that are targeted by scraping 
    '''
    list_site = []
    # Site recovery
    for k in source.keys():
        list_site.append(k)

    return list_site


def get_urls_by_console(source, site, choice):
    '''      
        Allows you to retrieve the site urls according to the choice of console
    '''
    
    dict_url = {}
    list_keys = []
    # Keys recovery
    for k in source[site].keys():
        list_keys.append(k)

    # Verification of the choice variable
    if choice == 'all':
        dict_url = source[site]
    elif choice in list_keys:
        dict_url[choice] = source[site][choice]
    else:
        print("choice not found")

    return dict_url


## Admin part