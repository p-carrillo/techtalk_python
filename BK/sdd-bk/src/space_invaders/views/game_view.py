from __future__ import annotations

from typing import Iterable

from space_invaders.models import Bullet, Enemy, Explosion, Player, PowerUp, Shield


class GameView:
    PLAYER_SCALE = 1.55
    ENEMY_SCALE = 1.45
    SHIELD_SCALE = 1.35
    BULLET_SCALE = 1.8
    POWERUP_SCALE = 1.5
    EXPLOSION_SCALE = 1.7

    @staticmethod
    def _scaled_size(width: float, height: float, scale: float) -> tuple[int, int]:
        return (max(1, int(width * scale)), max(1, int(height * scale)))

    @staticmethod
    def _blit_centered(surface: object, sprite: object, x: float, y: float, width: float, height: float) -> None:
        draw_x = int(x - (sprite.get_width() - width) / 2)
        draw_y = int(y - (sprite.get_height() - height) / 2)
        surface.blit(sprite, (draw_x, draw_y))

    def render(
        self,
        surface: object,
        asset_manager: object,
        background_id: str,
        player: Player,
        enemies: Iterable[Enemy],
        player_bullets: Iterable[Bullet],
        enemy_bullets: Iterable[Bullet],
        shields: Iterable[Shield],
        explosions: Iterable[Explosion],
        powerups: Iterable[PowerUp],
    ) -> None:
        bg = asset_manager.get_background_image(background_id, (surface.get_width(), surface.get_height()))
        surface.blit(bg, (0, 0))

        player_sprite = asset_manager.load_image(
            "player_ship",
            self._scaled_size(player.width, player.height, self.PLAYER_SCALE),
        )
        self._blit_centered(surface, player_sprite, player.x, player.y, player.width, player.height)

        for enemy in enemies:
            if enemy.alive:
                sprite = asset_manager.load_image(
                    "enemy_basic",
                    self._scaled_size(enemy.width, enemy.height, self.ENEMY_SCALE),
                )
                self._blit_centered(surface, sprite, enemy.x, enemy.y, enemy.width, enemy.height)

        for shield in shields:
            if shield.alive:
                sprite = asset_manager.load_image(
                    "shield_block",
                    self._scaled_size(shield.width, shield.height, self.SHIELD_SCALE),
                )
                self._blit_centered(surface, sprite, shield.x, shield.y, shield.width, shield.height)

        for bullet in player_bullets:
            if bullet.alive:
                sprite = asset_manager.load_image(
                    "bullet_player",
                    self._scaled_size(bullet.width, bullet.height, self.BULLET_SCALE),
                )
                self._blit_centered(surface, sprite, bullet.x, bullet.y, bullet.width, bullet.height)

        for bullet in enemy_bullets:
            if bullet.alive:
                sprite = asset_manager.load_image(
                    "bullet_enemy",
                    self._scaled_size(bullet.width, bullet.height, self.BULLET_SCALE),
                )
                self._blit_centered(surface, sprite, bullet.x, bullet.y, bullet.width, bullet.height)

        for power in powerups:
            if power.alive:
                sprite = asset_manager.load_image(
                    "powerup_token",
                    self._scaled_size(power.width, power.height, self.POWERUP_SCALE),
                )
                self._blit_centered(surface, sprite, power.x, power.y, power.width, power.height)

        for explosion in explosions:
            if explosion.alive:
                sprite = asset_manager.load_image(
                    "explosion_01",
                    self._scaled_size(explosion.width, explosion.height, self.EXPLOSION_SCALE),
                )
                self._blit_centered(surface, sprite, explosion.x, explosion.y, explosion.width, explosion.height)
