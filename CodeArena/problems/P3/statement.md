# Count Inversions

## Description
Un tableau contient une inversion si deux éléments sont dans le mauvais ordre. Plus formellement, une paire (i, j) est une inversion si i < j mais a[i] > a[j].

Comptez le nombre total d'inversions dans le tableau.

## Format de l'entrée
- La première ligne contient un entier `n` (1 ≤ n ≤ 100000)
- La deuxième ligne contient `n` entiers `a₁, a₂, ..., aₙ` (1 ≤ aᵢ ≤ 10⁹)

## Format de la sortie
Afficher un seul entier — le nombre d'inversions.

## Contraintes
- 1 ≤ n ≤ 100000
- 1 ≤ aᵢ ≤ 10⁹
- Time limit: 2 secondes
- Memory limit: 256 MB

## Exemple d'entrée
5
2 4 1 3 5

## Exemple de sortie
3

## Explication
Les inversions sont: (2,1), (4,1), (4,3)