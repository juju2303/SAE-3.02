# SAE 3.02 — Mini-simulation d’un carrefour connecté

## 1. Présentation du projet

Ce projet a été réalisé dans le cadre du BUT Réseaux et Télécommunications, parcours ROM.

Il consiste à développer une mini-simulation d'un carrefour connecté. L'application permet de visualiser des véhicules circulant sur un carrefour, des feux de signalisation et différentes interactions.

Le projet utilise notamment :
- **Python** pour le développement.
- **PyQt6** pour l'interface graphique.
- **TCP et JSON** pour les échanges réseau.
- **SQLite** pour l'enregistrement des événements.

## 2. Prérequis

Pour installer et lancer le projet sur une machine Debian, il faut :
- Une machine virtuelle avec Debian et un environnement graphique.
- Une connexion Internet.
- Un compte utilisateur Debian.
- Un accès à un terminal.

Aucune connaissance préalable en programmation n'est nécessaire. Les commandes ci-dessous permettent de réaliser l'installation.

## 3. Installation sur Debian

### Étape 1 — Ouvrir le terminal

Démarrez votre machine virtuelle Debian, connectez-vous à votre session et ouvrez le terminal.

### Étape 2 — Installer les outils nécessaires

Copiez-collez la commande suivante dans le terminal :

```bash
sudo apt update
sudo apt install -y git python3 python3-venv python3-pip
```

Cette commande installe :
- `git` : permet de récupérer le projet depuis GitHub.
- `python3` : permet d'exécuter le programme.
- `python3-venv` : permet de créer un environnement Python isolé.
- `python3-pip` : permet d'installer les bibliothèques nécessaires.

### Étape 3 — Télécharger le projet depuis GitHub

Placez-vous dans votre dossier personnel :

```bash
cd ~
```

Téléchargez ensuite le projet :

```bash
git clone https://github.com/juju2303/SAE-3.02.git
```

Entrez dans le dossier du projet :

```bash
cd SAE-3.02
```

Le code source et les documents du projet sont maintenant présents sur votre machine.

### Étape 4 — Créer l'environnement Python

Créez un environnement virtuel avec la commande :

```bash
python3 -m venv .venv
```

Activez-le :

```bash
source .venv/bin/activate
```

Lorsque l'environnement est activé, le nom `(.venv)` apparaît généralement au début de la ligne du terminal.

### Étape 5 — Installer les dépendances

Mettez à jour pip :

```bash
python -m pip install --upgrade pip
```

Installez ensuite les bibliothèques nécessaires au projet :

```bash
python -m pip install -r requirements.txt
```

Cette commande installe automatiquement les dépendances indiquées dans le fichier `requirements.txt`, notamment PyQt6.

## 4. Lancer l'application

Assurez-vous d'être toujours dans le dossier principal `SAE-3.02` et que l'environnement virtuel est activé.

Lancez le programme avec :

```bash
python src/main.py
```

L'interface graphique de la simulation doit alors s'ouvrir.

**Important :** le programme nécessite une session Debian avec un environnement graphique. Il ne peut pas afficher sa fenêtre dans un terminal uniquement en mode texte ou sur une VM sans interface graphique.

## 5. Utilisation de l'application

Une fois l'application ouverte :

1. Cliquer sur **Démarrer** pour lancer la simulation.
2. Cliquer sur **Ajouter voiture** pour ajouter un véhicule.
3. Observer les déplacements des véhicules et le fonctionnement des feux.
4. Cliquer sur **Arrêter** pour interrompre la simulation.
5. Fermer la fenêtre pour quitter l'application.

Les commandes et les fonctionnalités disponibles dépendent de la version finale de l'application.

## 6. Réseau et base de données

Le projet utilise une communication réseau TCP avec l'adresse locale `127.0.0.1` et le port `5000`.

Les messages échangés utilisent le format JSON.

La base de données SQLite permet d'enregistrer certains événements de la simulation dans le fichier :

```text
database/traffic.db
```

Les modules `socket`, `json`, `sqlite3` et `threading` utilisés pour ces fonctionnalités sont intégrés à Python. Ils ne nécessitent donc pas d'installation supplémentaire avec pip.

## 7. En cas de problème

### Erreur : git: command not found

Git n'est probablement pas installé. Exécutez :

```bash
sudo apt install git
```

### Erreur : No module named 'PyQt6'

Les dépendances n'ont probablement pas été installées ou l'environnement virtuel n'est pas activé.

Exécutez :

```bash
source .venv/bin/activate
python -m pip install -r requirements.txt
```

### Erreur liée au lancement de l'interface graphique ou au plugin Qt xcb

Si une erreur indique que Qt ne parvient pas à charger le plugin `xcb`, installez les bibliothèques système nécessaires :

```bash
sudo apt install -y libxcb-cursor0 libxkbcommon-x11-0
```

Puis essayez de relancer l'application.

### Le programme ne démarre pas

Vérifiez que vous êtes bien dans le dossier `SAE-3.02`, que l'environnement virtuel est activé et que vous utilisez la commande :

```bash
python src/main.py
```

## 8. Dépendances

Les dépendances Python du projet sont indiquées dans le fichier :

```text
requirements.txt
```

## 9. Auteurs

- Jules Landauer
- Maël Sasorith

## 10. Limites du projet

Cette application est une simulation pédagogique. Certains comportements de circulation sont simplifiés par rapport à un véritable carrefour.

Le projet a pour objectif de mettre en pratique plusieurs notions de programmation, d'interface graphique, de communication réseau et de gestion de données.
