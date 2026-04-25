from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Iterable, Set


@dataclass(slots=True)
class InputSnapshot:
    down: Set[str]
    pressed: Set[str]


class InputManager:
    def __init__(self, action_keymap: Dict[str, set[int]], keydown_event_type: int) -> None:
        self._action_keymap = action_keymap
        self._keydown_event_type = keydown_event_type
        self._down: Set[str] = set()
        self._pressed: Set[str] = set()

    def update(self, events: Iterable[Any], pressed_keys: Any) -> InputSnapshot:
        self._pressed.clear()
        self._down.clear()

        for action, keys in self._action_keymap.items():
            if any(pressed_keys[k] for k in keys):
                self._down.add(action)

        for event in events:
            if getattr(event, "type", None) != self._keydown_event_type:
                continue
            key = getattr(event, "key", None)
            for action, keys in self._action_keymap.items():
                if key in keys:
                    self._pressed.add(action)

        return InputSnapshot(down=set(self._down), pressed=set(self._pressed))

    def is_down(self, action: str) -> bool:
        return action in self._down

    def was_pressed(self, action: str) -> bool:
        return action in self._pressed
