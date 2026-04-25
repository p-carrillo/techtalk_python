import pytest

from space_invaders.core.scene import Scene
from space_invaders.core.scene_manager import SceneManager
from space_invaders.core.settings import GameSettings, SettingsService
from space_invaders.views import MenuView


class DummyScene(Scene):
    def __init__(self) -> None:
        super().__init__()
        self.enter_count = 0
        self.exit_count = 0

    def enter(self) -> None:
        self.enter_count += 1

    def exit(self) -> None:
        self.exit_count += 1

    def handle_events(self, events: list[object]) -> None:
        return

    def update(self, delta_time: float) -> None:
        return

    def render(self) -> None:
        return


def test_scene_manager_routes_transitions() -> None:
    manager = SceneManager()
    a = DummyScene()
    b = DummyScene()

    manager.register("a", a)
    manager.register("b", b)

    manager.change_scene("a")
    manager.change_scene("b")

    assert a.enter_count == 1
    assert a.exit_count == 1
    assert b.enter_count == 1
    assert manager.active_scene is b


def test_scene_manager_keeps_menu_render_operational_with_asset_backgrounds(tmp_path) -> None:
    pygame = pytest.importorskip("pygame")
    pygame.init()
    try:
        assets_root = tmp_path / "assets"
        bg_file = assets_root / "backgrounds" / "bg_main.png"
        bg_file.parent.mkdir(parents=True, exist_ok=True)

        bg_surface = pygame.Surface((32, 24))
        bg_surface.fill((18, 24, 110))
        pygame.image.save(bg_surface, bg_file.as_posix())

        from space_invaders.core.asset_manager import AssetManager

        asset_manager = AssetManager(
            assets_root=assets_root,
            asset_catalog={"bg_main": "backgrounds/bg_main.png"},
            background_ids=("bg_main",),
            default_background_id="bg_main",
        )
        settings_service = SettingsService(GameSettings(background_id="bg_main"))
        surface = pygame.Surface((160, 120))

        class MenuScene(Scene):
            def __init__(self, title: str) -> None:
                super().__init__()
                self._title = title
                self._menu_view = MenuView()

            def enter(self) -> None:
                return

            def exit(self) -> None:
                return

            def handle_events(self, events: list[object]) -> None:
                return

            def update(self, delta_time: float) -> None:
                return

            def render(self) -> None:
                self._menu_view.render(
                    surface=self.context["surface"],
                    title=self._title,
                    options=["Play", "Quit"],
                    selected=0,
                    fonts={
                        "title": self.context["asset_manager"].get_font(20),
                        "body": self.context["asset_manager"].get_font(14),
                    },
                    asset_manager=self.context["asset_manager"],
                    background_id=self.context["settings_service"].value.background_id,
                )

        manager = SceneManager()
        main = MenuScene("MAIN")
        pause = MenuScene("PAUSE")

        context = {
            "asset_manager": asset_manager,
            "settings_service": settings_service,
            "surface": surface,
        }
        main.set_context(context)
        pause.set_context(context)

        manager.register("main", main)
        manager.register("pause", pause)
        manager.change_scene("main")
        manager.active_scene.render()
        manager.change_scene("pause")
        manager.active_scene.render()

        assert manager.active_scene is pause
        assert surface.get_at((0, 0)) != pygame.Color(0, 0, 0, 255)
    finally:
        pygame.quit()
