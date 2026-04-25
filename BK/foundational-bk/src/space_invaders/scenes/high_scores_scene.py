from __future__ import annotations

from space_invaders.core.constants import SceneName
from space_invaders.core.scene import Scene


class HighScoresScene(Scene):
    def __init__(self) -> None:
        super().__init__()
        self._entries: list[tuple[str, int, int]] = []

    def enter(self) -> None:
        repo = self.context["high_score_repository"]
        self._entries = [(e.player_name, e.score, e.wave) for e in repo.top(limit=10)]

    def exit(self) -> None:
        return

    def handle_events(self, events: list[object]) -> None:
        return

    def update(self, delta_time: float) -> None:
        _ = delta_time
        snapshot = self.context["input_snapshot"]
        if "confirm" in snapshot.pressed or "back" in snapshot.pressed:
            self.context["scene_manager"].change_scene(SceneName.MAIN_MENU.value)

    def render(self) -> None:
        surface = self.context["surface"]
        asset_manager = self.context["asset_manager"]
        title_font = asset_manager.get_font(40)
        body_font = asset_manager.get_font(24)

        surface.fill((12, 12, 28))
        title = title_font.render("HIGH SCORES", True, (245, 245, 245))
        surface.blit(title, (surface.get_width() // 2 - title.get_width() // 2, 32))

        y = 92
        if not self._entries:
            line = body_font.render("No scores yet.", True, (190, 190, 190))
            surface.blit(line, (surface.get_width() // 2 - line.get_width() // 2, y))
            y += 40

        for idx, (name, score, wave) in enumerate(self._entries, start=1):
            line = body_font.render(f"{idx:02d}. {name:<8} {score:>6}  W{wave}", True, (230, 230, 180))
            surface.blit(line, (90, y))
            y += 28

        footer = body_font.render("Press confirm/back to return", True, (170, 170, 170))
        surface.blit(footer, (surface.get_width() // 2 - footer.get_width() // 2, surface.get_height() - 40))
