import Service.FileService as f_serve
import Script.Jeuxvideo as jv


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
        case "quit":
            break
        case "exit":
            break
        case _:
            print("choise not found...")