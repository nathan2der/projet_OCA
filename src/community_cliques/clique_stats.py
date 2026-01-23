from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, FrozenSet, Optional
from .graph_io import Node

Clique = FrozenSet[Node]


@dataclass
class CliqueStats:
    store: bool = False
    num_cliques: int = 0
    max_size: int = 0
    cliques: Optional[list[Clique]] = None

    def __post_init__(self) -> None:
        if self.store:
            self.cliques = []

    def update(self, clique: Iterable[Node]) -> None:
        c = frozenset(clique)
        self.num_cliques += 1
        sz = len(c)
        if sz > self.max_size:
            self.max_size = sz
        if self.store and self.cliques is not None:
            self.cliques.append(c)


def compute_clique_stats(cliques: Iterable[Iterable[Node]], *, store: bool = False) -> CliqueStats:
    stats = CliqueStats(store=store)
    for c in cliques:
        stats.update(c)
    return stats
