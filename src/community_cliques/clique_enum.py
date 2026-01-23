from __future__ import annotations

from typing import Dict, Set, Iterable, FrozenSet, Iterator, Optional
from .graph_io import Graph, Node

Clique = FrozenSet[Node]


def enumerate_maximal_cliques(graph: Graph) -> Iterator[Clique]:
    """
    Baseline (pour tests) : Bron–Kerbosch avec pivot sur le graphe non orienté.
    Votre version optimisée (dégénérescence + orientation) peut remplacer cette fonction.
    """
    # Bron–Kerbosch (pivot)
    R: Set[Node] = set()
    P: Set[Node] = set(graph.keys())
    X: Set[Node] = set()
    yield from _bron_kerbosch_pivot(R, P, X, graph)


def _bron_kerbosch_pivot(R: Set[Node], P: Set[Node], X: Set[Node], graph: Graph) -> Iterator[Clique]:
    if not P and not X:
        yield frozenset(R)
        return

    # pivot u dans P ∪ X qui maximise |P ∩ N(u)|
    u: Optional[Node] = None
    best = -1
    for cand in (P | X):
        inter = len(P & graph.get(cand, set()))
        if inter > best:
            best = inter
            u = cand

    Nu = graph.get(u, set()) if u is not None else set()

    # On explore les sommets v dans P \ N(u)
    for v in list(P - Nu):
        Nv = graph.get(v, set())
        yield from _bron_kerbosch_pivot(R | {v}, P & Nv, X & Nv, graph)
        P.remove(v)
        X.add(v)
