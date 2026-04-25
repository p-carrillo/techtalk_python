from __future__ import annotations

from dataclasses import dataclass

from .database import Database


@dataclass(slots=True)
class Progress:
    level: int
    wave: int
    lives: int
    score: int


class ProgressRepository:
    def __init__(self, database: Database) -> None:
        self._database = database

    def save(self, progress: Progress) -> None:
        with self._database.connection() as conn:
            conn.execute(
                "INSERT INTO progress(level, wave, lives, score) VALUES (?, ?, ?, ?)",
                (progress.level, progress.wave, progress.lives, progress.score),
            )

    def latest(self) -> Progress | None:
        with self._database.connection() as conn:
            row = conn.execute(
                "SELECT level, wave, lives, score FROM progress ORDER BY id DESC LIMIT 1"
            ).fetchone()
        if row is None:
            return None
        return Progress(level=int(row["level"]), wave=int(row["wave"]), lives=int(row["lives"]), score=int(row["score"]))
