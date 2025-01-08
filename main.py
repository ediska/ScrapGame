import Service.FileService as f_serve
import Script.Jeuxvideo as jv
import Script.Bdiherault as bdi


# Initialisation des variables
response = ""
source_url = f_serve.readJson("Data/urls.json")
# Afficher le header dans la console
f_serve.create_header()

# Boucle tant que response ne vaut pas exit ou quit
while response != "quit" or response != "exit":
    response = input("==>   ")
    # On met response en minuscule
    response = response.lower()
    # Vérification du contenu de response
    match response:
        case "list":
            print(f_serve.get_site(source_url))
        case "help":
            f_serve.help()
        case "-h":
            f_serve.help()
        case "scrap":
            # Récupération  des questions
            site = input("What is the target site ?   ")
            print("Choice of consoles: console name")
            print(f_serve.get_console(source_url, site))
            choice = input("What is your choice ?  ")
            urls = f_serve.get_urls_by_console(source_url, site, choice)
            # Switch sur les site appel du script
            match site:
                case "jeuxvideo":
                    jv.start_scrap(urls,site)
                case "bdiherault":
                    bdi.start_scrap(urls, site)
                case "exit":
                    break
                case "quit":
                    break
                case _:
                    print("Site inconnu")
        case "quit":
            break
        case "exit":
            break
        case _:
            print("choise not found...")