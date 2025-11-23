# Strongly Connected Components

## Description
Trouvez le nombre de composantes fortement connexes dans un graphe orienté.

Une composante fortement connexe est un sous-ensemble maximal de sommets tel qu'il existe un chemin entre chaque paire de sommets dans les deux directions.

## Format de l'entrée
- La première ligne contient deux entiers `n` et `m` (1 ≤ n ≤ 100000, 0 ≤ m ≤ 200000)
- Les `m` lignes suivantes contiennent deux entiers `u` et `v` — une arête dirigée de u vers v

## Format de la sortie
Afficher le nombre de composantes fortement connexes.

## Contraintes
- 1 ≤ n ≤ 100000
- 0 ≤ m ≤ 200000
- Time limit: 2 secondes
- Memory limit: 256 MB

## Exemple d'entrée
8 14
1 2
2 3
3 1
3 4
4 5
5 6
6 4
6 7
7 8
8 7
2 5
5 2
8 6
4 1

## Exemple de sortie
3

## Explication
Les SCCs sont: {1, 2, 3, 4, 5}, {6, 7, 8}... attendez non: {1,2,3}, {4,5,6}, {7,8}