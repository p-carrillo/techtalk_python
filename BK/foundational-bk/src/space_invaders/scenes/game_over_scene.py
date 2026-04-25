from __future__ import annotations

from space_invaders.controllers import MenuController
from space_invaders.core.constants import SceneName
from space_invaders.core.scene import Scene
from space_invaders.views import MenuView


class GameOverScene(Scene):
    def __init__(self) -> None:
        super().__init__()
        self._menu_view = MenuView()
        self._controller = MenuController()
        self._selection = 0
        self._items = [
            ("Restart", SceneName.GAME.value),
            ("Main Menu", SceneName.MAIN_MENU.value),
        ]
        self._title = "GAME OVER"

    def enter(self) -> None:
        self._selection = 0
        result = self.context.get("last_result", {})
        score = int(result.get("score", 0))
        wave = int(result.get("wave", 1))
        self._title = f"GAME OVER - {score} pts W{wave}"

    def exit(self) -> None:
        return

    def handle_events(self, events: list[object]) -> None:
        return

    def update(self, delta_time: float) -> None:
        _ = delta_time
        snapshot = self.context["input_snapshot"]
        self._selection = self._controller.navigate(self._selection, len(self._items), snapshot)

        if "confirm" not in snapshot.pressed:
            return

        target = self._items[self._selection][1]
        self.context["scene_manager"].change_scene(target)

    def render(self) -> None:
        asset_manager = self.context["asset_manager"]
        fonts = {
            "title": asset_manager.get_font(36),
            "body": asset_manager.get_font(26),
        }
        surface = self.context["surface"]
        self._menu_view.render(
            surface=surface,
            title=self._title,
            options=[label for label, _ in self._items],
            selected=self._selection,
            fonts=fonts,
        )
