from __future__ import annotations

from dataclasses import dataclass

import pygame


@dataclass(slots=True)
class Player:
    rect: pygame.Rect
    speed: float
    lives: int
    cooldown: float
    cooldown_timer: float = 0.0


@dataclass(slots=True)
class Enemy:
    rect: pygame.Rect
    alive: bool = True


@dataclass(slots=True)
class Bullet:
    rect: pygame.Rect
    velocity_y: float
    from_player: bool
    alive: bool = True


@dataclass(slots=True)
class Shield:
    rect: pygame.Rect
    health: int


@dataclass(slots=True)
class Explosion:
    pos: tuple[int, int]
    ttl: float = 0.2


@dataclass(slots=True)
class PowerUp:
    rect: pygame.Rect
    kind: str
    active: bool = True
