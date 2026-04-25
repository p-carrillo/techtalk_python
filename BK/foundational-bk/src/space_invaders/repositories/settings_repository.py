from __future__ import annotations

from .database import Database


class SettingsRepository:
    def __init__(self, database: Database) -> None:
        self._database = database

    def save(self, key: str, value: str) -> None:
        with self._database.connection() as conn:
            conn.execute(
                """
                INSERT INTO settings(key, value, updated_at)
                VALUES (?, ?, CURRENT_TIMESTAMP)
                ON CONFLICT(key) DO UPDATE SET value=excluded.value, updated_at=CURRENT_TIMESTAMP
                """,
                (key, value),
            )

    def get(self, key: str) -> str | None:
        with self._database.connection() as conn:
            row = conn.execute("SELECT value FROM settings WHERE key = ?", (key,)).fetchone()
        if row is None:
            return None
        return str(row["value"])

    def all(self) -> dict[str, str]:
        with self._database.connection() as conn:
            rows = conn.execute("SELECT key, value FROM settings").fetchall()
        return {str(r["key"]): str(r["value"]) for r in rows}
