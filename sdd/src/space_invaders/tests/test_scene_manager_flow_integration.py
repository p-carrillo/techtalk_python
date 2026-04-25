from space_invaders.core.scene import Scene
from space_invaders.core.scene_manager import SceneManager


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
