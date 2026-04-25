from __future__ import annotations


class ScoreService:
    def __init__(self) -> None:
        self._score = 0

    @property
    def score(self) -> int:
        return self._score

    def reset(self) -> None:
        self._score = 0

    def add(self, points: int) -> int:
        self._score += max(0, points)
        return self._score
