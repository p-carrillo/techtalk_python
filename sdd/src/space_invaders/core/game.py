from __future__ import annotations

from pathlib import Path

from space_invaders.core.asset_manager import AssetManager
from space_invaders.core.audio_manager import AudioManager
from space_invaders.core.constants import ACTIONS, SceneName
from space_invaders.core.event_bus import EventBus
from space_invaders.core.input_manager import InputManager, InputSnapshot
from space_invaders.core.scene_manager import SceneManager
from space_invaders.core.settings import GameSettings, SettingsService
from space_invaders.repositories import (
    Database,
    HighScoreRepository,
    ProgressRepository,
    SettingsRepository,
    StatsRepository,
)
from space_invaders.scenes import (
    GameOverScene,
    GameScene,
    HighScoresScene,
    MainMenuScene,
    PauseScene,
    SettingsScene,
)
from space_invaders.services import CollisionService, LevelService, ScoreService, WaveService


class Game:
    def __init__(self) -> None:
        import pygame

        pygame.init()
        pygame.font.init()

        settings = GameSettings()
        self.settings_service = SettingsService(settings)

        self.screen = pygame.display.set_mode((settings.resolution_width, settings.resolution_height))
        pygame.display.set_caption("Space Invaders")
        self.surface = pygame.Surface((settings.logical_width, settings.logical_height))
        self.clock = pygame.time.Clock()

        self.data_root = Path(".game_data")
        self.assets_root = Path("assets")

        database = Database(self.data_root / "space_invaders.db")
        database.migrate()

        self.high_score_repository = HighScoreRepository(database)
        self.settings_repository = SettingsRepository(database)
        self.stats_repository = StatsRepository(database)
        self.progress_repository = ProgressRepository(database)

        self.event_bus = EventBus()
        self.scene_manager = SceneManager()
        self.asset_manager = AssetManager(self.assets_root)
        self.audio_manager = AudioManager(master_volume=settings.master_volume)

        self.score_service = ScoreService()
        self.level_service = LevelService(WaveService(difficulty=settings.difficulty))
        self.collision_service = CollisionService()

        keymap = self._build_keymap()
        self.input_manager = InputManager(action_keymap=keymap, keydown_event_type=pygame.KEYDOWN)

        self.context = {
            "game": self,
            "settings_service": self.settings_service,
            "scene_manager": self.scene_manager,
            "asset_manager": self.asset_manager,
            "audio_manager": self.audio_manager,
            "event_bus": self.event_bus,
            "score_service": self.score_service,
            "level_service": self.level_service,
            "collision_service": self.collision_service,
            "high_score_repository": self.high_score_repository,
            "settings_repository": self.settings_repository,
            "stats_repository": self.stats_repository,
            "progress_repository": self.progress_repository,
            "input_snapshot": InputSnapshot(down=set(), pressed=set()),
            "surface": self.surface,
            "screen": self.screen,
            "resume_game": False,
            "debug_info": {},
            "last_result": {},
        }

        scenes = {
            SceneName.MAIN_MENU.value: MainMenuScene(),
            SceneName.GAME.value: GameScene(),
            SceneName.PAUSE.value: PauseScene(),
            SceneName.GAME_OVER.value: GameOverScene(),
            SceneName.HIGH_SCORES.value: HighScoresScene(),
            SceneName.SETTINGS.value: SettingsScene(),
        }

        for name, scene in scenes.items():
            scene.set_context(self.context)
            self.scene_manager.register(name, scene)

        self.scene_manager.change_scene(SceneName.MAIN_MENU.value)
        self.running = True

    def _build_keymap(self) -> dict[str, set[int]]:
        import pygame

        keymap = {
            "move_left": {pygame.K_LEFT, pygame.K_a, pygame.K_UP},
            "move_right": {pygame.K_RIGHT, pygame.K_d, pygame.K_DOWN},
            "shoot": {pygame.K_SPACE},
            "pause": {pygame.K_ESCAPE},
            "confirm": {pygame.K_RETURN, pygame.K_SPACE},
            "back": {pygame.K_BACKSPACE},
        }
        for action in ACTIONS:
            keymap.setdefault(action, set())
        return keymap

    def stop(self) -> None:
        self.running = False

    def _render_debug_overlay(self, fps: float) -> None:
        import pygame

        debug_info = self.context.get("debug_info", {})
        font = self.asset_manager.get_font(18)

        lines = [
            f"FPS: {fps:.1f}",
            f"Scene: {self.scene_manager.active_scene_name}",
            f"Entities: {debug_info.get('entities', 0)}",
            f"Player: ({debug_info.get('player_x', '-')} , {debug_info.get('player_y', '-')})",
        ]

        y = 10
        for line in lines:
            text = font.render(line, True, (40, 40, 40), (240, 240, 240))
            self.screen.blit(text, (10, y))
            y += 20

    def run(self) -> None:
        import pygame

        while self.running:
            delta_time = self.clock.tick(self.settings_service.value.target_fps) / 1000.0
            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False

            snapshot = self.input_manager.update(events, pygame.key.get_pressed())
            self.context["input_snapshot"] = snapshot

            scene = self.scene_manager.active_scene
            scene.handle_events(events)
            scene.update(delta_time)
            scene.render()

            scaled = pygame.transform.scale(self.surface, self.screen.get_size())
            self.screen.blit(scaled, (0, 0))

            if self.settings_service.value.debug_mode:
                self._render_debug_overlay(self.clock.get_fps())

            pygame.display.flip()

        pygame.quit()
