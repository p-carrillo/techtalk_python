from pathlib import Path

from space_invaders.repositories import (
    Database,
    HighScore,
    HighScoreRepository,
    Progress,
    ProgressRepository,
    SettingsRepository,
    StatsRepository,
)


def test_sqlite_repositories_roundtrip(tmp_path: Path) -> None:
    db = Database(tmp_path / "game.db")
    db.migrate()

    high_scores = HighScoreRepository(db)
    settings = SettingsRepository(db)
    stats = StatsRepository(db)
    progress = ProgressRepository(db)

    high_scores.add(HighScore(player_name="AAA", score=1200, wave=3))
    top = high_scores.top(limit=1)
    assert len(top) == 1
    assert top[0].score == 1200

    settings.save("master_volume", "0.7")
    assert settings.get("master_volume") == "0.7"

    stats.increment(games_played=1, enemies_destroyed=2, shots_fired=5, shots_hit=3)
    stats_data = stats.read()
    assert stats_data["games_played"] == 1
    assert stats_data["enemies_destroyed"] == 2

    progress.save(Progress(level=1, wave=2, lives=2, score=450))
    latest = progress.latest()
    assert latest is not None
    assert latest.wave == 2
