from PyQt6.QtCore import (Qt,QThread,pyqtSignal)
from PyQt6.QtGui import (QBrush,QPen,QFont)
from PyQt6.QtWidgets import (QMainWindow,QWidget,QVBoxLayout,QHBoxLayout,QPushButton,QLabel,QGraphicsScene,QGraphicsView)
from simulation import Simulation
from database import Database
from network import Server, send_message


class NetworkThread(QThread):
    result = pyqtSignal(object)
    def __init__(self, message):
        super().__init__()
        self.message = message

    def run(self):
        response = send_message(self.message)
        self.result.emit(response)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SAE 3.02 - Carrefour connecté")
        self.resize(900, 700)
        self.database = Database()
        self.simulation = Simulation()
        self.simulation.updated.connect(self.refresh)
        self.server = Server()
        self.server.start()
        self.network_thread = None
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        title = QLabel("SIMULATION DE CARREFOUR CONNECTÉ")
        title.setFont(QFont("Arial",16,QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        self.scene = QGraphicsScene(0,0,800,450)
        self.view = QGraphicsView(self.scene)
        layout.addWidget(self.view)
        buttons = QHBoxLayout()
        self.start_button = QPushButton("Démarrer")
        self.stop_button = QPushButton("Arrêter")
        self.add_button = QPushButton("Ajouter voiture")
        self.priority_button = QPushButton("Ajouter véhicule prioritaire")
        buttons.addWidget(self.start_button)
        buttons.addWidget(self.stop_button)
        buttons.addWidget(self.add_button)
        buttons.addWidget(self.priority_button)
        layout.addLayout(buttons)
        self.status_label = QLabel("État : arrêté | " "Véhicules : 0 | " "Réseau : OK")
        layout.addWidget(self.status_label)
        self.start_button.clicked.connect(self.simulation.start)
        self.stop_button.clicked.connect(self.simulation.stop)
        self.add_button.clicked.connect(self.add_vehicle)
        self.priority_button.clicked.connect(self.add_priority_vehicle)
        self.refresh()

    def refresh(self):
        self.scene.clear()
        self.scene.addRect(0,175,800,100,QPen(Qt.GlobalColor.darkGray),QBrush(Qt.GlobalColor.darkGray))
        self.scene.addRect(350,0,100,450,QPen(Qt.GlobalColor.darkGray),QBrush(Qt.GlobalColor.darkGray))
        self.draw_light(320,160,self.simulation.north.state)
        self.draw_light(460,275,self.simulation.south.state)
        self.draw_light(320,275,self.simulation.west.state)
        self.draw_light(460,160,self.simulation.east.state)
        for vehicle in (self.simulation.vehicles):
            if vehicle.priority:
                brush = QBrush(Qt.GlobalColor.red)
            else:
                brush = QBrush(Qt.GlobalColor.blue)
            self.scene.addRect(vehicle.x,vehicle.y,25,15,QPen(Qt.GlobalColor.black),brush)
        if self.simulation.running:
            state = "en cours"
        else:
            state = "arrêté"
        priority_text = ""
        if (self.simulation.priority_vehicle is not None):
            priority_text = (" | Priorité : ACTIVE")
        self.status_label.setText(f"État : {state}" f" | Véhicules : " f"{len(self.simulation.vehicles)}" f" | Réseau : OK" f"{priority_text}")

    def draw_light(self,x,y,state):
        if state == "GREEN":
            brush = QBrush(Qt.GlobalColor.green)
        elif state == "ORANGE":
            brush = QBrush(Qt.GlobalColor.yellow)
        else:
            brush = QBrush(Qt.GlobalColor.red)
        self.scene.addEllipse(x,y,20,20,QPen(Qt.GlobalColor.black),brush)

    def add_vehicle(self):
        vehicle = (self.simulation.add_vehicle())
        self.database.add_event("vehicle",f"Voiture {vehicle.id} ajoutée")
        message = {"type": "vehicle","id": vehicle.id,"priority": False}
        self.send_network_message(message)

    def add_priority_vehicle(self):
        vehicle = (self.simulation.add_priority_vehicle())
        if vehicle is None:
            self.status_label.setText("Priorité déjà active")
            return
        self.database.add_event("priority",f"Véhicule prioritaire " f"{vehicle.id} ajouté")
        message = {"type": "vehicle", "id": vehicle.id, "priority": True}
        self.send_network_message(message)

    def send_network_message(self,message):
        self.network_thread = (NetworkThread(message))
        self.network_thread.result.connect(self.network_result)
        self.network_thread.start()

    def network_result(self,response):
        if response is not None:
            self.database.add_event("network","Message TCP envoyé avec succès")
            self.refresh()
        else:
            self.database.add_event("network_error","Impossible de joindre le serveur")
            self.status_label.setText("Réseau : erreur")

    def closeEvent(self, event):
        self.simulation.stop()
        self.server.stop()
        self.database.close()
        event.accept()