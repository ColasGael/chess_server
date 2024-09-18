from enum import Enum


class Outcome(Enum):
    WIN = "Win"
    DRAW = "Draw"
    LOSS = "Loss"


def opposite_outcome(outcome: Outcome) -> Outcome:
    if outcome == Outcome.WIN:
        return Outcome.LOSS
    elif outcome == Outcome.DRAW:
        return Outcome.DRAW
    elif outcome == Outcome.LOSS:
        return Outcome.WIN
    else:
        raise RuntimeError(f"Unsupported outcome: {outcome}")


def outcome_to_score(outcome: Outcome) -> float:
    score = -1.0
    if outcome == Outcome.WIN:
        score = 1.0
    elif outcome == Outcome.DRAW:
        score = 0.5
    elif outcome == Outcome.LOSS:
        score = 0.0
    else:
        raise RuntimeError(f"Unsupported outcome: {outcome}")
    return score
