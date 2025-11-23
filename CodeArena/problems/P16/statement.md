# Edit Distance

## Description
Calculez la distance d'édition minimale entre deux chaînes.

Les opérations permises sont:
- Insérer un caractère
- Supprimer un caractère
- Remplacer un caractère

## Format de l'entrée
- La première ligne contient la chaîne `s1` (1 ≤ |s1| ≤ 1000)
- La deuxième ligne contient la chaîne `s2` (1 ≤ |s2| ≤ 1000)

## Format de la sortie
Afficher le nombre minimum d'opérations.

## Contraintes
- 1 ≤ |s1|, |s2| ≤ 1000
- Chaînes en minuscules
- Time limit: 2 secondes
- Memory limit: 256 MB

## Exemple d'entrée
horse
ros

## Exemple de sortie
3

## Explication
horse → rorse (remplacer h par r)
rorse → rose (supprimer r)
rose → ros (supprimer e)
