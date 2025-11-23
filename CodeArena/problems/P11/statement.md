# Valid Sudoku

## Description
Déterminez si une grille Sudoku 9x9 partiellement remplie est valide.

Une grille Sudoku valide respecte ces règles:
- Chaque ligne contient les chiffres 1-9 sans répétition
- Chaque colonne contient les chiffres 1-9 sans répétition
- Chaque sous-grille 3x3 contient les chiffres 1-9 sans répétition

Les cases vides sont représentées par '.'.

## Format de l'entrée
- 9 lignes contenant chacune 9 caractères (chiffre 1-9 ou '.')

## Format de la sortie
Afficher "YES" si la grille est valide, "NO" sinon.

## Contraintes
- La grille est toujours 9x9
- Caractères valides: 1-9 et '.'
- Time limit: 2 secondes
- Memory limit: 256 MB

## Exemple d'entrée
53..7....
6..195...
.98....6.
8...6...3
4..8.3..1
7...2...6
.6....28.
...419..5
....8..79

## Exemple de sortie
YES