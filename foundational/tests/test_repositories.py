from pathlib import Path

from space_invaders.repositories.high_scores import HighScoreRepository
from space_invaders.repositories.settings_repo import SettingsRepository
from space_invaders.repositories.sqlite import SQLiteDatabase
from space_invaders.repositories.stats import StatsRepository


def test_high_scores_insert_and_read(tmp_path: Path) -> None:
    db = SQLiteDatabase(tmp_path / "test.db")
    repo = HighScoreRepository(db)

    repo.add("AAA", 1234)
    repo.add("BBB", 2000)

    top = repo.top(2)

    assert top[0].player_name == "BBB"
    assert top[0].score == 2000


def test_settings_upsert(tmp_path: Path) -> None:
    db = SQLiteDatabase(tmp_path / "test.db")
    repo = SettingsRepository(db)

    assert repo.get("difficulty", "normal") == "normal"
    repo.set("difficulty", "hard")
    assert repo.get("difficulty", "normal") == "hard"


def test_stats_increment(tmp_path: Path) -> None:
    db = SQLiteDatabase(tmp_path / "test.db")
    repo = StatsRepository(db)

    repo.increment("games_played")
    repo.increment("games_played", 2)

    assert repo.get("games_played") == 3
