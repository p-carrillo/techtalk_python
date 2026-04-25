from __future__ import annotations

from dataclasses import dataclass

from .database import Database


@dataclass(slots=True)
class HighScore:
    player_name: str
    score: int
    wave: int


class HighScoreRepository:
    def __init__(self, database: Database) -> None:
        self._database = database

    def add(self, entry: HighScore) -> None:
        with self._database.connection() as conn:
            conn.execute(
                "INSERT INTO high_scores(player_name, score, wave) VALUES (?, ?, ?)",
                (entry.player_name, entry.score, entry.wave),
            )

    def top(self, limit: int = 10) -> list[HighScore]:
        with self._database.connection() as conn:
            rows = conn.execute(
                "SELECT player_name, score, wave FROM high_scores ORDER BY score DESC LIMIT ?",
                (limit,),
            ).fetchall()
        return [HighScore(player_name=r["player_name"], score=r["score"], wave=r["wave"]) for r in rows]
