from space_invaders.models import Bullet, Enemy, Player, Shield
from space_invaders.services import CollisionService


def test_collision_enemy_is_destroyed_by_player_bullet() -> None:
    service = CollisionService()
    player = Player(x=0, y=0, width=10, height=10)
    enemy = Enemy(x=10, y=10, width=10, height=10)
    bullet = Bullet(x=12, y=12, width=2, height=2, owner="player")

    report = service.resolve(
        player=player,
        enemies=[enemy],
        player_bullets=[bullet],
        enemy_bullets=[],
        shields=[],
        powerups=[],
    )

    assert not enemy.alive
    assert not bullet.alive
    assert len(report.enemies_destroyed) == 1


def test_collision_shield_takes_damage() -> None:
    service = CollisionService()
    player = Player(x=0, y=0, width=10, height=10)
    shield = Shield(x=10, y=10, width=8, height=8, health=2)
    bullet = Bullet(x=12, y=12, width=2, height=2, owner="enemy")

    report = service.resolve(
        player=player,
        enemies=[],
        player_bullets=[],
        enemy_bullets=[bullet],
        shields=[shield],
        powerups=[],
    )

    assert shield.health == 1
    assert report.shields_damaged == 1
