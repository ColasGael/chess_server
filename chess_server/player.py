from chess_server.outcome import Outcome


class Player(object):
    INITIAL_ELO: int = 1000

    __name: str
    __elo: int
    __num_wins: int
    __num_draws: int
    __num_losses: int

    def __init__(self, name: str) -> None:
        self.__name = name
        self.__elo = self.INITIAL_ELO
        self.__num_wins = 0
        self.__num_draws = 0
        self.__num_losses = 0

    @property
    def name(self) -> str:
        return self.__name

    @property
    def elo(self) -> int:
        return self.__elo

    @property
    def wins(self) -> int:
        return self.__num_wins

    @property
    def draws(self) -> int:
        return self.__num_draws

    @property
    def losses(self) -> int:
        return self.__num_losses

    def __update_elo(self, elo_diff: int) -> None:
        self.__elo += elo_diff

    def __record_outcome(self, outcome: Outcome) -> None:
        if outcome == Outcome.WIN:
            self.__num_wins += 1
        elif outcome == Outcome.DRAW:
            self.__num_draws += 1
        elif outcome == Outcome.LOSS:
            self.__num_losses += 1
        else:
            raise RuntimeError(f"Unsupported outcome: {outcome}")

    def update(self, elo_diff: int, outcome: Outcome) -> None:
        self.__update_elo(elo_diff)
        self.__record_outcome(outcome)
