from __future__ import annotations

from enum import Enum


class SceneName(str, Enum):
    MAIN_MENU = "main_menu"
    GAME = "game"
    PAUSE = "pause"
    GAME_OVER = "game_over"
    HIGH_SCORES = "high_scores"
    SETTINGS = "settings"


class GameSceneState(str, Enum):
    READY = "READY"
    PLAYING = "PLAYING"
    PLAYER_DIED = "PLAYER_DIED"
    LEVEL_CLEARED = "LEVEL_CLEARED"
    GAME_OVER = "GAME_OVER"


EVENT_ENEMY_DESTROYED = "enemy_destroyed"
EVENT_PLAYER_HIT = "player_hit"
EVENT_SCORE_CHANGED = "score_changed"
EVENT_LEVEL_COMPLETED = "level_completed"
EVENT_GAME_OVER = "game_over"

ACTIONS = (
    "move_left",
    "move_right",
    "shoot",
    "pause",
    "confirm",
    "back",
)
