# Importe QObject pour créer une classe compatible avec le système de signaux de PyQt6.
# Importe QTimer pour exécuter des actions automatiquement à intervalles réguliers.
# Importe pyqtSignal pour envoyer des signaux à d'autres parties du programme.
from PyQt6.QtCore import QObject, QTimer, pyqtSignal

# Importe la classe TrafficLight qui représente un feu de circulation.
from traffic_light import TrafficLight

# Importe la classe Vehicle qui représente un véhicule dans la simulation.
from vehicle import Vehicle


# Déclare la classe Simulation qui gère le fonctionnement du carrefour.
class Simulation:

    # Crée un signal qui permet d'indiquer que l'affichage doit être actualisé.
    updated = pyqtSignal()

    # Constructeur de la classe, exécuté lors de la création de la simulation.
    def __init__(self):

        # Initialise la classe QObject pour utiliser les fonctionnalités de PyQt6.
        super().__init__()

        # Indique que la simulation est arrêtée au démarrage.
        self.running = False

        # Initialise la variable qui stockera le véhicule prioritaire.
        self.priority_vehicle = None

        # Crée une liste vide qui contiendra tous les véhicules du carrefour.
        self.vehicles = []

        # Initialise le numéro du prochain véhicule à créer.
        self.next_id = 1

        # Crée les quatre feux de circulation du carrefour.
        self.north = TrafficLight()
        self.south = TrafficLight()
        self.east = TrafficLight()
        self.west = TrafficLight()

        # Définit les feux nord et sud au vert au démarrage.
        self.north.state = "GREEN"
        self.south.state = "GREEN"

        # Définit les feux est et ouest au rouge au démarrage.
        self.east.state = "RED"
        self.west.state = "RED"

        # Crée un timer pour gérer le changement automatique des feux.
        self.light_timer = QTimer()

        # Relie le déclenchement du timer à la méthode change_lights.
        self.light_timer.timeout.connect(self.change_lights)

        # Démarre le timer avec un intervalle de 4000 millisecondes, soit 4 secondes.
        self.light_timer.start(4000)

        # Crée un deuxième timer pour gérer le déplacement des véhicules.
        self.vehicle_timer = QTimer()

        # Relie le déclenchement du timer à la méthode update_vehicles.
        self.vehicle_timer.timeout.connect(self.update_vehicles)

    # Méthode permettant de démarrer la simulation.
    def start(self):

        # Indique que la simulation est en cours.
        self.running = True

        # Démarre le déplacement des véhicules avec une actualisation toutes les 50 ms.
        self.vehicle_timer.start(50)

        # Envoie un signal pour actualiser l'affichage.
        self.updated.emit()

    # Méthode permettant d'arrêter la simulation.
    def stop(self):

        # Indique que la simulation est arrêtée.
        self.running = False

        # Arrête le timer responsable du déplacement des véhicules.
        self.vehicle_timer.stop()

        # Envoie un signal pour actualiser l'affichage.
        self.updated.emit()

    # Méthode permettant de changer automatiquement l'état des feux.
    def change_lights(self):

        # Vérifie si un véhicule prioritaire est actuellement enregistré.
        if self.priority_vehicle is not None:

            # Vérifie si ce véhicule est toujours présent dans le carrefour.
            if self.priority_vehicle in self.vehicles:

                # Adapte les feux à la direction du véhicule prioritaire.
                self.set_priority_lights(self.priority_vehicle)

                # Actualise l'affichage des feux.
                self.updated.emit()

                # Arrête cette méthode pour ne pas effectuer le cycle normal des feux.
                return

            # Si le véhicule prioritaire n'est plus présent dans la simulation.
            else:

                # Supprime la référence au véhicule prioritaire.
                self.priority_vehicle = None

        # Vérifie si le feu nord est actuellement vert.
        if self.north.state == "GREEN":

            # Passe les feux nord et sud à l'orange.
            self.north.state = "ORANGE"
            self.south.state = "ORANGE"

        # Vérifie si le feu nord est actuellement orange.
        elif self.north.state == "ORANGE":

            # Passe les feux nord et sud au rouge.
            self.north.state = "RED"
            self.south.state = "RED"

            # Passe les feux est et ouest au vert.
            self.east.state = "GREEN"
            self.west.state = "GREEN"

        # Vérifie si le feu est est actuellement vert.
        elif self.east.state == "GREEN":

            # Passe les feux est et ouest à l'orange.
            self.east.state = "ORANGE"
            self.west.state = "ORANGE"

        # Si aucune des conditions précédentes n'est remplie.
        else:

            # Passe les feux est et ouest au rouge.
            self.east.state = "RED"
            self.west.state = "RED"

            # Passe les feux nord et sud au vert.
            self.north.state = "GREEN"
            self.south.state = "GREEN"

        # Envoie un signal pour actualiser l'affichage des feux.
        self.updated.emit()

    # Méthode permettant d'ajouter un véhicule classique.
    def add_vehicle(self):

        # Crée un véhicule avec la priorité désactivée.
        vehicle = self.create_vehicle(priority=False)

        # Vérifie que la position de départ du véhicule n'est pas déjà occupée.
        if not self.start_position_occupied(vehicle):

            # Ajoute le véhicule à la liste des véhicules présents.
            self.vehicles.append(vehicle)

            # Envoie un signal pour actualiser l'affichage.
            self.updated.emit()

        # Retourne le véhicule créé.
        return vehicle

    # Méthode permettant d'ajouter un véhicule prioritaire.
    def add_priority_vehicle(self):

        # Crée un véhicule avec la priorité activée.
        vehicle = self.create_vehicle(priority=True)

        # Vérifie que sa position de départ est libre.
        if not self.start_position_occupied(vehicle):

            # Ajoute le véhicule prioritaire à la liste des véhicules.
            self.vehicles.append(vehicle)

            # Enregistre ce véhicule comme véhicule prioritaire.
            self.priority_vehicle = vehicle

            # Modifie les feux pour laisser passer le véhicule prioritaire.
            self.set_priority_lights(vehicle)

            # Actualise l'affichage.
            self.updated.emit()

        # Retourne le véhicule créé.
        return vehicle

    # Méthode permettant de créer un véhicule et de définir ses caractéristiques.
    def create_vehicle(self, priority=False):

        # Récupère le numéro d'identification du prochain véhicule.
        vehicle_id = self.next_id

        # Incrémente l'identifiant pour le prochain véhicule.
        self.next_id += 1

        # Calcule un numéro entre 0 et 3 pour choisir une direction de départ.
        direction_number = ((vehicle_id - 1) % 4)

        # Si le résultat est 0, le véhicule arrive par la gauche.
        if direction_number == 0:

            # Définit la direction vers la droite.
            direction = "right"

            # Définit la position horizontale de départ.
            x = -30

            # Définit la position verticale de départ.
            y = 230

        # Si le résultat est 1, le véhicule arrive par la droite.
        elif direction_number == 1:

            # Définit la direction vers la gauche.
            direction = "left"

            # Définit la position horizontale de départ.
            x = 805

            # Définit la position verticale de départ.
            y = 205

        # Si le résultat est 2, le véhicule arrive par le haut.
        elif direction_number == 2:

            # Définit la direction vers le bas.
            direction = "down"

            # Définit la position horizontale de départ.
            x = 375

            # Définit la position verticale de départ.
            y = -30

        # Si aucune des conditions précédentes n'est remplie, le véhicule arrive par le bas.
        else:

            # Définit la direction vers le haut.
            direction = "up"

            # Définit la position horizontale de départ.
            x = 410

            # Définit la position verticale de départ.
            y = 465

        # Calcule un nombre entre 0 et 2 pour choisir le mouvement du véhicule.
        turn_number = vehicle_id % 3

        # Si le résultat est 0, le véhicule continue tout droit.
        if turn_number == 0:

            # Définit le mouvement comme étant tout droit.
            turn = "straight"

        # Si le résultat est 1, le véhicule tourne à gauche.
        elif turn_number == 1:

            # Définit le mouvement comme étant un virage à gauche.
            turn = "left"

        # Si aucune des conditions précédentes n'est remplie.
        else:

            # Définit le mouvement comme étant un virage à droite.
            turn = "right"

        # Crée et retourne un objet Vehicle avec toutes ses caractéristiques.
        return Vehicle(vehicle_id,x,y,direction,priority,turn)

    # Méthode qui actualise régulièrement la position des véhicules.
    def update_vehicles(self):

        # Parcourt une copie de la liste pour éviter les problèmes si elle est modifiée.
        for vehicle in list(self.vehicles):

            # Vérifie si le véhicule a franchi la ligne du feu.
            self.check_light_crossing(vehicle)

            # Vérifie si le véhicule n'a pas encore franchi le feu.
            if not vehicle.has_passed_light:

                # Vérifie si le véhicule est prioritaire.
                if vehicle.priority:

                    # Autorise le déplacement du véhicule prioritaire.
                    can_move = True

                # Si le véhicule n'est pas prioritaire.
                else:

                    # Vérifie si le feu autorise le passage du véhicule.
                    if self.light_allows_vehicle(vehicle):

                        # Autorise le déplacement si le feu est vert.
                        can_move = True

                    # Si le feu n'autorise pas le passage.
                    else:

                        # Vérifie si le véhicule peut avancer jusqu'à la ligne d'arrêt.
                        can_move = self.can_move_to_light(vehicle)

            # Si le véhicule a déjà franchi le feu.
            else:

                # Autorise son déplacement.
                can_move = True

            # Vérifie si le déplacement est actuellement autorisé.
            if can_move:

                # Vérifie si le prochain déplacement provoquerait une collision.
                if self.would_collide(vehicle):

                    # Bloque le déplacement en cas de collision potentielle.
                    can_move = False

            # Si le véhicule peut toujours avancer après les vérifications.
            if can_move:

                # Déplace le véhicule selon sa direction et sa vitesse.
                vehicle.move()

            # Vérifie à nouveau si le véhicule a franchi le feu après son déplacement.
            self.check_light_crossing(vehicle)

            # Applique le virage prévu lorsque le véhicule arrive au centre du carrefour.
            self.apply_turn(vehicle)

        # Supprime les véhicules qui ont quitté la zone de simulation.
        self.remove_finished_vehicles()

        # Vérifie si un véhicule prioritaire est encore enregistré.
        if self.priority_vehicle is not None:

            # Vérifie si ce véhicule est toujours présent dans la liste.
            if self.priority_vehicle not in self.vehicles:

                # Supprime la référence si le véhicule a quitté la simulation.
                self.priority_vehicle = None

        # Envoie un signal pour actualiser l'affichage des véhicules et des feux.
        self.updated.emit()

    # Méthode permettant de vérifier si le feu autorise le passage d'un véhicule.
    def light_allows_vehicle(self, vehicle):

        # Si le véhicule se déplace vers la droite, il dépend du feu ouest.
        if vehicle.direction == "right":
            return self.west.state == "GREEN"

        # Si le véhicule se déplace vers la gauche, il dépend du feu est.
        elif vehicle.direction == "left":
            return self.east.state == "GREEN"

        # Si le véhicule se déplace vers le bas, il dépend du feu nord.
        elif vehicle.direction == "down":
            return self.north.state == "GREEN"

        # Si le véhicule se déplace vers le haut, il dépend du feu sud.
        elif vehicle.direction == "up":
            return self.south.state == "GREEN"

        # Retourne False si la direction ne correspond à aucun cas prévu.
        return False

    # Méthode permettant de vérifier si un véhicule peut avancer jusqu'au feu rouge.
    def can_move_to_light(self, vehicle):

        # Récupère la position de la ligne d'arrêt correspondant au véhicule.
        stop_position = self.get_stop_position(vehicle)

        # Vérifie si aucune position d'arrêt n'a été trouvée.
        if stop_position is None:

            # Interdit le déplacement si la position est inconnue.
            return False

        # Définit une marge de sécurité de 5 pixels avant la ligne d'arrêt.
        margin = 5

        # Si le véhicule va vers la droite, vérifie qu'il ne dépasse pas la ligne d'arrêt.
        if vehicle.direction == "right":
            return (vehicle.x + vehicle.speed < stop_position - margin)

        # Si le véhicule va vers la gauche, vérifie qu'il ne dépasse pas la ligne d'arrêt.
        elif vehicle.direction == "left":
            return (vehicle.x - vehicle.speed > stop_position + margin)

        # Si le véhicule va vers le bas, vérifie qu'il ne dépasse pas la ligne d'arrêt.
        elif vehicle.direction == "down":
            return (vehicle.y + vehicle.speed < stop_position - margin)

        # Si le véhicule va vers le haut, vérifie qu'il ne dépasse pas la ligne d'arrêt.
        elif vehicle.direction == "up":
            return (vehicle.y - vehicle.speed > stop_position + margin)

        # Retourne False si la direction n'est pas reconnue.
        return False

    # Méthode qui retourne la position de la ligne d'arrêt selon la direction du véhicule.
    def get_stop_position(self, vehicle):

        # Pour un véhicule allant vers la droite, la ligne d'arrêt est à 295.
        if vehicle.direction == "right":
            return 295

        # Pour un véhicule allant vers la gauche, la ligne d'arrêt est à 460.
        elif vehicle.direction == "left":
            return 460

        # Pour un véhicule allant vers le bas, la ligne d'arrêt est à 145.
        elif vehicle.direction == "down":
            return 145

        # Pour un véhicule allant vers le haut, la ligne d'arrêt est à 275.
        elif vehicle.direction == "up":
            return 275

        # Retourne None si la direction n'est pas reconnue.
        return None

    # Méthode permettant de détecter si un véhicule a franchi son feu.
    def check_light_crossing(self, vehicle):

        # Vérifie si le véhicule a déjà franchi le feu.
        if vehicle.has_passed_light:

            # Arrête la méthode car le contrôle a déjà été effectué.
            return

        # Vérifie si le véhicule se déplace vers la droite.
        if vehicle.direction == "right":

            # Vérifie si sa position horizontale atteint ou dépasse 320.
            if vehicle.x >= 320:

                # Indique que le véhicule a franchi le feu.
                vehicle.has_passed_light = True

        # Vérifie si le véhicule se déplace vers la gauche.
        elif vehicle.direction == "left":

            # Vérifie si sa position horizontale atteint ou passe sous 435.
            if vehicle.x <= 435:

                # Indique que le véhicule a franchi le feu.
                vehicle.has_passed_light = True

        # Vérifie si le véhicule se déplace vers le bas.
        elif vehicle.direction == "down":

            # Vérifie si sa position verticale atteint ou dépasse 160.
            if vehicle.y >= 160:

                # Indique que le véhicule a franchi le feu.
                vehicle.has_passed_light = True

        # Vérifie si le véhicule se déplace vers le haut.
        elif vehicle.direction == "up":

            # Vérifie si sa position verticale atteint ou passe sous 255.
            if vehicle.y <= 255:

                # Indique que le véhicule a franchi le feu.
                vehicle.has_passed_light = True

    # Méthode qui vérifie si le prochain déplacement d'un véhicule provoquerait une collision.
    def would_collide(self, vehicle):

        # Initialise la future position horizontale avec la position actuelle.
        next_x = vehicle.x

        # Initialise la future position verticale avec la position actuelle.
        next_y = vehicle.y

        # Si le véhicule se déplace vers la droite.
        if vehicle.direction == "right":

            # Ajoute sa vitesse à sa future position horizontale.
            next_x += vehicle.speed

        # Si le véhicule se déplace vers la gauche.
        elif vehicle.direction == "left":

            # Retire sa vitesse à sa future position horizontale.
            next_x -= vehicle.speed

        # Si le véhicule se déplace vers le bas.
        elif vehicle.direction == "down":

            # Ajoute sa vitesse à sa future position verticale.
            next_y += vehicle.speed

        # Si le véhicule se déplace vers le haut.
        elif vehicle.direction == "up":

            # Retire sa vitesse à sa future position verticale.
            next_y -= vehicle.speed

        # Définit la largeur d'un véhicule en pixels.
        width = 25

        # Définit la hauteur d'un véhicule en pixels.
        height = 15

        # Calcule la limite gauche du véhicule à sa future position.
        left = next_x

        # Calcule la limite droite du véhicule à sa future position.
        right = next_x + width

        # Calcule la limite supérieure du véhicule à sa future position.
        top = next_y

        # Calcule la limite inférieure du véhicule à sa future position.
        bottom = next_y + height

        # Parcourt tous les véhicules présents dans la simulation.
        for other in self.vehicles:

            # Ignore le véhicule lui-même pour ne pas le comparer avec lui-même.
            if other == vehicle:
                continue

            # Récupère la limite gauche de l'autre véhicule.
            other_left = other.x

            # Calcule la limite droite de l'autre véhicule.
            other_right = other.x + width

            # Récupère la limite supérieure de l'autre véhicule.
            other_top = other.y

            # Calcule la limite inférieure de l'autre véhicule.
            other_bottom = other.y + height

            # Vérifie si les rectangles des deux véhicules se chevaucheraient.
            collision = (left < other_right and right > other_left and top < other_bottom and bottom > other_top)

            # Si un chevauchement est détecté.
            if collision:

                # Retourne True pour signaler une collision potentielle.
                return True

        # Retourne False si aucune collision potentielle n'a été détectée.
        return False

    # Méthode permettant de faire tourner un véhicule au centre du carrefour.
    def apply_turn(self, vehicle):

        # Vérifie si le véhicule a déjà effectué son virage.
        if vehicle.has_turned:

            # Arrête la méthode pour éviter de lui faire effectuer un deuxième virage.
            return

        # Vérifie si le véhicule se déplace actuellement vers la droite.
        if vehicle.direction == "right":

            # Vérifie si le véhicule a atteint le centre du carrefour.
            if vehicle.x >= 390:

                # Si le véhicule doit tourner à gauche.
                if vehicle.turn == "left":

                    # Change sa direction vers le haut.
                    vehicle.direction = "up"

                    # Définit sa nouvelle position horizontale.
                    vehicle.x = 410

                    # Définit sa nouvelle position verticale.
                    vehicle.y = 230

                # Si le véhicule doit tourner à droite.
                elif vehicle.turn == "right":

                    # Change sa direction vers le bas.
                    vehicle.direction = "down"

                    # Définit sa nouvelle position horizontale.
                    vehicle.x = 375

                    # Définit sa nouvelle position verticale.
                    vehicle.y = 230

                # Indique que le véhicule a effectué son virage ou atteint son point de décision.
                vehicle.has_turned = True

        # Vérifie si le véhicule se déplace vers la gauche.
        elif vehicle.direction == "left":

            # Vérifie si le véhicule a atteint le centre du carrefour.
            if vehicle.x <= 390:

                # Si le véhicule doit tourner à gauche.
                if vehicle.turn == "left":

                    # Change sa direction vers le bas.
                    vehicle.direction = "down"

                    # Définit sa nouvelle position horizontale.
                    vehicle.x = 375

                    # Définit sa nouvelle position verticale.
                    vehicle.y = 205

                # Si le véhicule doit tourner à droite.
                elif vehicle.turn == "right":

                    # Change sa direction vers le haut.
                    vehicle.direction = "up"

                    # Définit sa nouvelle position horizontale.
                    vehicle.x = 410

                    # Définit sa nouvelle position verticale.
                    vehicle.y = 205

                # Indique que le véhicule a effectué son virage ou atteint son point de décision.
                vehicle.has_turned = True

        # Vérifie si le véhicule se déplace vers le bas.
        elif vehicle.direction == "down":

            # Vérifie si le véhicule a atteint le centre du carrefour.
            if vehicle.y >= 205:

                # Si le véhicule doit tourner à gauche.
                if vehicle.turn == "left":

                    # Change sa direction vers la gauche.
                    vehicle.direction = "left"

                    # Définit sa nouvelle position horizontale.
                    vehicle.x = 375

                    # Définit sa nouvelle position verticale.
                    vehicle.y = 205

                # Si le véhicule doit tourner à droite.
                elif vehicle.turn == "right":

                    # Change sa direction vers la droite.
                    vehicle.direction = "right"

                    # Définit sa nouvelle position horizontale.
                    vehicle.x = 375

                    # Définit sa nouvelle position verticale.
                    vehicle.y = 230

                # Indique que le véhicule a effectué son virage ou atteint son point de décision.
                vehicle.has_turned = True

        # Vérifie si le véhicule se déplace vers le haut.
        elif vehicle.direction == "up":

            # Vérifie si le véhicule a atteint le centre du carrefour.
            if vehicle.y <= 230:

                # Si le véhicule doit tourner à gauche.
                if vehicle.turn == "left":

                    # Change sa direction vers la gauche.
                    vehicle.direction = "left"

                    # Définit sa nouvelle position horizontale.
                    vehicle.x = 410

                    # Définit sa nouvelle position verticale.
                    vehicle.y = 205

                # Si le véhicule doit tourner à droite.
                elif vehicle.turn == "right":

                    # Change sa direction vers la droite.
                    vehicle.direction = "right"

                    # Définit sa nouvelle position horizontale.
                    vehicle.x = 410

                    # Définit sa nouvelle position verticale.
                    vehicle.y = 230

                # Indique que le véhicule a effectué son virage ou atteint son point de décision.
                vehicle.has_turned = True

    # Méthode qui adapte les feux pour donner la priorité à un véhicule.
    def set_priority_lights(self, vehicle):

        # Si le véhicule prioritaire se dirige vers la droite.
        if vehicle.direction == "right":

            # Passe le feu ouest au vert pour autoriser son passage.
            self.west.state = "GREEN"

            # Passe les trois autres feux au rouge.
            self.east.state = "RED"
            self.north.state = "RED"
            self.south.state = "RED"

        # Si le véhicule prioritaire se dirige vers la gauche.
        elif vehicle.direction == "left":

            # Passe le feu est au vert.
            self.east.state = "GREEN"

            # Passe les trois autres feux au rouge.
            self.west.state = "RED"
            self.north.state = "RED"
            self.south.state = "RED"

        # Si le véhicule prioritaire se dirige vers le bas.
        elif vehicle.direction == "down":

            # Passe le feu nord au vert.
            self.north.state = "GREEN"

            # Passe les trois autres feux au rouge.
            self.south.state = "RED"
            self.east.state = "RED"
            self.west.state = "RED"

        # Si le véhicule prioritaire se dirige vers le haut.
        elif vehicle.direction == "up":

            # Passe le feu sud au vert.
            self.south.state = "GREEN"

            # Passe les trois autres feux au rouge.
            self.north.state = "RED"
            self.east.state = "RED"
            self.west.state = "RED"

    # Méthode qui vérifie si la position de départ d'un nouveau véhicule est déjà occupée.
    def start_position_occupied(self, vehicle):

        # Parcourt tous les véhicules déjà présents dans la simulation.
        for other in self.vehicles:

            # Calcule la distance horizontale entre les deux véhicules.
            horizontal_distance = abs(vehicle.x - other.x)

            # Calcule la distance verticale entre les deux véhicules.
            vertical_distance = abs(vehicle.y - other.y)

            # Vérifie si les deux véhicules sont trop proches l'un de l'autre.
            if (horizontal_distance < 35 and vertical_distance < 25):

                # Retourne True si la position de départ est occupée.
                return True

        # Retourne False si aucun véhicule ne bloque la position de départ.
        return False

    # Méthode qui supprime les véhicules ayant quitté la zone de simulation.
    def remove_finished_vehicles(self):

        # Crée une nouvelle liste pour conserver uniquement les véhicules encore visibles.
        remaining = []

        # Parcourt tous les véhicules présents dans la simulation.
        for vehicle in self.vehicles:

            # Vérifie si le véhicule est sorti des limites de la zone graphique.
            if (vehicle.x < -60 or vehicle.x > 860 or vehicle.y < -60 or vehicle.y > 520):

                # Passe au véhicule suivant sans conserver celui qui est sorti.
                continue

            # Ajoute le véhicule à la liste des véhicules encore présents.
            remaining.append(vehicle)

        # Remplace l'ancienne liste par la nouvelle liste sans les véhicules sortis.
        self.vehicles = remaining
