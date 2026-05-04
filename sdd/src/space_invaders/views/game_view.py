from __future__ import annotations

from typing import Iterable

from space_invaders.models import Bullet, Enemy, Explosion, Player, PowerUp, Shield


class GameView:
    def render(
        self,
        surface: object,
        asset_manager: object,
        player: Player,
        enemies: Iterable[Enemy],
        player_bullets: Iterable[Bullet],
        enemy_bullets: Iterable[Bullet],
        shields: Iterable[Shield],
        explosions: Iterable[Explosion],
        powerups: Iterable[PowerUp],
    ) -> None:
        import pygame

        width = surface.get_width()
        height = surface.get_height()
        background = asset_manager.try_get_image("background.main", size=(width, height))
        if background is None:
            surface.fill((6, 7, 20))
        else:
            surface.blit(background, (0, 0))

        player_sprite = asset_manager.try_get_image("sprite.player", size=(player.width, player.height))
        if player_sprite is None:
            pygame.draw.rect(surface, (80, 200, 255), pygame.Rect(player.x, player.y, player.width, player.height))
        else:
            surface.blit(player_sprite, (player.x, player.y))

        enemy_sprite_cache: dict[tuple[int, int], object | None] = {}
        shield_sprite_cache: dict[tuple[int, int], object | None] = {}
        bullet_sprite_cache: dict[tuple[int, int], object | None] = {}
        powerup_sprite_cache: dict[tuple[int, int], object | None] = {}
        explosion_sprite_cache: dict[tuple[str, int, int], object | None] = {}

        for enemy in enemies:
            if enemy.alive:
                enemy_size = (enemy.width, enemy.height)
                if enemy_size not in enemy_sprite_cache:
                    enemy_sprite_cache[enemy_size] = asset_manager.try_get_image(
                        "sprite.enemy.basic",
                        size=enemy_size,
                    )
                enemy_sprite = enemy_sprite_cache[enemy_size]
                if enemy_sprite is None:
                    pygame.draw.rect(surface, (250, 80, 110), pygame.Rect(enemy.x, enemy.y, enemy.width, enemy.height))
                else:
                    surface.blit(enemy_sprite, (enemy.x, enemy.y))

        for shield in shields:
            if shield.alive:
                shield_size = (shield.width, shield.height)
                if shield_size not in shield_sprite_cache:
                    shield_sprite_cache[shield_size] = asset_manager.try_get_image(
                        "sprite.shield.block",
                        size=shield_size,
                    )
                shield_sprite = shield_sprite_cache[shield_size]
                if shield_sprite is None:
                    color = (80, 220, 130) if shield.health > 1 else (180, 180, 80)
                    pygame.draw.rect(surface, color, pygame.Rect(shield.x, shield.y, shield.width, shield.height))
                else:
                    surface.blit(shield_sprite, (shield.x, shield.y))

        for bullet in player_bullets:
            if bullet.alive:
                bullet_size = (bullet.width, bullet.height)
                if bullet_size not in bullet_sprite_cache:
                    bullet_sprite_cache[bullet_size] = asset_manager.try_get_image(
                        "sprite.bullet.player",
                        size=bullet_size,
                    )
                bullet_sprite = bullet_sprite_cache[bullet_size]
                if bullet_sprite is None:
                    pygame.draw.rect(
                        surface,
                        (255, 255, 180),
                        pygame.Rect(bullet.x, bullet.y, bullet.width, bullet.height),
                    )
                else:
                    surface.blit(bullet_sprite, (bullet.x, bullet.y))

        for bullet in enemy_bullets:
            if bullet.alive:
                pygame.draw.rect(surface, (255, 120, 120), pygame.Rect(bullet.x, bullet.y, bullet.width, bullet.height))

        for power in powerups:
            if power.alive:
                power_size = (power.width, power.height)
                if power_size not in powerup_sprite_cache:
                    powerup_sprite_cache[power_size] = asset_manager.try_get_image(
                        "sprite.powerup.token",
                        size=power_size,
                    )
                powerup_sprite = powerup_sprite_cache[power_size]
                if powerup_sprite is None:
                    pygame.draw.rect(surface, (120, 255, 220), pygame.Rect(power.x, power.y, power.width, power.height))
                else:
                    surface.blit(powerup_sprite, (power.x, power.y))

        for explosion in explosions:
            if explosion.alive:
                frame_key = "effect.explosion.01" if explosion.ttl > 0.15 else "effect.explosion.02"
                cache_key = (frame_key, explosion.width, explosion.height)
                if cache_key not in explosion_sprite_cache:
                    explosion_sprite_cache[cache_key] = asset_manager.try_get_image(
                        frame_key,
                        size=(explosion.width, explosion.height),
                    )
                explosion_sprite = explosion_sprite_cache[cache_key]
                if explosion_sprite is None:
                    pygame.draw.rect(
                        surface,
                        (255, 180, 80),
                        pygame.Rect(explosion.x, explosion.y, explosion.width, explosion.height),
                    )
                else:
                    surface.blit(explosion_sprite, (explosion.x, explosion.y))
