from __future__ import annotations

import time
from pathlib import Path

import pygame

from space_invaders.core.asset_manager import AssetManager
from space_invaders.core.audio_manager import AudioManager
from space_invaders.core.constants import DB_FILE, TITLE
from space_invaders.core.event_bus import EventBus
from space_invaders.core.input_manager import InputManager
from space_invaders.core.scene_manager import SceneManager
from space_invaders.core.settings import Settings
from space_invaders.repositories.sqlite import SQLiteDatabase
from space_invaders.repositories.high_scores import HighScoreRepository
from space_invaders.repositories.settings_repo import SettingsRepository
from space_invaders.repositories.stats import StatsRepository


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode(self.settings.resolution)
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True

        self.scene_manager = SceneManager()
        self.assets = AssetManager()
        self.audio = AudioManager(self.settings.volume)
        self.events = EventBus()
        self.input = InputManager(self.settings.controls)

        db_path = Path(DB_FILE)
        self.db = SQLiteDatabase(db_path)
        self.high_scores = HighScoreRepository(self.db)
        self.settings_repo = SettingsRepository(self.db)
        self.stats_repo = StatsRepository(self.db)

    @property
    def active_scene_name(self) -> str:
        scene = self.scene_manager.current
        return scene.__class__.__name__ if scene else "None"

    def run(self) -> None:
        previous = time.perf_counter()
        while self.running:
            now = time.perf_counter()
            delta_time = now - previous
            previous = now

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False

            scene = self.scene_manager.current
            if scene is None:
                self.running = False
                continue

            scene.handle_events(events)
            scene.update(delta_time)
            scene.render()

            pygame.display.flip()
            self.clock.tick(self.settings.fps)

        pygame.quit()
