from __future__ import annotations

from space_invaders.core.game import Game
from space_invaders.scenes.main_menu_scene import MainMenuScene


def main() -> None:
    game = Game()

    # Load persisted settings at startup.
    game.settings.difficulty = game.settings_repo.get("difficulty", game.settings.difficulty)
    game.settings.debug = bool(int(game.settings_repo.get("debug", "0")))
    persisted_volume = float(game.settings_repo.get("volume", str(game.settings.volume)))
    game.audio.set_volume(persisted_volume)

    game.scene_manager.change_scene(MainMenuScene(game))
    game.run()


if __name__ == "__main__":
    main()
