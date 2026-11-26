# Importe le module socket pour créer des connexions réseau entre les machines.
import socket

# Importe le module json pour convertir les messages en format JSON et inversement.
import json

# Importe le module threading pour exécuter plusieurs tâches en parallèle.
import threading


# Déclare la classe Server qui gère la réception des messages du client.
class Server:

    # Constructeur de la classe, exécuté lors de la création du serveur.
    def __init__(self):

        # Indique que le serveur est actif.
        self.running = True

        # Crée une socket TCP IPv4 pour permettre la communication réseau.
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

        # Autorise la réutilisation de l'adresse et du port après l'arrêt du serveur.
        self.socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

        # Associe le serveur à toutes les interfaces réseau disponibles sur le port 5000.
        self.socket.bind(("0.0.0.0", 5000))

        # Met le serveur en attente de connexions avec une file d'attente maximale de 5 connexions.
        self.socket.listen(5)

    # Méthode permettant de démarrer le serveur.
    def start(self):

        # Crée un thread qui exécutera la méthode listen en arrière-plan.
        # daemon=True permet au thread de s'arrêter avec le programme principal.
        thread = threading.Thread(target=self.listen,daemon=True)

        # Démarre le thread du serveur.
        thread.start()

    # Méthode qui attend les connexions des clients.
    def listen(self):

        # Continue d'attendre des connexions tant que le serveur est actif.
        while self.running:

            # Essaie d'accepter une nouvelle connexion.
            try:

                # Accepte la connexion et récupère la socket du client ainsi que son adresse.
                client, address = (self.socket.accept())

                # Crée un nouveau thread pour traiter la communication avec ce client.
                thread = threading.Thread(target=self.handle,args=(client,),daemon=True)

                # Démarre le traitement de la connexion dans ce nouveau thread.
                thread.start()

            # Intercepte les erreurs liées à la fermeture ou à l'utilisation de la socket.
            except OSError:

                # Quitte la boucle si la socket ne peut plus accepter de connexions.
                break

    # Méthode qui traite les messages reçus d'un client.
    def handle(self, client):

        # Essaie de recevoir et de traiter les données envoyées par le client.
        try:

            # Reçoit jusqu'à 1024 octets envoyés par le client.
            data = client.recv(1024)

            # Vérifie si aucune donnée n'a été reçue.
            if not data:

                # Quitte la méthode si le client n'a envoyé aucun message.
                return

            # Convertit les données reçues en texte puis transforme le JSON en objet Python.
            message = json.loads(data.decode())

            # Affiche le message reçu dans le terminal du serveur.
            print("Message reçu :",message)

            # Prépare une réponse indiquant que le message a été reçu correctement.
            response = {"status": "ok"}

            # Convertit la réponse en JSON puis l'envoie au client.
            client.send(json.dumps(response).encode())

        # Intercepte les erreurs liées au format JSON ou à la communication réseau.
        except (json.JSONDecodeError,OSError):

            # Prépare une réponse indiquant qu'une erreur s'est produite.
            response = {"status": "error"}

            # Essaie d'envoyer la réponse d'erreur au client.
            try:
                client.send(json.dumps(response).encode())

            # Intercepte une éventuelle erreur pendant l'envoi de la réponse.
            except OSError:

                # Ne fait rien si la réponse ne peut pas être envoyée.
                pass

        # Cette partie est exécutée même si une erreur se produit.
        finally:

            # Ferme la connexion avec le client pour libérer les ressources.
            client.close()

    # Méthode permettant d'arrêter le serveur.
    def stop(self):

        # Indique que le serveur doit arrêter de fonctionner.
        self.running = False

        # Essaie de fermer la socket du serveur.
        try:
            self.socket.close()

        # Intercepte une éventuelle erreur lors de la fermeture.
        except OSError:

            # Ne fait rien si la socket est déjà fermée.
            pass


# Fonction permettant au client d'envoyer un message au serveur.
def send_message(message):

    # Essaie d'établir une communication avec le serveur et de transmettre le message.
    try:

        # Crée une connexion TCP vers le serveur à l'adresse IP 192.168.8.10 sur le port 5000.
        # Le délai maximum d'attente pour établir la connexion est de 2 secondes.
        sock = socket.create_connection(("192.168.8.10", 5000),timeout=2)

        # Convertit le message Python en JSON, puis l'envoie au serveur sous forme d'octets.
        sock.send(json.dumps(message).encode())

        # Attend de recevoir jusqu'à 1024 octets correspondant à la réponse du serveur.
        response = sock.recv(1024)

        # Ferme la connexion avec le serveur.
        sock.close()

        # Convertit la réponse reçue en texte puis en objet Python.
        return json.loads(response.decode())

    # Intercepte les erreurs réseau ou les erreurs liées au format JSON.
    except (OSError,json.JSONDecodeError):

        # Retourne None pour indiquer qu'aucune réponse valide n'a été reçue.
        return None
