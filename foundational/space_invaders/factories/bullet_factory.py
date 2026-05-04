from __future__ import annotations

import pygame

from space_invaders.core.constants import BULLET_SPEED, ENEMY_BULLET_SPEED
from space_invaders.models.entities import Bullet, Enemy, Player


class BulletFactory:
    def player_bullet(self, player: Player) -> Bullet:
        rect = pygame.Rect(player.rect.centerx - 2, player.rect.top - 12, 4, 12)
        return Bullet(rect=rect, velocity_y=-BULLET_SPEED, from_player=True)

    def enemy_bullet(self, enemy: Enemy) -> Bullet:
        rect = pygame.Rect(enemy.rect.centerx - 2, enemy.rect.bottom, 4, 12)
        return Bullet(rect=rect, velocity_y=ENEMY_BULLET_SPEED, from_player=False)
