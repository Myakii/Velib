import socket
import json
import time
import requests

class VelibData:
    #Utilisation d'une classe pour une question de clean code
    def __init__(self):
        self.last_request_time = 0
        self.data = None
    
    def fetch_data(self):
        #Comparaison en amont avec la date du dernier appel, s'il date de moins de 300s (5min), on retourne data sans appeler l'api
        current_time = time.time()
        if current_time - self.last_request_time < 300 and self.data:
            return self.data
        
        #Initialisation des variables pour faire tous les appels api
        all_data = []
        total_results = 1468
        limit = 100
        offset = 0

        #Boucle pour avoir toutes les données des vélib, la limite de stations d'un appel api, étant à 100 et le nombre de stations 1468
        while offset < total_results:
            api_url = f"https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/velib-disponibilite-en-temps-reel/records?limit={limit}&offset={offset}"
            try:
                response = requests.get(api_url)
                if response.status_code == 200:
                    data = response.json()
                    all_data.extend(data["results"])  #Compilation des données des différents appels dans 1 variable, on récupère ce qu'il y a dans l'objet résult de la réponse
                    offset += limit
                else:
                    print(f"Erreur lors de la récupération des données Velib: {response.status_code}")
                    return None
            except Exception as e:
                print(f"Erreur lors de la récupération des données Velib: {e}")
                return None
            
        #Mise à jour de l'heure du dernier appel et des données récupérées
        self.last_request_time = current_time
        self.data = all_data
        return self.data
        
try:
    #Initialisation du serveur socket et de velib_data
    velib_data = VelibData()
    socket_server = socket.socket()
    host = socket.gethostname()
    port = 3000
    socket_server.bind((host, port))
    socket_server.listen(5)
    print("Serveur en écoute sur le port 3000.")

    while True:
        #Récupération des données velib (si pas de message d'erreur)
        socket_client, addr = socket_server.accept()
        data = velib_data.fetch_data()
        if data:
            socket_client.sendall(json.dumps(data).encode())
        else:
            #Conversion de la chaîne avant l'envoi
            socket_client.sendall("Erreur lors de la récupération des données Velib.".encode())
        socket_client.close()
except KeyboardInterrupt:
    print("Interruption du serveur par l'utilisateur.")
except Exception as e:
    print(f"Erreur lors de l'exécution du serveur: {e}")
finally:
    socket_server.close()
