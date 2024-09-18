import unittest

from chess_server.elo_ranker import EloRanker
from chess_server.outcome import Outcome


class TestEloRanker(unittest.TestCase):
    def test_compute_expected_score(self):
        # Even players
        self.assertAlmostEqual(EloRanker.compute_expected_score(1000, 1000), 0.5)
        # Slightly higher rated white player
        self.assertGreater(EloRanker.compute_expected_score(1100, 1000), 0.5)
        # Slighly higher rated black player
        self.assertLess(EloRanker.compute_expected_score(900, 1000), 0.5)
        # Much higher rated white player
        self.assertAlmostEqual(EloRanker.compute_expected_score(2000, 100), 1.0, delta=0.01)
        # Much higher rated black player
        self.assertAlmostEqual(EloRanker.compute_expected_score(100, 2000), 0.0, delta=0.01)

    def test_compute_elo_diff(self):
        # Even players
        self.assertEqual(
            EloRanker.compute_elo_diff(1000, 1000, Outcome.WIN), 0.5 * EloRanker.MAX_ELO_DIFF
        )
        self.assertEqual(
            EloRanker.compute_elo_diff(1000, 1000, Outcome.LOSS), -0.5 * EloRanker.MAX_ELO_DIFF
        )
        self.assertEqual(EloRanker.compute_elo_diff(1000, 1000, Outcome.DRAW), 0)
        # Slightly higher rated white player
        self.assertLess(
            EloRanker.compute_elo_diff(1100, 1000, Outcome.WIN), 0.5 * EloRanker.MAX_ELO_DIFF
        )
        self.assertLess(
            EloRanker.compute_elo_diff(1100, 1000, Outcome.LOSS), -0.5 * EloRanker.MAX_ELO_DIFF
        )
        # Slightly higher rated black player
        self.assertGreater(
            EloRanker.compute_elo_diff(900, 1000, Outcome.WIN), 0.5 * EloRanker.MAX_ELO_DIFF
        )
        self.assertGreater(
            EloRanker.compute_elo_diff(900, 1000, Outcome.LOSS), -0.5 * EloRanker.MAX_ELO_DIFF
        )
        # Much higher rated white player
        self.assertAlmostEqual(EloRanker.compute_elo_diff(2000, 100, Outcome.WIN), 0)
        self.assertAlmostEqual(
            EloRanker.compute_elo_diff(2000, 100, Outcome.LOSS), -EloRanker.MAX_ELO_DIFF
        )
        # Much higher rated black player
        self.assertAlmostEqual(
            EloRanker.compute_elo_diff(100, 2000, Outcome.WIN), EloRanker.MAX_ELO_DIFF
        )
        self.assertAlmostEqual(EloRanker.compute_elo_diff(100, 2000, Outcome.LOSS), 0)

    def test_get_player(self):
        elo_ranker = EloRanker()
        self.assertEqual(len(elo_ranker.players), 0)
        player = elo_ranker.get_player("Alice")
        self.assertEqual(len(elo_ranker.players), 1)
        self.assertEqual(player.name, "Alice")
        player2 = elo_ranker.get_player("Alice")
        self.assertEqual(len(elo_ranker.players), 1)
        self.assertEqual(player, player2)

    def test_update(self):
        elo_ranker = EloRanker()
        alice = elo_ranker.get_player("Alice")
        bob = elo_ranker.get_player("Bob")
        self.assertEqual(alice.elo, 1000)
        self.assertEqual(bob.elo, 1000)
        elo_ranker.update("Alice", "Bob", "Draw")
        self.assertEqual(alice.elo, 1000)
        self.assertEqual(bob.elo, 1000)
        elo_ranker.update("Alice", "Bob", "Win")
        self.assertGreater(alice.elo, 1000)
        self.assertLess(bob.elo, 1000)
        self.assertEqual(alice.elo + bob.elo, 2000)
        elo_ranker.update("Alice", "Bob", "Loss")
        self.assertAlmostEqual(alice.elo, 1000, delta=1)
        self.assertAlmostEqual(bob.elo, 1000, delta=1)
        self.assertEqual(alice.elo + bob.elo, 2000)

    def test_invalid_update(self):
        elo_ranker = EloRanker()
        with self.assertRaises(ValueError):
            elo_ranker.update("Alice", "Alice", "Win")
        with self.assertRaises(ValueError):
            elo_ranker.update("Alice", "Bob", "invalid_outcome")
