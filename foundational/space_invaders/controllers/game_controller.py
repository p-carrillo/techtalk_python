from __future__ import annotations

from space_invaders.core.input_manager import InputState
from space_invaders.models.entities import Player


class GameController:
    def update_player(self, player: Player, input_state: InputState, delta_time: float, width: int) -> None:
        velocity = 0.0
        if input_state.move_left:
            velocity -= player.speed
        if input_state.move_right:
            velocity += player.speed

        player.rect.x += int(velocity * delta_time)
        if player.rect.left < 0:
            player.rect.left = 0
        if player.rect.right > width:
            player.rect.right = width
