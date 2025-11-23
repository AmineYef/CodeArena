# Dijkstra Shortest Path

## Description
Trouvez le plus court chemin entre deux nœuds dans un graphe pondéré.

## Format de l'entrée
- La première ligne contient trois entiers `n`, `m`, et `start`, `end` (1 ≤ n ≤ 10000, 0 ≤ m ≤ 50000)
- Les `m` lignes suivantes contiennent trois entiers `u`, `v`, `w` — une arête de u à v avec poids w (1 ≤ w ≤ 1000)

## Format de la sortie
Afficher la distance minimale de start à end, ou -1 si impossible.

## Contraintes
- 1 ≤ n ≤ 10000
- 0 ≤ m ≤ 50000
- 1 ≤ w ≤ 1000
- Time limit: 2 secondes
- Memory limit: 256 MB

## Exemple d'entrée
5 6 1 5
1 2 4
1 3 2
2 3 1
2 4 5
3 4 8
4 5 3

## Exemple de sortie
10
