from __future__ import annotations

from dataclasses import dataclass

from space_invaders.repositories.sqlite import SQLiteDatabase


@dataclass(slots=True)
class HighScore:
    player_name: str
    score: int


class HighScoreRepository:
    def __init__(self, db: SQLiteDatabase) -> None:
        self.db = db

    def add(self, player_name: str, score: int) -> None:
        with self.db.connect() as conn:
            conn.execute(
                "INSERT INTO high_scores(player_name, score) VALUES (?, ?)",
                (player_name, score),
            )

    def top(self, limit: int = 10) -> list[HighScore]:
        with self.db.connect() as conn:
            rows = conn.execute(
                "SELECT player_name, score FROM high_scores ORDER BY score DESC, id ASC LIMIT ?",
                (limit,),
            ).fetchall()
        return [HighScore(player_name=row["player_name"], score=row["score"]) for row in rows]
