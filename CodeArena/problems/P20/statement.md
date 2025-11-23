# Knapsack Problem

## Description
Vous avez un sac à dos de capacité W et n objets avec des poids et des valeurs.

Maximisez la valeur totale sans dépasser la capacité.

## Format de l'entrée
- La première ligne contient deux entiers `n` et `W` (1 ≤ n ≤ 1000, 1 ≤ W ≤ 10000)
- Les `n` lignes suivantes contiennent deux entiers `wᵢ` et `vᵢ` — poids et valeur de l'objet i

## Format de la sortie
Afficher la valeur maximale possible.

## Contraintes
- 1 ≤ n ≤ 1000
- 1 ≤ W ≤ 10000
- 1 ≤ wᵢ, vᵢ ≤ 1000
- Time limit: 2 secondes
- Memory limit: 256 MB

## Exemple d'entrée
4 7
1 1
3 4
4 5
5 7

## Exemple de sortie
9

## Explication
Prendre les objets 2 et 3: poids = 3+4 = 7, valeur = 4+5 = 9