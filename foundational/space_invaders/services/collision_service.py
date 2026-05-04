from __future__ import annotations

from space_invaders.models.entities import Bullet, Enemy, Player, Shield


class CollisionService:
    def bullets_vs_enemies(self, bullets: list[Bullet], enemies: list[Enemy]) -> int:
        destroyed = 0
        for bullet in bullets:
            if not bullet.alive or not bullet.from_player:
                continue
            for enemy in enemies:
                if enemy.alive and bullet.rect.colliderect(enemy.rect):
                    enemy.alive = False
                    bullet.alive = False
                    destroyed += 1
                    break
        return destroyed

    def bullets_vs_player(self, bullets: list[Bullet], player: Player) -> bool:
        for bullet in bullets:
            if bullet.alive and not bullet.from_player and bullet.rect.colliderect(player.rect):
                bullet.alive = False
                return True
        return False

    def bullets_vs_shields(self, bullets: list[Bullet], shields: list[Shield]) -> None:
        for bullet in bullets:
            if not bullet.alive:
                continue
            for shield in shields:
                if shield.health > 0 and bullet.rect.colliderect(shield.rect):
                    shield.health -= 1
                    bullet.alive = False
                    break

    def enemies_reached_bottom(self, enemies: list[Enemy], bottom: int) -> bool:
        return any(enemy.alive and enemy.rect.bottom >= bottom for enemy in enemies)
