# Segment Tree Range Queries

## Description
Construisez un segment tree pour répondre à des requêtes de somme sur un intervalle et des mises à jour ponctuelles.

## Format de l'entrée
- La première ligne contient deux entiers `n` et `q` (1 ≤ n, q ≤ 200000)
- La deuxième ligne contient `n` entiers — le tableau initial
- Les `q` lignes suivantes contiennent des requêtes de deux types:
  - `1 i x` : mettre a[i] = x
  - `2 l r` : calculer la somme de a[l] à a[r]

## Format de la sortie
Pour chaque requête de type 2, afficher la somme.

## Contraintes
- 1 ≤ n, q ≤ 200000
- 1 ≤ aᵢ, x ≤ 10⁹
- Time limit: 2 secondes
- Memory limit: 256 MB

## Exemple d'entrée
5 3
1 3 5 7 9
2 1 5
1 3 6
2 1 5

## Exemple de sortie
25
26
