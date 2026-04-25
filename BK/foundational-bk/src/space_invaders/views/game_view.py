from __future__ import annotations

from typing import Iterable

from space_invaders.models import Bullet, Enemy, Explosion, Player, PowerUp, Shield


class GameView:
    def render(
        self,
        surface: object,
        player: Player,
        enemies: Iterable[Enemy],
        player_bullets: Iterable[Bullet],
        enemy_bullets: Iterable[Bullet],
        shields: Iterable[Shield],
        explosions: Iterable[Explosion],
        powerups: Iterable[PowerUp],
    ) -> None:
        import pygame

        surface.fill((6, 7, 20))

        pygame.draw.rect(surface, (80, 200, 255), pygame.Rect(player.x, player.y, player.width, player.height))

        for enemy in enemies:
            if enemy.alive:
                pygame.draw.rect(surface, (250, 80, 110), pygame.Rect(enemy.x, enemy.y, enemy.width, enemy.height))

        for shield in shields:
            if shield.alive:
                color = (80, 220, 130) if shield.health > 1 else (180, 180, 80)
                pygame.draw.rect(surface, color, pygame.Rect(shield.x, shield.y, shield.width, shield.height))

        for bullet in player_bullets:
            if bullet.alive:
                pygame.draw.rect(surface, (255, 255, 180), pygame.Rect(bullet.x, bullet.y, bullet.width, bullet.height))

        for bullet in enemy_bullets:
            if bullet.alive:
                pygame.draw.rect(surface, (255, 120, 120), pygame.Rect(bullet.x, bullet.y, bullet.width, bullet.height))

        for power in powerups:
            if power.alive:
                pygame.draw.rect(surface, (120, 255, 220), pygame.Rect(power.x, power.y, power.width, power.height))

        for explosion in explosions:
            if explosion.alive:
                pygame.draw.rect(
                    surface,
                    (255, 180, 80),
                    pygame.Rect(explosion.x, explosion.y, explosion.width, explosion.height),
                )
