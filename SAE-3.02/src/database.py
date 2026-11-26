import sqlite3 # Importe le module sqlite3 pour utiliser une base de données SQLite.
from datetime import datetime # Importe datetime pour récupérer la date et l'heure actuelles.
from pathlib import Path # Importe Path pour manipuler les chemins des dossiers et fichiers.
    

class Database: # Déclaration de la classe Database qui gère la base de données.

    def __init__(self): # Constructeur : il est exécuté automatiquement à la création d'un objet Database.

        database_folder = (Path(__file__).parent.parent / "database") # Définit le chemin du dossier database situé à la racine du projet.
        # Crée le dossier database s'il n'existe pas déjà.
        # parents=True permet de créer les dossiers parents si nécessaire.
        # exist_ok=True évite une erreur si le dossier existe déjà.
        database_folder.mkdir(parents=True, exist_ok=True)
        # Ouvre une connexion à la base de données traffic.db.
        # Si le fichier n'existe pas, SQLite le crée automatiquement.
        self.connection = sqlite3.connect(database_folder / "traffic.db")
        # Exécute une commande SQL pour créer la table events si elle n'existe pas.
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS events (

                # Identifiant unique de chaque événement, généré automatiquement.
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                # Date et heure auxquelles l'événement a été enregistré.
                date TEXT,

                # Type de l'événement (voiture, priorité, réseau, etc.).
                type TEXT,

                # Description de l'événement enregistré.
                message TEXT
            )
        """)
        self.connection.commit() # Valide et enregistre la création de la table dans la base de données.
    def add_event(self,event_type,message): # Méthode permettant d'ajouter un événement dans la base de données.
        # Exécute une commande SQL pour insérer un nouvel événement dans la table.
        self.connection.execute(
            """
            INSERT INTO events(
                # Colonne dans laquelle sera enregistrée la date.
                date,
                # Colonne dans laquelle sera enregistré le type.
                type,
                # Colonne dans laquelle sera enregistré le message.
                message
            )
            # Les trois points d'interrogation correspondent aux valeurs à insérer.
            VALUES (?, ?, ?)
            """,
            # Fournit les valeurs qui remplaceront les points d'interrogation.
            (
                # Récupère la date et l'heure actuelles au format année-mois-jour heure:minute:seconde.
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                # Valeur du type d'événement reçue en paramètre.
                event_type,
                # Message décrivant l'événement reçu en paramètre.
                message
            )
        )
        # Valide et enregistre l'ajout de l'événement dans la base de données.
        self.connection.commit()
    # Méthode permettant de fermer la connexion à la base de données.
    def close(self):
        # Ferme la connexion SQLite pour libérer les ressources utilisées.
        self.connection.close()
