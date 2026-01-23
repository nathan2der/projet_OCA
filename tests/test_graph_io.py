import os
import tempfile
import unittest

from community_cliques.graph_io import read_graph
from community_cliques.graph_stats import number_of_edges


class TestGraphIO(unittest.TestCase):
    def test_read_graph_csv(self):
        content = "0,1\n1,2\n2,0\n"
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "g.csv")
            with open(p, "w", encoding="utf-8") as f:
                f.write(content)
            g = read_graph(p, delimiter=",", cast_int=True)

        self.assertEqual(number_of_edges(g), 3)
        self.assertEqual(g[0], {1, 2})
        self.assertEqual(g[1], {0, 2})
        self.assertEqual(g[2], {0, 1})


if __name__ == "__main__":
    unittest.main()
