from __future__ import annotations

from space_invaders.repositories.sqlite import SQLiteDatabase


class SettingsRepository:
    def __init__(self, db: SQLiteDatabase) -> None:
        self.db = db

    def get(self, key: str, default: str) -> str:
        with self.db.connect() as conn:
            row = conn.execute("SELECT value FROM settings WHERE key = ?", (key,)).fetchone()
            return row["value"] if row else default

    def set(self, key: str, value: str) -> None:
        with self.db.connect() as conn:
            conn.execute(
                """
                INSERT INTO settings(key, value) VALUES (?, ?)
                ON CONFLICT(key) DO UPDATE SET value = excluded.value
                """,
                (key, value),
            )
