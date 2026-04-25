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

ASSET_CATALOG: dict[str, str] = {
    "player_ship": "sprites/player_ship.png",
    "enemy_basic": "sprites/enemy_basic.png",
    "bullet_player": "sprites/bullet_player.png",
    "bullet_enemy": "sprites/bullet_player.png",
    "shield_block": "effects/shield_block.png",
    "explosion_01": "effects/explosion_01.png",
    "explosion_02": "effects/explosion_02.png",
    "powerup_token": "sprites/powerup_token.png",
    "bg_nebula_blue": "backgrounds/bg_nebula_blue.png",
    "bg_nebula_rainbow": "backgrounds/bg_nebula_rainbow.png",
    "bg_stars_seamless": "backgrounds/bg_stars_seamless.png",
}

BACKGROUND_ASSET_IDS = (
    "bg_nebula_blue",
    "bg_nebula_rainbow",
    "bg_stars_seamless",
)

DEFAULT_BACKGROUND_ID = "bg_nebula_blue"
