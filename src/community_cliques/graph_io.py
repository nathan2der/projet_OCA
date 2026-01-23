from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, Set, Hashable, Optional, Iterable

Node = int
Graph = Dict[Node, Set[Node]]

_COMMENT_PREFIXES = ("#", "%", "//")


def _is_comment_or_empty(line: str) -> bool:
    s = line.strip()
    if not s:
        return True
    s2 = s.lstrip()
    return any(s2.startswith(p) for p in _COMMENT_PREFIXES)


def _detect_delimiter(sample_line: str) -> Optional[str]:
    """Auto-détection simple : virgule, point-virgule, sinon whitespace."""
    if "," in sample_line:
        return ","
    if ";" in sample_line:
        return ";"
    return None  # whitespace


def read_graph(path: str, *, delimiter: Optional[str] = None, cast_int: bool = True) -> Graph:
    """
    Lit un graphe NON ORIENTÉ depuis un fichier d'arêtes (edge list).

    Formats acceptés :
      - CSV: `u,v` (ou `u;v`)
      - whitespace: `u v`

    Règles :
      - lignes vides / commentaires ignorés (#, %, //)
      - pas de doublons (voisins stockés dans un set)
      - pas de boucles (u == v ignoré)
      - non orienté : on ajoute u<->v
    """
    g: Graph = defaultdict(set)

    with open(path, "r", encoding="utf-8") as f:
        first_data_line: Optional[str] = None
        # trouver une ligne de données pour auto-détecter
        for raw in f:
            if _is_comment_or_empty(raw):
                continue
            first_data_line = raw.strip()
            break

        if first_data_line is None:
            return {}

        delim = delimiter if delimiter is not None else _detect_delimiter(first_data_line)

        def parse_line(line: str) -> Optional[tuple[Node, Node]]:
            if _is_comment_or_empty(line):
                return None
            s = line.strip()
            parts = s.split(delim) if delim else s.split()
            if len(parts) < 2:
                return None
            a, b = parts[0].strip(), parts[1].strip()
            if cast_int:
                try:
                    u = int(a)
                    v = int(b)
                except ValueError:
                    return None
            else:
                # type ignore: si cast_int=False, Node devrait être Hashable
                u = a  # type: ignore
                v = b  # type: ignore
            if u == v:
                return None
            return u, v

        # traiter la première ligne puis le reste
        parsed = parse_line(first_data_line)
        if parsed:
            u, v = parsed
            g[u].add(v)
            g[v].add(u)

        for raw in f:
            parsed = parse_line(raw)
            if not parsed:
                continue
            u, v = parsed
            g[u].add(v)
            g[v].add(u)

    return {u: set(neigh) for u, neigh in g.items()}
