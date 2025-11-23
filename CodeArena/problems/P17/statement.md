# Maximum Flow

## Description
Calculez le flux maximum d'un réseau de flot.

Étant donné un graphe dirigé avec des capacités sur les arêtes, trouvez le flux maximum de la source au puits.

## Format de l'entrée
- La première ligne contient quatre entiers `n`, `m`, `source`, `sink` (2 ≤ n ≤ 500, 0 ≤ m ≤ 10000)
- Les `m` lignes suivantes contiennent trois entiers `u`, `v`, `c` — une arête de u à v avec capacité c (1 ≤ c ≤ 1000)

## Format de la sortie
Afficher le flux maximum.

## Contraintes
- 2 ≤ n ≤ 500
- 0 ≤ m ≤ 10000
- 1 ≤ c ≤ 1000
- Time limit: 2 secondes
- Memory limit: 256 MB

## Exemple d'entrée
6 9 1 6
1 2 16
1 3 13
2 3 10
2 4 12
3 2 4
3 5 14
4 3 9
4 6 20
5 4 7
5 6 4

## Exemple de sortie
23
