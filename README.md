# CodeArena - Plateforme de Contest de Programmation

## Vue d'ensemble

CodeArena est une plateforme de compétition de programmation en temps réel permettant à plusieurs utilisateurs de participer simultanément à des contests chronométrés. Le système évalue automatiquement les soumissions et maintient un classement dynamique.

## Fonctionnalités principales

### Contests en temps réel
- Timer global synchronisé pour tous les participants
- Durée configurable (15 à 180 minutes)
- Sélection automatique de problèmes par difficulté
- Blocage des soumissions après expiration du temps

### Support multi-langages
- **Python** : exécution directe
- **C++** : compilation avec g++ puis exécution
- **Java** : compilation avec javac puis exécution
- Détection automatique du langage

### Système d'évaluation
- Compilation automatique si nécessaire
- Exécution avec timeout (2 secondes)
- Comparaison de sortie ligne par ligne
- Verdicts : `OK`, `WRONG_ANSWER`, `TIMEOUT`, `COMPILATION_ERROR`, `RUNTIME_ERROR`

### Scoring et classement
- **OK** : +100 points
- **Wrong Answer** : -10 points
- **Timeout** : -20 points
- **Erreurs de compilation/runtime** : -10 points
- Leaderboard mis à jour en temps réel
- Suivi des tentatives par problème

### Interface web complète
- Dashboard avec vue d'ensemble du contest
- Éditeur de code intégré
- Feedback instantané sur les soumissions
- Affichage des statistiques utilisateur
- Page de classement en temps réel

## Technologies utilisées

### Backend
- Python 3.8+
- Flask pour le serveur web
- Threading pour la gestion multi-clients
- Multiprocessing pour l'exécution parallèle
- Subprocess pour l'exécution du code

### Frontend
- HTML5, CSS3, JavaScript
- Markdown pour les énoncés de problèmes
- Refresh automatique des données

### Langages supportés
- Python 3
- C++ (standard C++17)
- Java (JDK 11+)

## Concepts techniques appliqués

### Multithreading
- Gestion de connexions clients simultanées
- Thread par soumission pour l'évaluation
- Communication non-bloquante

### Multiprocessing
- Pool de workers pour exécution parallèle
- Isolation des processus pour la sécurité
- Utilisation optimale des cœurs CPU

### Synchronisation
- Gestion thread-safe du leaderboard
- Tracking des tentatives par utilisateur
- Timer global synchronisé

### Gestion des ressources
- Timeout d'exécution (2 secondes)
- Limite de mémoire (256 MB)
- Nettoyage automatique des fichiers temporaires

### Sécurité
- Exécution isolée dans des processus séparés
- Validation des entrées utilisateur
- Détection de langage pour éviter les erreurs

## Problèmes disponibles

Le système inclut 21 problèmes classés par difficulté :

### Easy (7 problèmes)
- Two Sum, Palindrome Check, Count Inversions
- Missing Number, Valid Parentheses, Frequency Sort, Binary Search

### Medium (7 problèmes)
- Longest Increasing Subsequence, Coin Change, Kth Largest Element
- Valid Sudoku, Number of Islands, Minimum Window Substring, Dijkstra

### Hard (7 problèmes)
- Topological Sort, Edit Distance, Maximum Flow
- Segment Tree, TSP, Knapsack, Strongly Connected Components

**Chaque problème contient :**
- Énoncé détaillé en Markdown
- Contraintes et limites
- Exemples d'entrée/sortie
- Tests automatiques

## Exemple d'utilisation

### Scénario typique :

1. Le professeur crée un contest de 30 minutes avec 3 problèmes de difficulté moyenne
2. Les étudiants se connectent et entrent leur nom d'utilisateur
3. Chaque étudiant choisit un problème et soumet sa solution
4. Le système compile et exécute le code automatiquement
5. Le verdict apparaît instantanément (OK, WRONG_ANSWER, etc.)
6. Le leaderboard se met à jour après chaque soumission
7. À la fin du timer, le classement final est affiché

### Verdicts possibles :
- **OK** : Solution correcte (+100 points)
- **WRONG_ANSWER** : Sortie incorrecte (-10 points)
- **TIMEOUT** : Temps d'exécution dépassé (-20 points)
- **COMPILATION_ERROR** : Erreur de compilation (-10 points)
- **RUNTIME_ERROR** : Erreur pendant l'exécution (-10 points)

## Auteur

Mohamed Amine Yeferni - Projet de Systèmes Parallèles et Distribués
