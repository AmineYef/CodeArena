# CodeArena - Plateforme de Contest de Programmation en Temps Réel

## À propos du projet

CodeArena est une plateforme qui permet à plusieurs utilisateurs de participer à des compétitions de programmation en temps réel. Le système reçoit du code en Python, C++ ou Java, l'exécute automatiquement, et donne les résultats instantanément.

C'est comme une version simplifiée de Codeforces ou HackerRank, développée pour démontrer les concepts de systèmes parallèles et distribués.

## Comment ça marche

Le principe est simple :

1. Plusieurs personnes se connectent au serveur en même temps
2. Un contest démarre avec un timer et une liste de problèmes
3. Chaque participant envoie son code pour résoudre un problème
4. Le serveur exécute le code, vérifie si c'est correct, et donne un score
5. Un classement en temps réel est affiché à tous les participants
6. À la fin du contest, le gagnant est celui qui a le meilleur score

## Fonctionnalités principales

**Contest en temps réel**
- Un timer global pour tous les participants
- Durée configurable (exemple : 30 minutes)
- Liste de problèmes à résoudre
- Les soumissions sont acceptées uniquement pendant la durée du contest

**Support de plusieurs utilisateurs**
- Plusieurs personnes peuvent se connecter en même temps
- Chaque utilisateur a son propre thread
- Communication instantanée entre serveur et clients

**Trois langages de programmation supportés**
- Python (exécution directe)
- C++ (compilation avec g++ puis exécution)
- Java (compilation avec javac puis exécution)

**Évaluation automatique**
- Le système compile le code si nécessaire
- Exécute le programme avec un timeout pour éviter les boucles infinies
- Compare le résultat avec la réponse attendue
- Donne un verdict :
  - OK : solution correcte (+100 points)
  - WRONG ANSWER : mauvaise réponse (-10 points)
  - TIMEOUT : programme trop lent (-20 points)
  - COMPILATION ERROR : erreur de compilation (-5 points)
  - RUNTIME ERROR : erreur pendant l'exécution (-10 points)

**Classement dynamique**
- Mis à jour après chaque soumission
- Affiche le score, les problèmes résolus, et le temps
- Visible par tous les participants en temps réel

**Dashboard web**
- Interface pour voir l'état du contest
- Affiche le timer, le classement, et les statistiques
- Montre combien de tâches sont en attente
- Affiche les logs du système

## Architecture du système

Le projet est composé de plusieurs parties qui travaillent ensemble :

**Clients**
- Les participants se connectent via des sockets TCP
- Chaque client envoie son code et reçoit les résultats
- Affiche le classement et le timer

**Serveur**
- Reçoit les connexions des clients
- Gère un thread pour chaque client
- Place les soumissions dans une file d'attente
- Distribue le travail aux workers
- Met à jour le classement
- Envoie les résultats aux clients

**Workers (processus parallèles)**
- Pool de processus qui exécutent le code
- Chaque worker prend une soumission de la file d'attente
- Compile le code si nécessaire
- Exécute le programme avec un timeout
- Renvoie le résultat au serveur

**Judge (évaluateur)**
- Compare la sortie du programme avec la réponse attendue
- Génère le verdict (OK, WRONG, TIMEOUT, etc.)
- Calcule le score

**Dashboard web**
- Serveur Flask séparé
- Affiche les informations en temps réel
- Interface pour monitorer le système

## Technologies utilisées

- Python 3.8 ou plus récent
- Sockets TCP pour la communication réseau
- Threading pour gérer plusieurs clients
- Multiprocessing pour exécuter le code en parallèle
- Queue pour synchroniser les tâches
- Flask pour le dashboard web
- g++ pour compiler le C++
- javac et java pour compiler et exécuter Java

## Installation

**Prérequis**

Avant de commencer, assurez-vous d'avoir :
- Python 3.8 ou plus récent
- g++ (pour compiler le C++)
- JDK 11 ou plus récent (pour compiler et exécuter Java)

**Étapes d'installation**

1. Cloner le projet
```bash
git clone https://github.com/VOTRE_USERNAME/CodeArena.git
cd CodeArena
```

2. Créer un environnement virtuel (recommandé)
```bash
python3 -m venv venv
source venv/bin/activate  # Sur Linux/Mac
# ou
venv\Scripts\activate  # Sur Windows
```

3. Installer les dépendances Python
```bash
pip install -r requirements.txt
```

4. Vérifier que les compilateurs sont installés
```bash
g++ --version
javac -version
java -version
```

## Utilisation

**Démarrer le serveur**
```bash
python server/main.py
```

**Lancer le dashboard web**
```bash
python dashboard/app.py
```
Puis ouvrir http://localhost:8080 dans votre navigateur

**Connecter un client**
```bash
python client/main.py
```

## Structure du projet

```
CodeArena/
│
├── server/                     # Code du serveur
│   ├── main.py                 # Point d'entrée
│   ├── socket_server.py        # Gestion des sockets
│   ├── contest_manager.py      # Gestion du contest
│   ├── submission_queue.py     # File d'attente
│   └── config.py               # Configuration
│
├── workers/                    # Workers pour exécuter le code
│   ├── worker_pool.py          # Pool de processus
│   ├── judge.py                # Évaluation
│   ├── compiler.py             # Compilation C++/Java
│   └── executor.py             # Exécution
│
├── client/                     # Code du client
│   ├── main.py                 # Point d'entrée
│   ├── socket_client.py        # Communication
│   └── ui.py                   # Interface
│
├── dashboard/                  # Dashboard web
│   ├── app.py                  # Serveur Flask
│   ├── templates/              # Pages HTML
│   └── static/                 # CSS et JavaScript
│
├── data/
│   ├── problems/               # Définitions des problèmes
│   └── submissions/            # Historique
│
├── tests/                      # Tests unitaires
│
├── requirements.txt            # Dépendances
└── README.md                   # Ce fichier
```

## Concepts techniques mis en pratique

Ce projet démontre plusieurs concepts importants des systèmes parallèles et distribués :

**Multithreading**
- Un thread est créé pour chaque client connecté
- Permet à plusieurs utilisateurs de soumettre du code en même temps
- Communication non-bloquante

**Multiprocessing**
- Un pool de processus exécute le code en parallèle
- Chaque soumission s'exécute dans un processus isolé
- Utilise plusieurs cœurs du processeur

**Sockets réseau**
- Communication TCP entre clients et serveur
- Échange de données en format JSON
- Gestion des connexions et déconnexions

**Synchronisation**
- File d'attente thread-safe pour les soumissions
- Locks pour protéger le leaderboard
- Events pour le timer global

**Architecture distribuée**
- Séparation entre serveur, workers et dashboard
- Composants qui communiquent entre eux
- Système modulaire et extensible

## Exemple d'utilisation

Scénario typique :

1. Le professeur lance un contest de 30 minutes avec 3 problèmes
2. Trois étudiants se connectent : Ali, Mariem et Yassine
3. Ali soumet une solution Python pour le problème 1 : résultat OK, +100 points
4. Mariem soumet du C++ pour le problème 3 : WRONG ANSWER, puis OK, +90 points
5. Yassine soumet du Java pour le problème 2 : TIMEOUT, -20 points
6. Le classement est mis à jour après chaque soumission
7. Le dashboard affiche l'état en temps réel
8. À la fin des 30 minutes, le classement final est affiché

## Auteur

Développé par Mohamed Amine Yeferni dans le cadre du module Systèmes Parallèles et Distribués.

