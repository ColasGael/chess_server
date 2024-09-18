import unittest

from chess_server.outcome import Outcome
from chess_server.player import Player


class TestPlayer(unittest.TestCase):
    def test_update(self):
        player = Player("Alice")
        # 0. Initial state
        self.assertEqual(player.elo, Player.INITIAL_ELO)
        self.assertEqual(player.wins, 0)
        self.assertEqual(player.draws, 0)
        self.assertEqual(player.losses, 0)
        # 1. Update with a win
        player.update(2, Outcome.WIN)
        self.assertEqual(player.elo, Player.INITIAL_ELO + 2)
        self.assertEqual(player.wins, 1)
        self.assertEqual(player.draws, 0)
        self.assertEqual(player.losses, 0)
        # 2. Update with a draw
        player.update(1, Outcome.DRAW)
        self.assertEqual(player.elo, Player.INITIAL_ELO + 3)
        self.assertEqual(player.wins, 1)
        self.assertEqual(player.draws, 1)
        self.assertEqual(player.losses, 0)
        # 3. Update with a loss
        player.update(-3, Outcome.LOSS)
        self.assertEqual(player.elo, Player.INITIAL_ELO)
        self.assertEqual(player.wins, 1)
        self.assertEqual(player.draws, 1)
        self.assertEqual(player.losses, 1)
