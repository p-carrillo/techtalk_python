from __future__ import annotations

from typing import Dict

from .scene import Scene


class SceneManager:
    def __init__(self) -> None:
        self._scenes: Dict[str, Scene] = {}
        self.active_scene_name: str | None = None

    def register(self, name: str, scene: Scene) -> None:
        self._scenes[name] = scene

    def get(self, name: str) -> Scene:
        return self._scenes[name]

    @property
    def active_scene(self) -> Scene:
        if self.active_scene_name is None:
            raise RuntimeError("No active scene registered")
        return self._scenes[self.active_scene_name]

    def change_scene(self, name: str) -> None:
        if self.active_scene_name == name:
            return
        if self.active_scene_name is not None:
            self._scenes[self.active_scene_name].exit()
        self.active_scene_name = name
        self._scenes[name].enter()
