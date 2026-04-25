from __future__ import annotations

from space_invaders.core.input_manager import InputSnapshot


class MenuController:
    def navigate(self, selection: int, item_count: int, snapshot: InputSnapshot) -> int:
        if "move_left" in snapshot.pressed:
            selection = (selection - 1) % item_count
        if "move_right" in snapshot.pressed:
            selection = (selection + 1) % item_count
        return selection
