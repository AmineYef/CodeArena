# Longest Increasing Subsequence

## Description
Trouvez la longueur de la plus longue sous-séquence strictement croissante dans un tableau.

Une sous-séquence est une séquence qui peut être dérivée du tableau en supprimant certains éléments sans changer l'ordre des éléments restants.

## Format de l'entrée
- La première ligne contient un entier `n` (1 ≤ n ≤ 100000)
- La deuxième ligne contient `n` entiers (1 ≤ aᵢ ≤ 10⁹)

## Format de la sortie
Afficher un seul entier — la longueur de la LIS.

## Contraintes
- 1 ≤ n ≤ 100000
- 1 ≤ aᵢ ≤ 10⁹
- Time limit: 2 secondes
- Memory limit: 256 MB

## Exemple d'entrée
8
10 9 2 5 3 7 101 18

## Exemple de sortie
4

## Explication
La LIS est [2, 3, 7, 18] ou [2, 5, 7, 18] (longueur 4).