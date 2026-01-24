#!/usr/bin/env python3
"""
Script de test pour valider l'implémentation du projet.
Teste les algorithmes sur les graphes fournis.
"""

import sys
from pathlib import Path
import time

# Ajouter les dossiers nécessaires au path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "src"))
sys.path.insert(0, str(project_root / "tests"))

# Importer les modules nécessaires
from community_cliques.graph_io import read_graph
from test_clique_enum import find_cliques_main

def test_graph(graph_path: Path) -> dict:
    """Teste un graphe et retourne les statistiques."""
    print(f"\n{'='*60}")
    print(f"Test de {graph_path.name}")
    print(f"{'='*60}")
    
    # Charger le graphe
    try:
        graph = read_graph(str(graph_path), delimiter=",", cast_int=True)
        print(f"✓ Graphe chargé: {len(graph)} sommets")
    except Exception as e:
        print(f"✗ Erreur lors du chargement: {e}")
        return None
    
    # Convertir le format du graphe (dict de sets) vers le format attendu (dict de listes)
    adj_list = {node: list(neighbors) for node, neighbors in graph.items()}
    
    # Tester l'algorithme
    try:
        start_time = time.perf_counter()
        cliques, k_degeneracy = find_cliques_main(adj_list)
        end_time = time.perf_counter()
        duration = end_time - start_time
        
        # Calculer les statistiques
        nb_cliques = len(cliques)
        max_size = max([len(c) for c in cliques]) if cliques else 0
        
        print(f"✓ Dégénérescence k: {k_degeneracy}")
        print(f"✓ Nombre de cliques maximales: {nb_cliques}")
        print(f"✓ Taille maximale d'une clique: {max_size}")
        print(f"✓ Temps d'exécution: {duration:.6f} secondes")
        
        # Afficher quelques cliques (max 5) pour vérification
        if cliques:
            print(f"\nExemples de cliques (max 5):")
            for i, clique in enumerate(sorted(cliques, key=len, reverse=True)[:5]):
                print(f"  - Clique de taille {len(clique)}: {sorted(clique)}")
        
        return {
            "graphe": graph_path.name,
            "sommets": len(graph),
            "dégénérescence": k_degeneracy,
            "nb_cliques": nb_cliques,
            "taille_max": max_size,
            "temps": duration
        }
        
    except Exception as e:
        print(f"✗ Erreur lors de l'exécution: {e}")
        import traceback
        traceback.print_exc()
        return None

def main():
    """Fonction principale de test."""
    # Trouver les graphes
    data_dir = Path(__file__).parent / "data"
    
    if not data_dir.exists():
        print(f"✗ Dossier {data_dir} introuvable!")
        return
    
    graph_files = sorted([f for f in data_dir.iterdir() if f.suffix.lower() == ".csv"])
    
    if not graph_files:
        print(f"✗ Aucun fichier .csv trouvé dans {data_dir}")
        return
    
    print(f"Trouvé {len(graph_files)} graphe(s) à tester")
    
    # Tester chaque graphe
    results = []
    for graph_file in graph_files:
        result = test_graph(graph_file)
        if result:
            results.append(result)
    
    # Résumé
    print(f"\n{'='*60}")
    print("RÉSUMÉ DES RÉSULTATS")
    print(f"{'='*60}")
    print(f"{'Graphe':<15} | {'k':<5} | {'Cliques':<10} | {'Taille max':<10} | {'Temps (s)':<12}")
    print("-" * 60)
    
    for r in results:
        print(f"{r['graphe']:<15} | {r['dégénérescence']:<5} | {r['nb_cliques']:<10} | {r['taille_max']:<10} | {r['temps']:<12.6f}")
    
    print(f"\n✓ {len(results)} graphe(s) testé(s) avec succès!")

if __name__ == "__main__":
    main()
