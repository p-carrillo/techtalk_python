from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class Settings:
    resolution: tuple[int, int] = (960, 640)
    fps: int = 60
    volume: float = 0.5
    difficulty: str = "normal"
    controls: dict[str, int] = field(
        default_factory=lambda: {
            "move_left": 1073741904,  # pygame.K_LEFT
            "move_right": 1073741903,  # pygame.K_RIGHT
            "shoot": 32,  # pygame.K_SPACE
            "pause": 112,  # pygame.K_p
            "confirm": 13,  # pygame.K_RETURN
            "back": 27,  # pygame.K_ESCAPE
        }
    )
    debug: bool = False
