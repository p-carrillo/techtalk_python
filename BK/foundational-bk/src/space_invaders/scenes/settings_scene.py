from __future__ import annotations

from space_invaders.controllers import MenuController
from space_invaders.core.constants import SceneName
from space_invaders.core.scene import Scene


class SettingsScene(Scene):
    def __init__(self) -> None:
        super().__init__()
        self._controller = MenuController()
        self._selection = 0

    def enter(self) -> None:
        self._selection = 0

    def exit(self) -> None:
        return

    def handle_events(self, events: list[object]) -> None:
        return

    def update(self, delta_time: float) -> None:
        _ = delta_time
        snapshot = self.context["input_snapshot"]
        self._selection = self._controller.navigate(self._selection, 3, snapshot)

        if "back" in snapshot.pressed:
            self.context["scene_manager"].change_scene(SceneName.MAIN_MENU.value)
            return

        if "confirm" not in snapshot.pressed:
            return

        settings_service = self.context["settings_service"]
        settings_repo = self.context["settings_repository"]

        if self._selection == 0:
            current = settings_service.value.master_volume
            new_value = 0.0 if current >= 1.0 else round(current + 0.1, 1)
            settings_service.update_volume(new_value)
            settings_repo.save("master_volume", str(new_value))
            self.context["audio_manager"].set_master_volume(new_value)
            return

        if self._selection == 1:
            settings_service.toggle_debug()
            settings_repo.save("debug_mode", "1" if settings_service.value.debug_mode else "0")
            return

        self.context["scene_manager"].change_scene(SceneName.MAIN_MENU.value)

    def render(self) -> None:
        surface = self.context["surface"]
        settings_service = self.context["settings_service"]
        asset_manager = self.context["asset_manager"]

        title_font = asset_manager.get_font(40)
        body_font = asset_manager.get_font(24)

        options = [
            f"Master Volume: {int(settings_service.value.master_volume * 100)}%",
            f"Debug Mode: {'ON' if settings_service.value.debug_mode else 'OFF'}",
            "Back",
        ]

        surface.fill((12, 12, 28))
        title = title_font.render("SETTINGS", True, (245, 245, 245))
        surface.blit(title, (surface.get_width() // 2 - title.get_width() // 2, 32))

        y = 120
        for idx, label in enumerate(options):
            color = (255, 220, 120) if idx == self._selection else (200, 200, 200)
            prefix = "> " if idx == self._selection else "  "
            line = body_font.render(prefix + label, True, color)
            surface.blit(line, (70, y))
            y += 36
