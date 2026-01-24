# Fichier: main_projet.py
import time
import os
import pandas as pd

# Import des modules du collègue et du vôtre
# NOTE : Vérifiez le nom de la fonction de chargement dans test_graph_io.py
# J'assume ici qu'elle s'appelle 'load_adjacency_list' ou 'read_graph'
from test_graph_io import test_read_graph_csv # <--- AJUSTEZ CE NOM SI NÉCESSAIRE
from test_clique_enum import find_cliques_main

def process_graphs():
    fichiers = ["graphe0.csv", "graphe1.csv", "graphe2.csv", 
                "graphe3.csv", "graphe4.csv", "graphe5.csv"]
    
    resultats = []
    
    print(f"{'Graphe':<15} | {'Dégénérescence':<15} | {'Nb Cliques':<12} | {'Taille Max':<12} | {'Temps (s)':<10}")
    print("-" * 80)
    
    for fichier in fichiers:
        if not os.path.exists(fichier):
            print(f"Fichier {fichier} introuvable.")
            continue
            
        # 1. Chargement (Code du collègue)
        # On suppose que load_graph retourne un dict {noeud: [voisins]}
        adj_list = test_read_graph_csv(fichier) 
        
        # 2. Exécution de VOTRE algo (Tâches 4, 5, 6)
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
    df = pd.DataFrame(resultats)
    df.to_csv("resultats_finaux.csv", index=False)
    print("\nLes résultats ont été sauvegardés dans 'resultats_finaux.csv'.")

if __name__ == "__main__":
    process_graphs()
