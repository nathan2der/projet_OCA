# Projet OCA : Détection de Communautés dans les Réseaux Sociaux

**Auteurs :** Nathan DEROUARD, Wadhah HMISSI 
**Encadrant :** Georges MANOUSSAKIS

## Description

Ce projet implémente un algorithme d'énumération de cliques maximales dans des graphes, basé sur l'article de Manoussakis (2019) "A new decomposition technique for maximal clique enumeration for sparse graphs". L'algorithme utilise l'ordre de dégénérescence combiné avec l'algorithme de Bron-Kerbosch avec pivot pour obtenir des performances optimales sur des graphes peu denses.

## Structure du Projet

```
projet_OCA/
├── src/
│   └── community_cliques/
│       ├── __init__.py
│       ├── graph_io.py          # Lecture des graphes depuis CSV
│       ├── graph_stats.py        # Calcul des statistiques des graphes
│       ├── clique_enum.py        # Algorithme baseline (Bron-Kerbosch)
│       ├── clique_stats.py       # Statistiques sur les cliques
│       ├── timing.py             # Mesure de temps d'exécution
│       ├── main.py               # Pipeline principal (baseline)
│       └── main_projet.py        # Script principal avec algorithme optimisé
├── tests/
│   ├── test_graph_io.py         # Tests de lecture de graphes
│   ├── test_graph_stats.py      # Tests des statistiques
│   ├── test_clique_enum.py      # Implémentation de l'algorithme optimisé
│   └── test_clique_stats.py     # Tests des statistiques de cliques
├── data/                         # Graphes d'entrée (CSV)
│   ├── graphe0.csv
│   ├── graphe1.csv
│   ├── graphe2.csv
│   ├── graphe3.csv
│   ├── graphe4.csv
│   └── graphe5.csv
├── enonce/                       # Documents du sujet
│   ├── sujet.pdf
│   └── papier.pdf
├── generate_tables.py            # Script pour générer les tableaux du rapport
├── test_projet.py                # Script de test complet
└── README.md                     # Ce fichier
```

## Prérequis

- **Python 3.8+** (testé avec Python 3.12)
- **Modules Python standard uniquement** (pas de dépendances externes requises)
- **Optionnel :** `matplotlib` pour générer les graphiques de distribution des degrés
  ```bash
  pip install matplotlib
  ```

## Installation

Aucune installation n'est nécessaire. Le projet utilise uniquement la bibliothèque standard de Python.

1. Clonez ou téléchargez le projet
2. Assurez-vous d'être dans le répertoire racine du projet

## Utilisation

### 1. Exécuter l'algorithme principal (recommandé)

Le script `main_projet.py` exécute l'algorithme optimisé sur tous les graphes :

```bash
# Depuis la racine du projet
python3 src/community_cliques/main_projet.py
```

**Options :**
```bash
# Spécifier un autre dossier de données
python3 src/community_cliques/main_projet.py --data data
```

**Résultat :** 
- Affiche un tableau avec les résultats pour chaque graphe
- Génère `resultats_finaux.csv` à la racine du projet

### 2. Exécuter le pipeline baseline

Le script `main.py` utilise l'algorithme baseline (Bron-Kerbosch simple) :

```bash
# Depuis la racine du projet
PYTHONPATH=src:$PYTHONPATH python3 -m community_cliques.main --data data
```



### 3. Exécuter les tests unitaires

```bash
# Tous les tests
PYTHONPATH=src:$PYTHONPATH python3 -m unittest discover -s tests -p "test_*.py" -v

# Un test spécifique
PYTHONPATH=src:$PYTHONPATH python3 -m unittest tests.test_graph_io -v
```

### 4. Test complet du projet

```bash
python3 test_projet.py
```



## Algorithme Implémenté

L'algorithme principal (`test_clique_enum.py`) implémente :

1. **Calcul de l'ordre de dégénérescence** (O(m))
   - Utilise un système de buckets pour un tri linéaire
   - Retourne l'ordre et la dégénérescence k

2. **Algorithme de Bron-Kerbosch avec pivot**
   - Optimisation pour réduire l'espace de recherche
   - Utilise une table de hachage (set de frozensets) au lieu d'un arbre de suffixes

3. **Algorithme principal**
   - Parcourt les sommets selon l'ordre de dégénérescence
   - Pour chaque sommet, cherche les cliques avec ses voisins "futurs"
   - Évite les doublons grâce à la table de hachage

