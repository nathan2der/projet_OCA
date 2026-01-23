import os
import tempfile
import unittest

from community_cliques.graph_io import read_graph
from community_cliques.graph_stats import degree, max_degree, average_degree, number_of_edges, degree_distribution


class TestGraphStats(unittest.TestCase):
    def test_metrics_triangle(self):
        content = "0,1\n1,2\n2,0\n"
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "tri.csv")
            with open(p, "w", encoding="utf-8") as f:
                f.write(content)
            g = read_graph(p, delimiter=",", cast_int=True)

        self.assertEqual(degree(g, 0), 2)
        self.assertEqual(max_degree(g), 2)
        self.assertEqual(number_of_edges(g), 3)
        self.assertAlmostEqual(average_degree(g), 2.0, places=9)
        self.assertEqual(degree_distribution(g), {2: 3})


if __name__ == "__main__":
    unittest.main()
