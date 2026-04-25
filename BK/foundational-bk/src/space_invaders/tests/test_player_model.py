from space_invaders.models import Player


def test_player_tick_reduces_cooldowns() -> None:
    player = Player(x=0, y=0, width=10, height=10, cooldown_left=0.5, invulnerable_time=1.0)
    player.tick(0.2)
    assert player.cooldown_left == 0.3
    assert player.invulnerable_time == 0.8
