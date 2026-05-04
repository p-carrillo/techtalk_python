from __future__ import annotations

import random
from dataclasses import dataclass
from enum import Enum, auto

import pygame

from space_invaders.controllers.game_controller import GameController
from space_invaders.core.constants import (
    ENEMY_DROP_STEP,
    ENEMY_SHOOT_BASE_CHANCE,
    PLAYER_COOLDOWN,
    PLAYER_LIVES,
    PLAYER_SPEED,
    SCORE_ENEMY,
    SCORE_WAVE_CLEAR,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    SHIELD_HEALTH,
)
from space_invaders.core.scene import Scene
from space_invaders.factories.bullet_factory import BulletFactory
from space_invaders.factories.enemy_factory import EnemyFactory
from space_invaders.factories.level_factory import LevelFactory
from space_invaders.factories.powerup_factory import PowerUpFactory
from space_invaders.models.entities import Bullet, Enemy, Explosion, Player, PowerUp, Shield
from space_invaders.services.collision_service import CollisionService
from space_invaders.services.wave_service import WaveService
from space_invaders.views.ui import draw_text


class GameSceneState(Enum):
    READY = auto()
    PLAYING = auto()
    PLAYER_DIED = auto()
    LEVEL_CLEARED = auto()
    GAME_OVER = auto()


@dataclass(slots=True)
class EnemyMotion:
    timer: float = 0.0
    interval: float = 0.8


class GameScene(Scene):
    def __init__(self, game: "Game", start_level: int = 1) -> None:
        super().__init__(game)
        self.state = GameSceneState.READY
        self.state_timer = 1.0
        self.score = 0
        self.level = start_level

        self.player = Player(
            rect=pygame.Rect(SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT - 60, 40, 24),
            speed=PLAYER_SPEED,
            lives=PLAYER_LIVES,
            cooldown=PLAYER_COOLDOWN,
        )

        self.enemies: list[Enemy] = []
        self.bullets: list[Bullet] = []
        self.shields: list[Shield] = []
        self.explosions: list[Explosion] = []
        self.powerups: list[PowerUp] = []

        self.enemy_motion = EnemyMotion()
        self.controller = GameController()
        self.wave_service = WaveService()
        self.level_factory = LevelFactory()
        self.enemy_factory = EnemyFactory()
        self.bullet_factory = BulletFactory()
        self.powerup_factory = PowerUpFactory()
        self.collision = CollisionService()

        self.title_font = self.game.assets.get_font(44)
        self.ui_font = self.game.assets.get_font(24)
        self.small_font = self.game.assets.get_font(18)

        self._initialized = False

        self.game.events.subscribe("enemy_destroyed", self._on_enemy_destroyed)
        self.game.events.subscribe("player_hit", self._on_player_hit)

    def enter(self) -> None:
        if not self._initialized:
            self._setup_level(reset_score=True)
            self._initialized = True

    def exit(self) -> None:
        return

    def handle_events(self, events: list[pygame.event.Event]) -> None:
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == self.game.settings.controls["pause"]:
                from space_invaders.scenes.pause_scene import PauseScene

                self.game.scene_manager.change_scene(PauseScene(self.game, self))
                return

    def update(self, delta_time: float) -> None:
        if self.state == GameSceneState.READY:
            self.state_timer -= delta_time
            if self.state_timer <= 0:
                self.state = GameSceneState.PLAYING
            return

        if self.state == GameSceneState.PLAYER_DIED:
            self.state_timer -= delta_time
            if self.state_timer <= 0:
                if self.player.lives <= 0:
                    self.state = GameSceneState.GAME_OVER
                    self._go_game_over()
                    return
                self.player.rect.centerx = SCREEN_WIDTH // 2
                self.state = GameSceneState.PLAYING
            return

        if self.state == GameSceneState.LEVEL_CLEARED:
            self.state_timer -= delta_time
            if self.state_timer <= 0:
                self.level += 1
                self._setup_level(reset_score=False)
                self.state = GameSceneState.READY
                self.state_timer = 1.0
            return

        if self.state != GameSceneState.PLAYING:
            return

        pressed = pygame.key.get_pressed()
        input_state = self.game.input.to_state(pressed)

        self.controller.update_player(self.player, input_state, delta_time, SCREEN_WIDTH)

        self.player.cooldown_timer = max(0.0, self.player.cooldown_timer - delta_time)
        if input_state.shoot and self.player.cooldown_timer <= 0:
            self.bullets.append(self.bullet_factory.player_bullet(self.player))
            self.player.cooldown_timer = self.player.cooldown

        self._update_enemies(delta_time)
        self._maybe_enemy_shot()
        self._update_bullets(delta_time)
        self._update_powerups(delta_time)
        self._resolve_collisions()
        self._cleanup_entities()
        self._update_explosions(delta_time)

        if self.wave_service.all_destroyed(self.enemies):
            self.score += SCORE_WAVE_CLEAR
            self.game.events.publish("level_completed", level=self.level)
            self.state = GameSceneState.LEVEL_CLEARED
            self.state_timer = 1.0

        if self.collision.enemies_reached_bottom(self.enemies, SCREEN_HEIGHT - 90):
            self.player.lives = 0
            self._on_player_hit()

    def render(self) -> None:
        screen = self.game.screen
        screen.fill((8, 8, 20))

        pygame.draw.rect(screen, (40, 220, 90), self.player.rect)

        for enemy in self.enemies:
            if enemy.alive:
                pygame.draw.rect(screen, (220, 80, 100), enemy.rect)

        for bullet in self.bullets:
            if bullet.alive:
                color = (240, 240, 140) if bullet.from_player else (255, 100, 100)
                pygame.draw.rect(screen, color, bullet.rect)

        for shield in self.shields:
            if shield.health > 0:
                intensity = 40 + shield.health * 45
                pygame.draw.rect(screen, (70, intensity, 210), shield.rect)

        for powerup in self.powerups:
            if powerup.active:
                pygame.draw.rect(screen, (140, 210, 255), powerup.rect)

        for explosion in self.explosions:
            pygame.draw.circle(screen, (255, 180, 90), explosion.pos, 12)

        draw_text(screen, self.ui_font, f"SCORE {self.score}", (20, 12))
        draw_text(screen, self.ui_font, f"LIVES {self.player.lives}", (20, 40))
        draw_text(screen, self.ui_font, f"LEVEL {self.level}", (20, 68))

        if self.state == GameSceneState.READY:
            draw_text(screen, self.title_font, "READY", (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), center=True)
        elif self.state == GameSceneState.PLAYER_DIED:
            draw_text(screen, self.title_font, "PLAYER HIT", (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), center=True)
        elif self.state == GameSceneState.LEVEL_CLEARED:
            draw_text(screen, self.title_font, "LEVEL CLEARED", (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), center=True)

        if self.game.settings.debug:
            self._render_debug()

    def _setup_level(self, reset_score: bool) -> None:
        if reset_score:
            self.score = 0
            self.player.lives = PLAYER_LIVES

        level_def = self.level_factory.create(self.level)
        self.wave_service.setup_level(self.level)
        self.enemy_motion.interval = max(0.18, 0.8 / level_def.enemy_speed_multiplier)
        self.enemy_fire_bonus = level_def.enemy_fire_bonus

        self.enemies = self.enemy_factory.create_wave()
        self.bullets.clear()
        self.explosions.clear()
        self.powerups.clear()

        self.shields = [
            Shield(pygame.Rect(180 + i * 180, SCREEN_HEIGHT - 150, 90, 40), SHIELD_HEALTH)
            for i in range(4)
        ]

    def _update_enemies(self, delta_time: float) -> None:
        self.enemy_motion.timer += delta_time
        if self.enemy_motion.timer < self.enemy_motion.interval:
            return
        self.enemy_motion.timer = 0.0

        alive = [enemy for enemy in self.enemies if enemy.alive]
        if not alive:
            return

        left = min(enemy.rect.left for enemy in alive)
        right = max(enemy.rect.right for enemy in alive)

        if left <= 24 and self.wave_service.direction < 0:
            self.wave_service.direction = 1
            for enemy in alive:
                enemy.rect.y += ENEMY_DROP_STEP
        elif right >= SCREEN_WIDTH - 24 and self.wave_service.direction > 0:
            self.wave_service.direction = -1
            for enemy in alive:
                enemy.rect.y += ENEMY_DROP_STEP

        dx = int(self.wave_service.enemy_speed * self.wave_service.direction * self.enemy_motion.interval)
        for enemy in alive:
            enemy.rect.x += dx

    def _maybe_enemy_shot(self) -> None:
        living = [enemy for enemy in self.enemies if enemy.alive]
        if not living:
            return
        chance = ENEMY_SHOOT_BASE_CHANCE + self.enemy_fire_bonus
        if random.random() < chance * max(1, len(living) // 4):
            shooter = random.choice(living)
            self.bullets.append(self.bullet_factory.enemy_bullet(shooter))

    def _update_bullets(self, delta_time: float) -> None:
        for bullet in self.bullets:
            if bullet.alive:
                bullet.rect.y += int(bullet.velocity_y * delta_time)
                if bullet.rect.bottom < 0 or bullet.rect.top > SCREEN_HEIGHT:
                    bullet.alive = False

    def _update_powerups(self, delta_time: float) -> None:
        for powerup in self.powerups:
            if not powerup.active:
                continue
            powerup.rect.y += int(120 * delta_time)
            if powerup.rect.top > SCREEN_HEIGHT:
                powerup.active = False
            elif powerup.rect.colliderect(self.player.rect):
                powerup.active = False
                self.player.cooldown = max(0.12, self.player.cooldown - 0.05)

    def _resolve_collisions(self) -> None:
        destroyed = self.collision.bullets_vs_enemies(self.bullets, self.enemies)
        if destroyed:
            self.score += destroyed * SCORE_ENEMY
            self.game.events.publish("score_changed", score=self.score)
            for enemy in self.enemies:
                if not enemy.alive:
                    self.game.events.publish("enemy_destroyed", x=enemy.rect.centerx, y=enemy.rect.centery)

        self.collision.bullets_vs_shields(self.bullets, self.shields)

        if self.collision.bullets_vs_player(self.bullets, self.player):
            self.game.events.publish("player_hit")

    def _cleanup_entities(self) -> None:
        self.bullets = [bullet for bullet in self.bullets if bullet.alive]
        self.powerups = [powerup for powerup in self.powerups if powerup.active]

    def _update_explosions(self, delta_time: float) -> None:
        for explosion in self.explosions:
            explosion.ttl -= delta_time
        self.explosions = [explosion for explosion in self.explosions if explosion.ttl > 0]

    def _on_enemy_destroyed(self, x: int, y: int) -> None:
        self.explosions.append(Explosion((x, y)))
        maybe = self.powerup_factory.maybe_spawn(x, y)
        if maybe:
            self.powerups.append(maybe)

    def _on_player_hit(self) -> None:
        self.player.lives -= 1
        self.state = GameSceneState.PLAYER_DIED
        self.state_timer = 1.0

    def _go_game_over(self) -> None:
        from space_invaders.scenes.game_over_scene import GameOverScene

        self.game.events.publish("game_over", score=self.score)
        self.game.stats_repo.increment("games_played", 1)
        self.game.high_scores.add("PLAYER", self.score)
        self.game.scene_manager.change_scene(GameOverScene(self.game, self.score))

    def _render_debug(self) -> None:
        fps = int(self.game.clock.get_fps())
        active_entities = len([enemy for enemy in self.enemies if enemy.alive]) + len(self.bullets)
        lines = [
            f"FPS: {fps}",
            f"Scene: {self.game.active_scene_name}",
            f"Active entities: {active_entities}",
            f"Player: ({self.player.rect.x},{self.player.rect.y})",
            f"State: {self.state.name}",
        ]
        y = 12
        for line in lines:
            draw_text(self.game.screen, self.small_font, line, (SCREEN_WIDTH - 260, y), (180, 220, 255))
            y += 18

        for enemy in self.enemies:
            if enemy.alive:
                pygame.draw.rect(self.game.screen, (80, 140, 255), enemy.rect, 1)
        pygame.draw.rect(self.game.screen, (80, 255, 180), self.player.rect, 1)
        for bullet in self.bullets:
            if bullet.alive:
                pygame.draw.rect(self.game.screen, (255, 255, 255), bullet.rect, 1)
