from space_invaders.factories import EnemyFactory


def test_enemy_factory_creates_grid() -> None:
    factory = EnemyFactory()
    enemies = factory.create_wave(rows=3, cols=4, start_x=10, start_y=20)

    assert len(enemies) == 12
    assert enemies[0].x == 10
    assert enemies[0].y == 20
    assert enemies[-1].x > enemies[0].x
