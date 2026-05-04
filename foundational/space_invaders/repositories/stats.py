from __future__ import annotations

from space_invaders.repositories.sqlite import SQLiteDatabase


class StatsRepository:
    def __init__(self, db: SQLiteDatabase) -> None:
        self.db = db

    def increment(self, key: str, amount: int = 1) -> None:
        with self.db.connect() as conn:
            conn.execute(
                """
                INSERT INTO game_stats(key, value) VALUES (?, ?)
                ON CONFLICT(key) DO UPDATE SET value = value + excluded.value
                """,
                (key, amount),
            )

    def get(self, key: str, default: int = 0) -> int:
        with self.db.connect() as conn:
            row = conn.execute("SELECT value FROM game_stats WHERE key = ?", (key,)).fetchone()
            return int(row["value"]) if row else default
