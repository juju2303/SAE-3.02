# Déclare la classe TrafficLight qui représente un feu de circulation.
class TrafficLight:

    # Constructeur de la classe, exécuté lors de la création d'un feu.
    def __init__(self):

        # Initialise le feu à l'état rouge par défaut.
        self.state = "RED"

    # Méthode permettant de changer l'état du feu de circulation.
    def change(self):

        # Vérifie si le feu est actuellement rouge.
        if self.state == "RED":

            # Passe le feu au vert.
            self.state = "GREEN"

        # Vérifie si le feu est actuellement vert.
        elif self.state == "GREEN":

            # Passe le feu à l'orange.
            self.state = "ORANGE"

        # Si le feu est dans un autre état, notamment orange.
        else:

            # Repasse le feu au rouge.
            self.state = "RED"
