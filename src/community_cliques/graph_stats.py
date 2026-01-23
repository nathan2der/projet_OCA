from __future__ import annotations

from typing import Dict, Set
from .graph_io import Graph, Node


def degree(graph: Graph, v: Node) -> int:
    return len(graph.get(v, set()))


def number_of_edges(graph: Graph) -> int:
    # Non orienté: somme des degrés / 2
    return sum(len(neigh) for neigh in graph.values()) // 2


def max_degree(graph: Graph) -> int:
    if not graph:
        return 0
    return max(len(neigh) for neigh in graph.values())


def average_degree(graph: Graph) -> float:
    n = len(graph)
    if n == 0:
        return 0.0
    m = number_of_edges(graph)
    return (2.0 * m) / n


def degree_distribution(graph: Graph) -> Dict[int, int]:
    dist: Dict[int, int] = {}
    for neigh in graph.values():
        d = len(neigh)
        dist[d] = dist.get(d, 0) + 1
    return dist
