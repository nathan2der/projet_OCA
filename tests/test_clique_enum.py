# Fichier: test_clique_enum.py

def get_degeneracy_ordering(adj_list):
    """
    Tâche 4 : Calcul de l'ordre de dégénérescence (Algo 1 du papier).
    Retourne l'ordre et le rang de chaque noeud.
    """
    degrees = {v: len(neighbors) for v, neighbors in adj_list.items()}
    max_degree = max(degrees.values()) if degrees else 0
    
    D = [set() for _ in range(max_degree + 1)]
    for v, deg in degrees.items():
        D[deg].add(v)
    
    ordering = [] # Liste L
    # On garde aussi un dictionnaire pour connaître la position (rang) de chaque noeud en O(1)
    rank = {} 
    
    k_max = 0
    i = 0
    num_vertices = len(degrees)
    removed = set()

    for pos in range(num_vertices):
        while i < len(D) and not D[i]:
            i += 1
        if i >= len(D): break
            
        k_max = max(k_max, i)
        v = D[i].pop()
        
        ordering.append(v)
        rank[v] = pos # v est à la position 'pos' dans l'ordre de dégénérescence
        removed.add(v)
        
        for w in adj_list[v]:
            if w not in removed:
                old_deg = degrees[w]
                if old_deg > i:
                    if w in D[old_deg]:
                        D[old_deg].remove(w)
                        new_deg = old_deg - 1
                        degrees[w] = new_deg
                        D[new_deg].add(w)
                        if new_deg < i:
                            i = new_deg
                            
    return ordering, k_max, rank

def bron_kerbosch_pivot(P, R, X, adj_list, clique_storage):
    """
    Tâche 5 : Bron-Kerbosch avec Pivot.
    Note : On passe 'clique_storage' (dict) au lieu d'une liste.
    """
    if not P and not X:
        # Stockage sous forme de Hachage (Table de hachage simulée par un set/dict)
        # On utilise un frozenset comme clé car c'est hachable
        c = frozenset(R)
        # On ne stocke que si c'est nouveau (bien que BK garantisse l'unicité par branche)
        clique_storage.add(c) 
        return

    # Pivot : u dans P U X qui maximise |P inter N(u)|
    # Optimisation : On utilise len() direct car adj_list est un set
    pivot = max(P.union(X), key=lambda u: len(P.intersection(adj_list[u])), default=None)
    
    if pivot is None: # Sécurité si P U X est vide
        return

    # P \ N(pivot)
    candidates = P.difference(adj_list[pivot])
    
    for v in candidates:
        new_R = R.union({v})
        new_P = P.intersection(adj_list[v])
        new_X = X.intersection(adj_list[v])
        
        bron_kerbosch_pivot(new_P, new_R, new_X, adj_list, clique_storage)
        
        P.remove(v)
        X.add(v)

def find_cliques_main(adj_list):
    """
    Tâche 6 (Revisité) : Algorithme Principal Conforme.
    - Utilise explicitement l'ordre pour trier les listes d'adjacence (G_i implicite).
    - Utilise un Set (Table de Hachage) pour le stockage [Source: 27].
    """
    # 1. Calcul de l'ordre et des rangs
    ordering, k_degeneracy, rank = get_degeneracy_ordering(adj_list)
    
    # 2. Pré-traitement : Conversion en Sets pour rapidité ET respect de l'ordre
    # Bien que BK gère les sets, avoir l'accès rapide est crucial.
    adj_sets = {u: set(v) for u, v in adj_list.items()}
    
    # 3. Structure de stockage conforme au sujet (remplace l'arbre des suffixes)
    # Un set de frozensets agit comme une table de hachage des cliques trouvées.
    cliques_hash_table = set()
    
    # 4. Boucle principale conforme au concept G_i du papier
    # On itère v dans l'ordre de dégénérescence.
    # Pour chaque v, on cherche les cliques qui contiennent v et ses voisins SUIVANTS.
    # Les voisins PRECEDENTS servent uniquement à l'exclusion (X).
    
    for v in ordering:
        neighbors = adj_sets[v]
        
        # Construction explicite des ensembles basée sur le RANG (Définition 2 du papier)
        v_rank = rank[v]
        
        # P = Voisins de v qui ont un rang > rang(v) (apparaissent APRES dans l'ordre)
        P = {n for n in neighbors if rank[n] > v_rank}
        
        # X = Voisins de v qui ont un rang < rang(v) (apparaissent AVANT dans l'ordre)
        X = {n for n in neighbors if rank[n] < v_rank}
        
        R = {v}
        
        # Appel de la sous-routine sur ce sous-graphe restreint
        bron_kerbosch_pivot(P, R, X, adj_sets, cliques_hash_table)
        
    # Conversion finale en liste pour le rapport
    return list(cliques_hash_table), k_degeneracy
