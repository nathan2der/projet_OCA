from __future__ import annotations

import argparse
import os
from pathlib import Path

from .graph_io import read_graph
from .graph_stats import number_of_edges, max_degree, average_degree, degree_distribution
from .clique_enum import enumerate_maximal_cliques
from .clique_stats import compute_clique_stats
from .timing import time_call


def run_on_file(path: Path) -> None:
    graph = read_graph(str(path), delimiter=",", cast_int=True)

    n = len(graph)
    m = number_of_edges(graph)
    dmax = max_degree(graph)
    davg = average_degree(graph)
    dist = degree_distribution(graph)

    # Cliques + timing
    def compute():
        return compute_clique_stats(enumerate_maximal_cliques(graph), store=False)

    stats, t = time_call(compute)

    print(f"=== {path.name} ===")
    print(f"n (sommets)          : {n}")
    print(f"m (arêtes)           : {m}")
    print(f"deg max              : {dmax}")
    print(f"deg moyen            : {davg:.4f}")
    print(f"distribution degrés  : {dict(sorted(dist.items()))}")
    print(f"cliques maximales    : {stats.num_cliques}")
    print(f"taille max clique    : {stats.max_size}")
    print(f"temps (s)            : {t:.6f}")
    print()


def main() -> None:
    parser = argparse.ArgumentParser(description="Pipeline graphes: stats + cliques maximales")
    parser.add_argument("--data", type=str, default="data", help="Dossier contenant les graphes .csv")
    args = parser.parse_args()

    data_dir = Path(args.data)
    if not data_dir.exists():
        raise SystemExit(f"Dossier introuvable: {data_dir}")

    files = sorted([p for p in data_dir.iterdir() if p.suffix.lower() == ".csv"])
    if not files:
        raise SystemExit(f"Aucun .csv trouvé dans {data_dir}")

    for f in files:
        run_on_file(f)


if __name__ == "__main__":
    main()
