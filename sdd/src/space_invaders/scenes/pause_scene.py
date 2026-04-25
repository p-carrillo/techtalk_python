from __future__ import annotations

from space_invaders.controllers import MenuController
from space_invaders.core.constants import SceneName
from space_invaders.core.scene import Scene
from space_invaders.views import MenuView


class PauseScene(Scene):
    def __init__(self) -> None:
        super().__init__()
        self._menu_view = MenuView()
        self._controller = MenuController()
        self._selection = 0
        self._items = [
            ("Resume", SceneName.GAME.value),
            ("Main Menu", SceneName.MAIN_MENU.value),
        ]

    def enter(self) -> None:
        self._selection = 0

    def exit(self) -> None:
        return

    def handle_events(self, events: list[object]) -> None:
        return

    def update(self, delta_time: float) -> None:
        _ = delta_time
        snapshot = self.context["input_snapshot"]
        self._selection = self._controller.navigate(self._selection, len(self._items), snapshot)

        if "back" in snapshot.pressed:
            self.context["resume_game"] = True
            self.context["scene_manager"].change_scene(SceneName.GAME.value)
            return

        if "confirm" not in snapshot.pressed:
            return

        target = self._items[self._selection][1]
        if target == SceneName.GAME.value:
            self.context["resume_game"] = True
        self.context["scene_manager"].change_scene(target)

    def render(self) -> None:
        asset_manager = self.context["asset_manager"]
        fonts = {
            "title": asset_manager.get_font(48),
            "body": asset_manager.get_font(26),
        }
        surface = self.context["surface"]
        self._menu_view.render(
            surface=surface,
            title="PAUSED",
            options=[label for label, _ in self._items],
            selected=self._selection,
            fonts=fonts,
        )
