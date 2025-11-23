# Travelling Salesman Problem

## Description
Trouvez le plus court circuit hamiltonien dans un graphe complet pondéré.

Vous devez visiter chaque ville exactement une fois et revenir à la ville de départ.

## Format de l'entrée
- La première ligne contient un entier `n` (2 ≤ n ≤ 15)
- Les `n` lignes suivantes contiennent `n` entiers — la matrice des distances

## Format de la sortie
Afficher la distance minimale du circuit.

## Contraintes
- 2 ≤ n ≤ 15
- 1 ≤ distance ≤ 1000
- Time limit: 2 secondes
- Memory limit: 256 MB

## Exemple d'entrée
4
0 10 15 20
10 0 35 25
15 35 0 30
20 25 30 0

## Exemple de sortie
80
