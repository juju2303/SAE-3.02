# SAE 3.02 — Déploiement d'un carrefour connecté sur deux machines virtuelles

## 1. Présentation du projet

Ce projet a été réalisé dans le cadre du BUT Réseaux et Télécommunications, parcours ROM.

L'objectif est de créer une simulation d'un carrefour connecté permettant de visualiser la circulation de véhicules, le fonctionnement des feux de signalisation et la gestion des véhicules prioritaires.

Le projet utilise :
- **Python** : développement de l'application.
- **PyQt6** : interface graphique du carrefour.
- **TCP** : communication entre les deux machines virtuelles.
- **JSON** : format des messages échangés.
- **SQLite** : enregistrement des événements de la simulation.
- **GitHub** : récupération du code source.

Le déploiement final utilise deux machines virtuelles Debian installées sur un même ordinateur grâce à VirtualBox.

### Fonctionnement général

Le projet est séparé en deux parties :

| Machine virtuelle | Rôle |
|---|---|
| VM 1 — Serveur | Reçoit les messages envoyés par le client et les affiche dans son terminal. |
| VM 2 — Client | Affiche le carrefour, lance la simulation, ajoute les véhicules et enregistre les événements dans la base de données. |

Les deux machines communiquent grâce au protocole TCP sur le port `5000`.

## 2. Prérequis

Avant de commencer, il faut disposer de :

- Un ordinateur fixe ou portable.
- Une connexion Internet.
- VirtualBox installé.
- Deux machines virtuelles Debian avec environnement graphique.
- Un compte utilisateur sur chaque Debian.

Aucune connaissance particulière en programmation ou en administration réseau n'est nécessaire. Il suffit de suivre les étapes dans l'ordre.

## 3. Création et configuration des machines virtuelles

### 3.1. Installer VirtualBox

Télécharger VirtualBox depuis le site officiel :

https://www.virtualbox.org/wiki/Downloads

Installer le logiciel en suivant les instructions proposées.

Il faut ensuite disposer de deux machines virtuelles Debian.

Si Debian n'est pas encore installé, télécharger l'image ISO depuis :

https://www.debian.org/download

Créer les deux machines virtuelles et installer Debian sur chacune d'elles.

Donner des noms faciles à reconnaître :

- `SAE-SERVEUR`
- `SAE-CLIENT`

**Important :** les deux machines doivent être démarrées séparément et posséder leur propre configuration réseau.

### 3.2. Configuration réseau de la VM Serveur

Dans VirtualBox :

1. Éteindre la VM `SAE-SERVEUR`.
2. Sélectionner la machine virtuelle.
3. Ouvrir **Configuration**.
4. Aller dans **Réseau**.

Configurer les deux cartes réseau :

**Carte 1 : NAT**

- Cocher « Activer la carte réseau ».
- Mode d'accès réseau : NAT.

Cette carte permet au serveur d'accéder à Internet.

**Carte 2 : Réseau interne**

- Cocher « Activer la carte réseau ».
- Mode d'accès réseau : Réseau interne.
- Nom : `SAE-INTERNE`.

Cette carte permet au serveur de communiquer avec la VM cliente.

Valider les modifications.

### 3.3. Configuration réseau de la VM Client

Dans VirtualBox :

1. Éteindre la VM `SAE-CLIENT`.
2. Sélectionner la machine virtuelle.
3. Ouvrir **Configuration**.
4. Aller dans **Réseau**.

Configurer uniquement la carte 1 :

- Cocher « Activer la carte réseau ».
- Mode d'accès réseau : Réseau interne.
- Nom : `SAE-INTERNE`.

**Attention :** le nom du réseau interne doit être exactement le même que celui de la deuxième carte réseau du serveur.

La VM cliente ne doit pas avoir de carte NAT supplémentaire. Elle utilisera la connexion Internet fournie par le serveur.

## 4. Configuration réseau de Debian

Les configurations suivantes doivent être réalisées dans les terminaux des machines virtuelles.

### 4.1. Identifier les cartes réseau

Démarrer les deux machines virtuelles et ouvrir un terminal sur chacune.

Exécuter :

```bash
ip -br link
```

Cette commande affiche les cartes réseau disponibles.

Sur le serveur, il faut identifier :
- La carte reliée au NAT.
- La carte reliée au réseau interne.

Sur le client, il faut identifier :
- La carte reliée au réseau interne.

Les noms peuvent varier selon l'installation Debian. Dans les exemples suivants, on utilisera :

| Machine | Carte | Rôle |
|---|---|---|
| Serveur | enp0s3 | NAT |
| Serveur | enp0s8 | Réseau interne |
| Client | enp0s3 | Réseau interne |

Si les noms affichés sur votre ordinateur sont différents, remplacez-les dans les commandes suivantes par les noms réellement obtenus.

### 4.2. Configuration de la VM Serveur

Sur la VM `SAE-SERVEUR`, ouvrir le fichier de configuration réseau :

```bash
sudo nano /etc/network/interfaces
```

Ajouter ou adapter les paramètres suivants :

```text
auto lo
iface lo inet loopback

allow-hotplug enp0s3
iface enp0s3 inet dhcp

auto enp0s8
iface enp0s8 inet static
    address 192.168.8.10
    netmask 255.255.255.0
```

Explication :

- `enp0s3` récupère automatiquement une adresse IP grâce au NAT de VirtualBox.
- `enp0s8` reçoit une adresse IP fixe pour communiquer avec le client.
- L'adresse IP interne du serveur est `192.168.8.10`.

Enregistrer avec `Ctrl + O`, puis Entrée.

Quitter avec `Ctrl + X`.

Redémarrer la machine virtuelle pour appliquer les modifications.

Vérifier les adresses :

```bash
ip -br addr
```

La carte interne doit avoir l'adresse :

```text
192.168.8.10
```

### 4.3. Configuration de la VM Client

Sur la VM `SAE-CLIENT`, ouvrir :

```bash
sudo nano /etc/network/interfaces
```

Ajouter ou adapter :

```text
auto lo
iface lo inet loopback

auto enp0s3
iface enp0s3 inet static
    address 192.168.8.11
    netmask 255.255.255.0
    gateway 192.168.8.10
    dns-nameservers 1.1.1.1 8.8.8.8
```

Explication :

- L'adresse IP du client est `192.168.8.11`.
- Le serveur `192.168.8.10` est utilisé comme passerelle.
- Les serveurs DNS permettent de résoudre les noms de domaine.

Enregistrer et quitter.

Redémarrer la VM.

Vérifier la configuration :

```bash
ip -br addr
```

La carte réseau interne doit posséder l'adresse `192.168.8.11`.

## 5. Permettre au client d'accéder à Internet grâce au serveur

Le serveur possède deux cartes réseau. Il doit donc transmettre les connexions entre le réseau interne et Internet.

### 5.1. Activer le transfert IPv4 sur le serveur

Sur la VM `SAE-SERVEUR`, exécuter :

```bash
sudo nano /etc/sysctl.conf
```

Repérer la ligne :

```text
#net.ipv4.ip_forward=1
```

Supprimer le `#` pour obtenir :

```text
net.ipv4.ip_forward=1
```

Enregistrer et quitter.

Appliquer la modification :

```bash
sudo sysctl -p
```

### 5.2. Configurer le partage de connexion

Installer les outils nécessaires :

```bash
sudo apt update
sudo apt install iptables iptables-persistent -y
```

Autoriser le transfert entre les deux cartes réseau :

```bash
sudo iptables -A FORWARD -i enp0s8 -o enp0s3 -j ACCEPT
```

Autoriser les réponses des connexions :

```bash
sudo iptables -A FORWARD -i enp0s3 -o enp0s8 -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT
```

Activer la traduction d'adresses réseau :

```bash
sudo iptables -t nat -A POSTROUTING -o enp0s3 -j MASQUERADE
```

Enregistrer les règles :

```bash
sudo netfilter-persistent save
```

**Remarque :** ces commandes utilisent les noms de cartes réseau indiqués précédemment. Il faut les adapter si votre Debian affiche d'autres noms.

### 5.3. Tester la connexion entre les deux VM

Sur la VM cliente, exécuter :

```bash
ping -c 4 192.168.8.10
```

Si tout fonctionne, la VM cliente reçoit des réponses du serveur.

Tester ensuite l'accès à Internet :

```bash
ping -c 4 8.8.8.8
```

Enfin, tester la résolution DNS :

```bash
ping -c 4 google.com
```

Si les trois tests fonctionnent, la configuration réseau est opérationnelle.

## 6. Installation du projet depuis GitHub

Le dépôt GitHub contient le code source nécessaire au fonctionnement du carrefour connecté.

Adresse du dépôt :

https://github.com/juju2303/SAE-3.02

Le projet doit être récupéré sur les deux machines virtuelles.

### 6.1. Sur la VM Serveur

Ouvrir un terminal.

Mettre Debian à jour :

```bash
sudo apt update
```

Installer Git et Python :

```bash
sudo apt install -y git python3 python3-venv python3-pip
```

Se placer dans le dossier personnel :

```bash
cd ~
```

Récupérer le dépôt :

```bash
git clone https://github.com/juju2303/SAE-3.02.git
```

Entrer dans le dossier du projet :

```bash
cd ~/SAE-3.02/SAE-3.02
```

Le serveur dispose maintenant du code source nécessaire.

### 6.2. Sur la VM Client

Ouvrir un terminal.

Mettre Debian à jour :

```bash
sudo apt update
```

Installer Git et Python :

```bash
sudo apt install -y git python3 python3-venv python3-pip
```

Récupérer le dépôt :

```bash
cd ~
git clone https://github.com/juju2303/SAE-3.02.git
```

Entrer dans le dossier du projet :

```bash
cd ~/SAE-3.02/SAE-3.02
```

## 7. Installation des dépendances Python

Cette étape est nécessaire sur la VM cliente, qui exécute l'interface graphique.

Créer un environnement Python :

```bash
python3 -m venv .venv
```

L'activer :

```bash
source .venv/bin/activate
```

Mettre pip à jour :

```bash
python -m pip install --upgrade pip
```

Installer les dépendances du projet :

```bash
python -m pip install -r requirements.txt
```

Le fichier `requirements.txt` contient notamment PyQt6.

Installer également les bibliothèques système nécessaires à l'affichage Qt si elles ne sont pas déjà présentes :

```bash
sudo apt install -y libxcb-cursor0 libxkbcommon-x11-0
```

L'installation du client est maintenant terminée.

## 8. Lancement du carrefour connecté

Le lancement doit obligatoirement se faire dans le bon ordre.

### 8.1. Démarrer le serveur (VM 1)

Sur la VM `SAE-SERVEUR`, se placer dans le dossier du projet :

```bash
cd ~/SAE-3.02/SAE-3.02
```

Démarrer le serveur TCP avec :

```bash
python3 -c 'from src.network import Server; s=Server(); s.start(); print("Serveur en attente de connexions sur le port 5000"); input("Appuyer sur Entrée pour arrêter le serveur...")'
```

Le serveur écoute maintenant les connexions entrantes sur le port TCP `5000`.

**Important :** ne pas fermer ce terminal pendant la démonstration.

### 8.2. Démarrer le client (VM 2)

Sur la VM `SAE-CLIENT`, ouvrir un autre terminal.

Se placer dans le dossier du projet :

```bash
cd ~/SAE-3.02/SAE-3.02
```

Activer l'environnement Python :

```bash
source .venv/bin/activate
```

Lancer l'application :

```bash
python src/main.py
```

La fenêtre graphique du carrefour connecté doit apparaître.

## 9. Tester le fonctionnement du projet

Une fois les deux machines démarrées :

1. Vérifier que le serveur est toujours en fonctionnement sur la VM 1.
2. Vérifier que l'interface graphique est ouverte sur la VM 2.
3. Cliquer sur **Démarrer**.
4. Cliquer sur **Ajouter voiture**.
5. Observer le terminal de la VM serveur.
6. Cliquer sur **Ajouter véhicule prioritaire**.
7. Observer les nouveaux messages reçus par le serveur.

### Exemple de message envoyé au serveur

```json
{
    "type": "vehicle",
    "id": 1,
    "priority": false
}
```

Pour un véhicule prioritaire :

```json
{
    "type": "vehicle",
    "id": 2,
    "priority": true
}
```

Le serveur affiche les messages reçus et renvoie une réponse de confirmation :

```json
{
    "status": "ok"
}
```

Les véhicules classiques sont représentés en bleu et les véhicules prioritaires en rouge dans l'interface graphique.

## 10. Base de données

Le projet utilise SQLite pour enregistrer les événements produits pendant la simulation.

Le fichier de base de données est :

```text
database/traffic.db
```

Il est créé automatiquement par l'application si nécessaire.

La base de données se trouve sur la VM cliente, car c'est cette machine qui gère la simulation et les événements.

Les événements enregistrés comprennent notamment :
- L'ajout d'une voiture.
- L'ajout d'un véhicule prioritaire.
- La réussite d'un envoi de message réseau.
- Les erreurs de communication avec le serveur.

Le serveur reçoit les messages et les affiche dans son terminal. Il ne stocke pas les événements dans sa propre base SQLite.

### Vérifier la présence de la base de données

Sur la VM cliente :

```bash
ls -l database/
```

Le fichier `traffic.db` doit apparaître après le premier lancement de l'application.

## 11. Arrêter le projet

Pour arrêter correctement le projet :

**Sur la VM cliente :**

1. Fermer la fenêtre de simulation.
2. Revenir dans le terminal.
3. Quitter l'environnement virtuel :

```bash
deactivate
```

**Sur la VM serveur :**

1. Revenir dans le terminal où le serveur fonctionne.
2. Utiliser `Ctrl + C` pour interrompre le programme.

Les deux machines virtuelles peuvent ensuite être arrêtées normalement.

## 12. Résolution des problèmes

### Le client ne communique pas avec le serveur

Vérifier :
- Que les deux machines sont démarrées.
- Que les deux cartes internes utilisent le réseau `SAE-INTERNE`.
- Que le serveur possède bien l'adresse `192.168.8.10`.
- Que le client possède bien l'adresse `192.168.8.11`.
- Que le serveur a bien été lancé avant le client.

Tester :

```bash
ping -c 4 192.168.8.10
```

### Le serveur ne reçoit aucun message

Vérifier que le serveur est toujours lancé et que le port TCP `5000` est accessible.

Sur le serveur :

```bash
sudo ss -lntp | grep 5000
```

Le port `5000` doit apparaître en écoute.

### Le client n'a pas accès à Internet

Vérifier :
- Que la carte NAT du serveur fonctionne.
- Que le transfert IPv4 est activé.
- Que les règles iptables sont présentes.
- Que la passerelle du client est `192.168.8.10`.

Sur le serveur, vérifier :

```bash
cat /proc/sys/net/ipv4/ip_forward
```

Le résultat doit être `1`.

### Erreur : No module named PyQt6

Sur la VM cliente, activer l'environnement virtuel :

```bash
source .venv/bin/activate
```

Puis réinstaller les dépendances :

```bash
python -m pip install -r requirements.txt
```

### L'interface graphique ne s'ouvre pas

Vérifier que Debian possède bien un environnement graphique et installer si nécessaire :

```bash
sudo apt install -y libxcb-cursor0 libxkbcommon-x11-0
```

### Le dépôt GitHub n'est pas à jour

Dans le dossier du projet, exécuter :

```bash
git pull
```

Cela permet de récupérer les dernières modifications publiées sur GitHub.

## 13. Architecture finale du déploiement

| Fonctionnalité | VM Serveur | VM Client |
|---|:---:|:---:|
| Système Debian | Oui | Oui |
| Récupération du dépôt GitHub | Oui | Oui |
| Interface graphique | Non | Oui |
| Simulation du carrefour | Non | Oui |
| Ajout de véhicules | Non | Oui |
| Ajout de véhicules prioritaires | Non | Oui |
| Communication TCP | Réception | Envoi |
| Messages JSON | Réception | Envoi |
| Base SQLite | Non | Oui |
| Accès Internet direct par NAT | Oui | Non |
| Accès Internet par passerelle | — | Oui |

## 14. Auteurs

Projet réalisé dans le cadre du BUT Réseaux et Télécommunications, parcours ROM.

- Jules Landauer
- Maël Sasorith

## 15. Conclusion

Ce projet permet de mettre en pratique plusieurs compétences du BUT Réseaux et Télécommunications :

- La configuration de machines virtuelles Debian.
- La configuration d'adresses IP et de cartes réseau.
- Le partage de connexion Internet.
- La communication entre deux machines avec TCP.
- L'échange de données au format JSON.
- Le développement d'une interface graphique avec Python et PyQt6.
- L'utilisation d'une base de données SQLite.

Le déploiement final repose sur une architecture client-serveur composée de deux machines virtuelles indépendantes qui communiquent au sein d'un réseau virtuel.
