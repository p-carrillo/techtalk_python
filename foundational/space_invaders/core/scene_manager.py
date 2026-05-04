from __future__ import annotations

from space_invaders.core.scene import Scene


class SceneManager:
    def __init__(self) -> None:
        self._current: Scene | None = None

    @property
    def current(self) -> Scene | None:
        return self._current

    def change_scene(self, next_scene: Scene) -> None:
        if self._current is not None:
            self._current.exit()
        self._current = next_scene
        self._current.enter()
