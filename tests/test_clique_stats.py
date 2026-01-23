import unittest

from community_cliques.clique_stats import compute_clique_stats


class TestCliqueStats(unittest.TestCase):
    def test_stats(self):
        cliques = [{0, 1, 2}, {3, 4}, {9}, {5, 6, 7, 8}]
        stats = compute_clique_stats(cliques)
        self.assertEqual(stats.num_cliques, 4)
        self.assertEqual(stats.max_size, 4)


if __name__ == "__main__":
    unittest.main()
