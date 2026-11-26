# Importe le module sys pour accéder aux arguments et gérer la fermeture du programme.
import sys

# Importe QApplication, qui permet de créer et de gérer une application PyQt6.
from PyQt6.QtWidgets import QApplication

# Importe la classe MainWindow depuis le fichier gui.py.
from gui import MainWindow


# Crée l'application PyQt6 en lui transmettant les arguments du programme.
app = QApplication(sys.argv)

# Crée une instance de la fenêtre principale de l'application.
window = MainWindow()

# Affiche la fenêtre principale à l'écran.
window.show()

# Lance la boucle principale de l'application et récupère son code de sortie
# lorsque l'utilisateur ferme la fenêtre.
sys.exit(app.exec())
