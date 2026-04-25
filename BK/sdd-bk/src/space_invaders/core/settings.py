from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List

from space_invaders.core.constants import DEFAULT_BACKGROUND_ID


@dataclass(slots=True)
class GameSettings:
    resolution_width: int = 960
    resolution_height: int = 720
    logical_width: int = 480
    logical_height: int = 360
    target_fps: int = 60
    master_volume: float = 0.5
    difficulty: str = "normal"
    debug_mode: bool = False
    background_id: str = DEFAULT_BACKGROUND_ID
    controls: Dict[str, List[int]] = field(default_factory=dict)


DEFAULT_CONTROL_NAMES = {
    "move_left": "K_LEFT",
    "move_right": "K_RIGHT",
    "shoot": "K_SPACE",
    "pause": "K_ESCAPE",
    "confirm": "K_RETURN",
    "back": "K_BACKSPACE",
}


class SettingsService:
    def __init__(self, settings: GameSettings | None = None) -> None:
        self._settings = settings or GameSettings()

    @property
    def value(self) -> GameSettings:
        return self._settings

    def update_volume(self, volume: float) -> None:
        self._settings.master_volume = max(0.0, min(1.0, volume))

    def toggle_debug(self) -> None:
        self._settings.debug_mode = not self._settings.debug_mode

    def set_background(self, background_id: str) -> None:
        self._settings.background_id = background_id
