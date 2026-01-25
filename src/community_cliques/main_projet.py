# Fichier: main_projet.py
import time
import os
import sys
from pathlib import Path
import csv

# Ajouter les chemins nécessaires
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root / "src"))
sys.path.insert(0, str(project_root / "tests"))

# Import des modules
from community_cliques.graph_io import read_graph
from test_clique_enum import find_cliques_main

def process_graphs(data_dir="data"):
    """
    Traite tous les graphes dans le dossier data_dir.
    
    Args:
        data_dir: Chemin vers le dossier contenant les fichiers CSV
    """
    data_path = Path(project_root) / data_dir
    fichiers = ["graphe0.csv", "graphe1.csv", "graphe2.csv", 
                "graphe3.csv", "graphe4.csv", "graphe5.csv"]
    
    resultats = []
    
    print(f"{'Graphe':<15} | {'Dégénérescence':<15} | {'Nb Cliques':<12} | {'Taille Max':<12} | {'Temps (s)':<10}")
    print("-" * 80)
    
    for fichier in fichiers:
        fichier_path = data_path / fichier
        if not fichier_path.exists():
            print(f"Fichier {fichier} introuvable dans {data_path}.")
            continue
            
        # 1. Chargement du graphe (retourne dict {noeud: set(voisins)})
        graph = read_graph(str(fichier_path), delimiter=",", cast_int=True)
        
        # 2. Conversion en format attendu par find_cliques_main (dict {noeud: list(voisins)})
        adj_list = {node: list(neighbors) for node, neighbors in graph.items()} 
        
        # 3. Exécution de l'algorithme (Tâches 4, 5, 6)
        start_time = time.time()
        cliques, k_degen = find_cliques_main(adj_list)
        end_time = time.time()
        
        duration = end_time - start_time
        nb_cliques = len(cliques)
        max_size = max([len(c) for c in cliques]) if cliques else 0
        
        # Affichage console
        print(f"{fichier:<15} | {k_degen:<15} | {nb_cliques:<12} | {max_size:<12} | {duration:.4f}")
        
        # Stockage pour le rapport
        resultats.append({
            "Graphe": fichier,
            "Dégénérescence": k_degen,
            "Nombre Cliques": nb_cliques,
            "Taille Max": max_size,
            "Temps (s)": round(duration, 4)
        })
    
    # Sauvegarde des résultats
    if resultats:
        output_path = project_root / "resultats_finaux.csv"
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            if resultats:
                writer = csv.DictWriter(f, fieldnames=resultats[0].keys())
                writer.writeheader()
                writer.writerows(resultats)
        print(f"\n✓ Les résultats ont été sauvegardés dans '{output_path}'.")
    else:
        print("\n✗ Aucun résultat à sauvegarder.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Exécute l'algorithme d'énumération de cliques maximales sur tous les graphes")
    parser.add_argument("--data", type=str, default="data", help="Dossier contenant les graphes CSV (par défaut: data)")
    args = parser.parse_args()
    
    process_graphs(args.data)
