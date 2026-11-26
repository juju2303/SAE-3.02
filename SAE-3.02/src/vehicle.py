# Déclare la classe Vehicle qui représente un véhicule dans la simulation.
class Vehicle:

    # Constructeur de la classe, appelé lors de la création d'un véhicule.
    # Il reçoit son identifiant, sa position, sa direction, sa priorité et son virage.
    # priority=False signifie que le véhicule n'est pas prioritaire par défaut.
    # turn="straight" signifie qu'il continue tout droit par défaut.
    def __init__(self, vehicle_id, x, y, direction, priority=False, turn="straight"):

        # Stocke l'identifiant unique du véhicule.
        self.id = vehicle_id

        # Définit la position horizontale du véhicule sur la simulation.
        self.x = x

        # Définit la position verticale du véhicule sur la simulation.
        self.y = y

        # Enregistre la direction dans laquelle le véhicule se déplace.
        # Les valeurs possibles sont "right", "left", "up" et "down".
        self.direction = direction

        # Indique si le véhicule est prioritaire, par exemple une ambulance.
        self.priority = priority

        # Indique la direction que le véhicule souhaite prendre au carrefour.
        # Les valeurs possibles sont "straight", "left" et "right".
        self.turn = turn

        # Définit la vitesse de déplacement du véhicule.
        self.speed = 3

        # Indique si le véhicule a déjà franchi son feu de circulation.
        # False signifie qu'il ne l'a pas encore franchi.
        self.has_passed_light = False

        # Indique si le véhicule a déjà effectué son virage.
        # False signifie qu'il n'a pas encore tourné.
        self.has_turned = False

    # Méthode qui permet de déplacer le véhicule en fonction de sa direction.
    def move(self):

        # Si le véhicule se dirige vers la droite.
        if self.direction == "right":

            # Augmente sa position horizontale selon sa vitesse.
            self.x += self.speed

        # Si le véhicule se dirige vers la gauche.
        elif self.direction == "left":

            # Diminue sa position horizontale selon sa vitesse.
            self.x -= self.speed

        # Si le véhicule se dirige vers le bas.
        elif self.direction == "down":

            # Augmente sa position verticale selon sa vitesse.
            self.y += self.speed

        # Si le véhicule se dirige vers le haut.
        elif self.direction == "up":

            # Diminue sa position verticale selon sa vitesse.
            self.y -= self.speed
