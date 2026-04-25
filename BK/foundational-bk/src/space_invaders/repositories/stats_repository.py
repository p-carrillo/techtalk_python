from __future__ import annotations

from .database import Database


class StatsRepository:
    def __init__(self, database: Database) -> None:
        self._database = database

    def ensure_row(self) -> None:
        with self._database.connection() as conn:
            conn.execute(
                """
                INSERT INTO player_stats(games_played, enemies_destroyed, shots_fired, shots_hit)
                SELECT 0, 0, 0, 0
                WHERE NOT EXISTS (SELECT 1 FROM player_stats)
                """
            )

    def increment(self, *, games_played: int = 0, enemies_destroyed: int = 0, shots_fired: int = 0, shots_hit: int = 0) -> None:
        self.ensure_row()
        with self._database.connection() as conn:
            conn.execute(
                """
                UPDATE player_stats
                SET games_played = games_played + ?,
                    enemies_destroyed = enemies_destroyed + ?,
                    shots_fired = shots_fired + ?,
                    shots_hit = shots_hit + ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = (SELECT id FROM player_stats ORDER BY id LIMIT 1)
                """,
                (games_played, enemies_destroyed, shots_fired, shots_hit),
            )

    def read(self) -> dict[str, int]:
        self.ensure_row()
        with self._database.connection() as conn:
            row = conn.execute(
                "SELECT games_played, enemies_destroyed, shots_fired, shots_hit FROM player_stats ORDER BY id LIMIT 1"
            ).fetchone()
        assert row is not None
        return {
            "games_played": int(row["games_played"]),
            "enemies_destroyed": int(row["enemies_destroyed"]),
            "shots_fired": int(row["shots_fired"]),
            "shots_hit": int(row["shots_hit"]),
        }
