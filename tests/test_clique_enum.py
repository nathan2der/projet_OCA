import os
import tempfile
import unittest

from community_cliques.graph_io import read_graph
from community_cliques.clique_enum import enumerate_maximal_cliques


class TestCliqueEnum(unittest.TestCase):
    def test_triangle_has_one_maximal_clique(self):
        content = "0,1\n1,2\n2,0\n"
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "tri.csv")
            with open(p, "w", encoding="utf-8") as f:
                f.write(content)
            g = read_graph(p, delimiter=",", cast_int=True)

        cliques = list(enumerate_maximal_cliques(g))
        self.assertEqual(len(cliques), 1)
        self.assertEqual(set(next(iter(cliques))), {0,1,2})


if __name__ == "__main__":
    unittest.main()
