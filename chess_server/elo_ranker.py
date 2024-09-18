from typing import Dict, List

from chess_server.outcome import Outcome, opposite_outcome, outcome_to_score
from chess_server.player import Player


class EloRanker(object):
    MAX_ELO_DIFF: int = 32

    __players: Dict[str, Player]

    def __init__(self) -> None:
        self.__players = {}

    @property
    def players(self) -> List[Player]:
        return list(self.__players.values())

    def add_player(self, name: str) -> None:
        self.__players[name] = Player(name)

    def get_player(self, name: str) -> Player:
        if name not in self.__players:
            self.add_player(name)
        return self.__players[name]

    def update(self, white_name: str, black_name: str, outcome_value: str) -> None:
        if white_name == black_name:
            raise ValueError("White and black player names must be different")
        outcome = Outcome(outcome_value)
        white = self.get_player(white_name)
        black = self.get_player(black_name)
        elo_diff = self.compute_elo_diff(white.elo, black.elo, outcome)
        white.update(elo_diff, outcome)
        black.update(-elo_diff, opposite_outcome(outcome))

    @staticmethod
    def compute_expected_score(white_elo: int, black_elo: int) -> float:
        """Compute the expected score (win probability) for white"""
        return 1 / (1 + 10 ** ((black_elo - white_elo) / 400))

    @classmethod
    def compute_elo_diff(cls, white_elo: int, black_elo: int, actual_outcome: Outcome) -> int:
        """Compute the ELO difference for white player

        Args:
            white_elo (int): initial ELO rating of the white player
            black_elo (int): inital ELO rating of the black player
            actual_outcome (Outcome): outcome of the game

        Returns:
            elo_diff (int): how to update white ELO rating after that game
        """
        expected_score = cls.compute_expected_score(white_elo, black_elo)
        actual_score = outcome_to_score(actual_outcome)
        elo_diff = round(cls.MAX_ELO_DIFF * (actual_score - expected_score))
        return elo_diff
