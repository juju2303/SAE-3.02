# SAE 3.02 — Mini-simulation d’un carrefour connecté

## Présentation
Projet pédagogique du BUT Réseaux et Télécommunications, parcours ROM. L’application représente un carrefour, ses feux et des véhicules. Elle prévoit des commandes de simulation, des échanges TCP en JSON et l’enregistrement d’événements dans SQLite.

## Prérequis
Python 3 et pip.

## Installation
Depuis la racine du projet :
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt

Sous Windows, activez l’environnement avec `.venv\\Scripts\\activate`.

## Lancement
Depuis la racine :
python src/main.py

Si les imports de votre version supposent un lancement depuis `src`, ouvrez `src/main.py` dans PyCharm, sélectionnez l’environnement `.venv`, puis lancez le fichier.

## Utilisation
1. Ouvrir l’application.
2. Cliquer sur **Démarrer**.
3. Cliquer sur **Ajouter voiture** pour ajouter un véhicule.
4. Observer les déplacements et les feux.
5. Cliquer sur **Arrêter**, puis fermer la fenêtre.

Les libellés et fonctions exacts doivent correspondre à la version finale.

## Réseau et base de données
La communication prévue utilise TCP sur `127.0.0.1:5000` et des messages JSON. Le port doit être libre. SQLite conserve des événements dans `database/traffic.db` si cette fonction est activée. Les modules `socket`, `json`, `sqlite3` et `threading` font partie de Python et ne s’installent pas avec pip.

## Dépendances
Voir `requirements.txt`.

## Auteurs
- Jules Landauer
- Maël Sasorith

## Limites
La simulation est pédagogique et simplifie les comportements routiers. Les fonctions de priorité, d’évitement des collisions, de réseau et de base de données doivent être vérifiées par les tests avant le rendu.
