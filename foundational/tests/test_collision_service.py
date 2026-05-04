import pygame

from space_invaders.models.entities import Bullet, Enemy, Player, Shield
from space_invaders.services.collision_service import CollisionService


pygame.init()


def test_player_bullet_destroys_enemy() -> None:
    service = CollisionService()
    bullets = [Bullet(rect=pygame.Rect(10, 10, 4, 10), velocity_y=-100, from_player=True)]
    enemies = [Enemy(rect=pygame.Rect(8, 8, 20, 20))]

    destroyed = service.bullets_vs_enemies(bullets, enemies)

    assert destroyed == 1
    assert not bullets[0].alive
    assert not enemies[0].alive


def test_enemy_bullet_hits_player() -> None:
    service = CollisionService()
    player = Player(rect=pygame.Rect(10, 10, 30, 20), speed=1.0, lives=3, cooldown=0.2)
    bullets = [Bullet(rect=pygame.Rect(15, 15, 4, 10), velocity_y=100, from_player=False)]

    assert service.bullets_vs_player(bullets, player) is True
    assert bullets[0].alive is False


def test_bullet_damages_shield() -> None:
    service = CollisionService()
    shield = Shield(rect=pygame.Rect(50, 50, 20, 20), health=4)
    bullet = Bullet(rect=pygame.Rect(55, 55, 4, 8), velocity_y=-10, from_player=True)

    service.bullets_vs_shields([bullet], [shield])

    assert shield.health == 3
    assert bullet.alive is False
