from __future__ import annotations

from dataclasses import dataclass

from space_invaders.core.input_manager import InputSnapshot
from space_invaders.models import Player


@dataclass(slots=True)
class GameActions:
    shoot: bool = False
    pause: bool = False


class GameController:
    def update_player(
        self,
        player: Player,
        snapshot: InputSnapshot,
        delta_time: float,
        world_width: float,
    ) -> GameActions:
        if "move_left" in snapshot.down:
            player.x -= player.speed * delta_time
        if "move_right" in snapshot.down:
            player.x += player.speed * delta_time

        player.x = max(0.0, min(world_width - player.width, player.x))

        actions = GameActions()
        if "shoot" in snapshot.pressed and player.can_shoot():
            actions.shoot = True
            player.cooldown_left = player.shoot_cooldown
        if "pause" in snapshot.pressed:
            actions.pause = True
        return actions
