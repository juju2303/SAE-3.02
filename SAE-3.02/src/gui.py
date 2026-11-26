# Importe Qt pour utiliser les alignements et les couleurs.
# Importe QThread pour exécuter des tâches dans un thread séparé.
# Importe pyqtSignal pour transmettre des résultats entre les threads.
from PyQt6.QtCore import (Qt,QThread,pyqtSignal)

# Importe les outils graphiques pour les couleurs, les contours et les polices.
from PyQt6.QtGui import (QBrush,QPen,QFont)

# Importe les composants nécessaires à la création de la fenêtre et de son interface.
from PyQt6.QtWidgets import (QMainWindow,QWidget,QVBoxLayout,QHBoxLayout,QPushButton,QLabel,QGraphicsScene,QGraphicsView)

# Importe la classe Simulation qui gère le fonctionnement du carrefour.
from simulation import Simulation

# Importe la classe Database qui gère l'enregistrement des événements.
from database import Database

# Importe la fonction permettant d'envoyer des messages au serveur.
from network import send_message


# Déclare une classe pour gérer les communications réseau dans un thread séparé.
class NetworkThread(QThread):

    # Crée un signal qui permettra de transmettre la réponse du serveur.
    result = pyqtSignal(object)

    # Constructeur de la classe, appelé lors de la création du thread.
    def __init__(self, message):

        # Initialise la classe QThread.
        super().__init__()

        # Stocke le message qui devra être envoyé au serveur.
        self.message = message

    # Méthode exécutée automatiquement lorsque le thread démarre.
    def run(self):

        # Envoie le message au serveur et récupère sa réponse.
        response = send_message(self.message)

        # Transmet la réponse au reste de l'application grâce au signal.
        self.result.emit(response)


# Déclare la fenêtre principale de l'application.
class MainWindow(QMainWindow):

    # Constructeur de la fenêtre principale.
    def __init__(self):

        # Initialise la fenêtre QMainWindow.
        super().__init__()

        # Définit le titre affiché en haut de la fenêtre.
        self.setWindowTitle("SAE 3.02 - Carrefour connecté")

        # Définit la taille initiale de la fenêtre : 900 pixels de large et 700 de haut.
        self.resize(900, 700)

        # Crée une connexion à la base de données.
        self.database = Database()

        # Crée l'objet qui gère la simulation du carrefour.
        self.simulation = Simulation()

        # Connecte le signal updated de la simulation à la méthode refresh.
        # Ainsi, l'affichage est actualisé lorsque la simulation change.
        self.simulation.updated.connect(self.refresh)

        # Initialise la variable qui stockera le thread réseau.
        self.network_thread = None

        # Crée le widget central qui contiendra tous les éléments de la fenêtre.
        central = QWidget()

        # Définit ce widget comme contenu principal de la fenêtre.
        self.setCentralWidget(central)

        # Crée une disposition verticale pour organiser les éléments.
        layout = QVBoxLayout(central)

        # Crée le titre affiché dans la fenêtre.
        title = QLabel("SIMULATION DE CARREFOUR CONNECTÉ")

        # Définit la police du titre : Arial, taille 16, en gras.
        title.setFont(QFont("Arial",16,QFont.Weight.Bold))

        # Centre le titre horizontalement.
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Ajoute le titre à la disposition verticale.
        layout.addWidget(title)

        # Crée une scène graphique de 800 pixels de large et 450 de haut.
        self.scene = QGraphicsScene(0,0,800,450)

        # Crée une vue permettant d'afficher la scène graphique.
        self.view = QGraphicsView(self.scene)

        # Ajoute la vue graphique à la fenêtre.
        layout.addWidget(self.view)

        # Crée une disposition horizontale pour aligner les boutons.
        buttons = QHBoxLayout()

        # Crée le bouton permettant de démarrer la simulation.
        self.start_button = QPushButton("Démarrer")

        # Crée le bouton permettant d'arrêter la simulation.
        self.stop_button = QPushButton("Arrêter")

        # Crée le bouton permettant d'ajouter une voiture.
        self.add_button = QPushButton("Ajouter voiture")

        # Crée le bouton permettant d'ajouter un véhicule prioritaire.
        self.priority_button = QPushButton("Ajouter véhicule prioritaire")

        # Ajoute le bouton démarrer à la disposition horizontale.
        buttons.addWidget(self.start_button)

        # Ajoute le bouton arrêter à la disposition horizontale.
        buttons.addWidget(self.stop_button)

        # Ajoute le bouton ajouter voiture à la disposition horizontale.
        buttons.addWidget(self.add_button)

        # Ajoute le bouton véhicule prioritaire à la disposition horizontale.
        buttons.addWidget(self.priority_button)

        # Ajoute la disposition des boutons à la disposition principale.
        layout.addLayout(buttons)

        # Crée une étiquette affichant l'état de la simulation et du réseau.
        self.status_label = QLabel("État : arrêté | " "Véhicules : 0 | " "Réseau : OK")

        # Ajoute cette étiquette à la fenêtre.
        layout.addWidget(self.status_label)

        # Relie le clic sur le bouton démarrer à la méthode start de la simulation.
        self.start_button.clicked.connect(self.simulation.start)

        # Relie le clic sur le bouton arrêter à la méthode stop de la simulation.
        self.stop_button.clicked.connect(self.simulation.stop)

        # Relie le clic sur le bouton ajouter voiture à la méthode add_vehicle.
        self.add_button.clicked.connect(self.add_vehicle)

        # Relie le clic sur le bouton véhicule prioritaire à la méthode correspondante.
        self.priority_button.clicked.connect(self.add_priority_vehicle)

        # Effectue un premier rafraîchissement de l'affichage.
        self.refresh()

    # Méthode permettant de mettre à jour l'affichage du carrefour.
    def refresh(self):

        # Efface tous les éléments graphiques précédemment affichés.
        self.scene.clear()

        # Dessine la route horizontale du carrefour en gris foncé.
        self.scene.addRect(0,175,800,100,QPen(Qt.GlobalColor.darkGray),QBrush(Qt.GlobalColor.darkGray))

        # Dessine la route verticale du carrefour en gris foncé.
        self.scene.addRect(350,0,100,450,QPen(Qt.GlobalColor.darkGray),QBrush(Qt.GlobalColor.darkGray))

        # Dessine le feu situé au nord selon son état actuel.
        self.draw_light(320,160,self.simulation.north.state)

        # Dessine le feu situé au sud selon son état actuel.
        self.draw_light(460,275,self.simulation.south.state)

        # Dessine le feu situé à l'ouest selon son état actuel.
        self.draw_light(320,275,self.simulation.west.state)

        # Dessine le feu situé à l'est selon son état actuel.
        self.draw_light(460,160,self.simulation.east.state)

        # Parcourt tous les véhicules présents dans la simulation.
        for vehicle in (self.simulation.vehicles):

            # Vérifie si le véhicule est prioritaire.
            if vehicle.priority:

                # Attribue la couleur rouge aux véhicules prioritaires.
                brush = QBrush(Qt.GlobalColor.red)

            # Si le véhicule n'est pas prioritaire.
            else:

                # Attribue la couleur bleue aux véhicules classiques.
                brush = QBrush(Qt.GlobalColor.blue)

            # Dessine le véhicule sous forme de rectangle avec ses coordonnées.
            self.scene.addRect(vehicle.x,vehicle.y,25,15,QPen(Qt.GlobalColor.black),brush)

        # Vérifie si la simulation est actuellement en fonctionnement.
        if self.simulation.running:

            # Définit le texte indiquant que la simulation est en cours.
            state = "en cours"

        # Si la simulation n'est pas en fonctionnement.
        else:

            # Définit le texte indiquant que la simulation est arrêtée.
            state = "arrêté"

        # Initialise le texte concernant la priorité à vide.
        priority_text = ""

        # Vérifie si un véhicule prioritaire est actuellement présent.
        if (self.simulation.priority_vehicle is not None):

            # Ajoute une indication signalant qu'une priorité est active.
            priority_text = (" | Priorité : ACTIVE")

        # Met à jour le texte affiché avec l'état, le nombre de véhicules,
        # l'état du réseau et la présence éventuelle d'un véhicule prioritaire.
        self.status_label.setText(f"État : {state}" f" | Véhicules : " f"{len(self.simulation.vehicles)}" f" | Réseau : OK" f"{priority_text}")

    # Méthode permettant de dessiner un feu à une position donnée.
    def draw_light(self,x,y,state):

        # Vérifie si le feu doit être vert.
        if state == "GREEN":

            # Définit la couleur verte.
            brush = QBrush(Qt.GlobalColor.green)

        # Vérifie si le feu doit être orange.
        elif state == "ORANGE":

            # Définit la couleur jaune pour représenter le feu orange.
            brush = QBrush(Qt.GlobalColor.yellow)

        # Si le feu n'est ni vert ni orange.
        else:

            # Définit la couleur rouge.
            brush = QBrush(Qt.GlobalColor.red)

        # Dessine le feu sous forme de cercle de 20 pixels de diamètre.
        self.scene.addEllipse(x,y,20,20,QPen(Qt.GlobalColor.black),brush)

    # Méthode appelée lorsqu'on clique sur le bouton ajouter voiture.
    def add_vehicle(self):

        # Ajoute un véhicule classique dans la simulation.
        vehicle = (self.simulation.add_vehicle())

        # Enregistre dans la base de données l'ajout de ce véhicule.
        self.database.add_event("vehicle",f"Voiture {vehicle.id} ajoutée")

        # Prépare un message contenant le type, l'identifiant et la priorité du véhicule.
        message = {"type": "vehicle","id": vehicle.id,"priority": False}

        # Envoie le message préparé au serveur.
        self.send_network_message(message)

    # Méthode appelée lorsqu'on clique sur le bouton véhicule prioritaire.
    def add_priority_vehicle(self):

        # Tente d'ajouter un véhicule prioritaire dans la simulation.
        vehicle = (self.simulation.add_priority_vehicle())

        # Vérifie si aucun véhicule prioritaire n'a pu être ajouté.
        if vehicle is None:

            # Affiche un message indiquant qu'une priorité est déjà active.
            self.status_label.setText("Priorité déjà active")

            # Arrête l'exécution de la méthode.
            return

        # Enregistre l'ajout du véhicule prioritaire dans la base de données.
        self.database.add_event("priority",f"Véhicule prioritaire " f"{vehicle.id} ajouté")

        # Prépare le message à envoyer au serveur avec la priorité activée.
        message = {"type": "vehicle", "id": vehicle.id, "priority": True}

        # Envoie le message au serveur.
        self.send_network_message(message)

    # Méthode permettant d'envoyer un message au serveur sans bloquer l'interface.
    def send_network_message(self,message):

        # Crée un thread réseau avec le message à transmettre.
        self.network_thread = (NetworkThread(message))

        # Relie le signal result du thread à la méthode qui traite la réponse.
        self.network_thread.result.connect(self.network_result)

        # Démarre le thread, ce qui exécute sa méthode run.
        self.network_thread.start()

    # Méthode appelée lorsque le thread réseau reçoit une réponse du serveur.
    def network_result(self,response):

        # Vérifie si une réponse a bien été reçue.
        if response is not None:

            # Enregistre dans la base de données la réussite de l'envoi du message TCP.
            self.database.add_event("network","Message TCP envoyé avec succès")

            # Actualise l'affichage de la fenêtre.
            self.refresh()

        # Si aucune réponse n'a été reçue.
        else:

            # Enregistre une erreur de communication dans la base de données.
            self.database.add_event("network_error","Impossible de joindre le serveur")

            # Affiche une erreur réseau dans l'interface.
            self.status_label.setText("Réseau : erreur")

    # Méthode automatiquement appelée lorsque l'utilisateur ferme la fenêtre.
    def closeEvent(self, event):

        # Arrête la simulation avant de fermer l'application.
        self.simulation.stop()

        # Ferme le serveur réseau.
        self.server.stop()

        # Ferme la connexion à la base de données.
        self.database.close()

        # Accepte la fermeture de la fenêtre.
        event.accept()
