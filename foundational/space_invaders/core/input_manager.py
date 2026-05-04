from __future__ import annotations

from dataclasses import dataclass

import pygame


@dataclass(slots=True)
class InputState:
    move_left: bool = False
    move_right: bool = False
    shoot: bool = False
    pause: bool = False
    confirm: bool = False
    back: bool = False


class InputManager:
    def __init__(self, controls: dict[str, int]) -> None:
        self.controls = controls

    def to_state(self, pressed: pygame.key.ScancodeWrapper) -> InputState:
        return InputState(
            move_left=pressed[self.controls["move_left"]],
            move_right=pressed[self.controls["move_right"]],
            shoot=pressed[self.controls["shoot"]],
            pause=pressed[self.controls["pause"]],
            confirm=pressed[self.controls["confirm"]],
            back=pressed[self.controls["back"]],
        )
