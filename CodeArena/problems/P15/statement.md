# Topological Sort

## Description
Étant donné un graphe orienté acyclique (DAG), effectuez un tri topologique.

Un tri topologique est un ordonnancement linéaire des sommets tel que pour chaque arête u→v, u vient avant v.

## Format de l'entrée
- La première ligne contient deux entiers `n` et `m` (1 ≤ n ≤ 100000, 0 ≤ m ≤ 200000)
- Les `m` lignes suivantes contiennent deux entiers `u` et `v` — une arête dirigée de u vers v

## Format de la sortie
Afficher n entiers — un tri topologique valide.
S'il y a un cycle, afficher "-1".

## Contraintes
- 1 ≤ n ≤ 100000
- 0 ≤ m ≤ 200000
- Time limit: 2 secondes
- Memory limit: 256 MB

## Exemple d'entrée
6 6
5 2
5 0
4 0
4 1
2 3
3 1

## Exemple de sortie
4 5 0 2 3 1
