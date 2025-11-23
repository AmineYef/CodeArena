# Coin Change

## Description
Vous avez des pièces de monnaie de différentes valeurs en quantité illimitée.

Trouvez le nombre minimum de pièces nécessaires pour obtenir exactement la somme cible.

Si c'est impossible, retournez -1.

## Format de l'entrée
- La première ligne contient deux entiers `n` et `target` (1 ≤ n ≤ 100, 1 ≤ target ≤ 10000)
- La deuxième ligne contient `n` entiers — les valeurs des pièces (1 ≤ cᵢ ≤ 10000)

## Format de la sortie
Afficher le nombre minimum de pièces ou -1 si impossible.

## Contraintes
- 1 ≤ n ≤ 100
- 1 ≤ target ≤ 10000
- 1 ≤ cᵢ ≤ 10000
- Time limit: 2 secondes
- Memory limit: 256 MB

## Exemple d'entrée
3 11
1 2 5

## Exemple de sortie
3

## Explication
11 = 5 + 5 + 1 (3 pièces)