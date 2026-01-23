# projet_OCA
wadhah taches:
# Projet — Graphes : stats + cliques maximales

Ce dépôt fournit :
- Lecture des graphes **en listes d’adjacence** (CSV edge-list `u,v`)
- Fonctions de base : degré, degré max, degré moyen, nombre d’arêtes, distribution des degrés
- Stats sur les cliques maximales (compte + taille max)
- Mesure de temps d’exécution
- Une implémentation **baseline** de Bron–Kerbosch avec pivot (pour pouvoir tester le pipeline).
  Votre binôme peut remplacer `enumerate_maximal_cliques()` par la version optimisée (ordre de dégénérescence + orientation).

## Structure
```
src/community_cliques/
  graph_io.py
  graph_stats.py
  clique_enum.py
  clique_stats.py
  timing.py
  main.py
tests/
data/
```
## Lancer sur un dossier de graphes CSV
Depuis la racine du projet :

```bash
python -m community_cliques.main --data ./data
```
## Lancer les tests (unittest)
```bash
python -m unittest discover -s tests -p "test_*.py"
```
## Format attendu des graphes
- Un fichier par graphe
- Une arête par ligne : `u,v` (séparateur virgule)
- Lignes vides et commentaires ignorés (`#`, `%`, `//`)
- Graphe non orienté : on ajoute (u,v) et (v,u)
- Pas de doublons (voisins stockés dans un `set`)
