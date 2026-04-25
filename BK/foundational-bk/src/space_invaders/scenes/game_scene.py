from __future__ import annotations

import random

from space_invaders.controllers import GameController
from space_invaders.core.constants import (
    EVENT_ENEMY_DESTROYED,
    EVENT_GAME_OVER,
    EVENT_LEVEL_COMPLETED,
    EVENT_PLAYER_HIT,
    EVENT_SCORE_CHANGED,
    GameSceneState,
    SceneName,
)
from space_invaders.core.scene import Scene
from space_invaders.factories import BulletFactory, EnemyFactory, PowerUpFactory
from space_invaders.models import Bullet, Enemy, Explosion, Player, PowerUp, Shield
from space_invaders.repositories import HighScore, Progress
from space_invaders.views import GameView, HudView


class GameScene(Scene):
    def __init__(self) -> None:
        super().__init__()
        self.state = GameSceneState.READY
        self.state_timer = 0.0

        self.player = Player(x=220, y=320, width=20, height=12)
        self.enemies: list[Enemy] = []
        self.player_bullets: list[Bullet] = []
        self.enemy_bullets: list[Bullet] = []
        self.shields: list[Shield] = []
        self.explosions: list[Explosion] = []
        self.powerups: list[PowerUp] = []

        self.enemy_direction = 1
        self.enemy_speed = 32.0
        self.rapid_fire_timer = 0.0

        self._controller = GameController()
        self._game_view = GameView()
        self._hud_view = HudView()
        self._enemy_factory = EnemyFactory()
        self._bullet_factory = BulletFactory()
        self._powerup_factory = PowerUpFactory()

    def enter(self) -> None:
        if self.context.get("resume_game", False):
            self.context["resume_game"] = False
            return
        self._start_new_game()

    def exit(self) -> None:
        return

    def handle_events(self, events: list[object]) -> None:
        return

    def _start_new_game(self) -> None:
        self.player = Player(x=220, y=320, width=20, height=12, lives=3)
        self.player_bullets.clear()
        self.enemy_bullets.clear()
        self.powerups.clear()
        self.explosions.clear()
        self.shields = [
            Shield(x=85, y=285, width=35, height=14, health=3),
            Shield(x=220, y=285, width=35, height=14, health=3),
            Shield(x=355, y=285, width=35, height=14, health=3),
        ]

        self.enemy_direction = 1
        self.rapid_fire_timer = 0.0
        self.state = GameSceneState.READY
        self.state_timer = 1.0

        self.context["score_service"].reset()
        self.context["level_service"].reset()
        self._spawn_wave()

        self.context["stats_repository"].increment(games_played=1)
        self.context["event_bus"].publish(EVENT_SCORE_CHANGED, {"score": 0})

    def _spawn_wave(self) -> None:
        config = self.context["level_service"].current_config()
        start_x = max(12.0, (480 - config.cols * 28) / 2)
        self.enemies = self._enemy_factory.create_wave(
            rows=config.rows,
            cols=config.cols,
            start_x=start_x,
            start_y=58,
        )
        self.enemy_speed = config.enemy_speed

    def _trigger_game_over(self) -> None:
        if self.state == GameSceneState.GAME_OVER:
            return

        self.state = GameSceneState.GAME_OVER
        score = self.context["score_service"].score
        wave = self.context["level_service"].current_wave
        self.context["event_bus"].publish(EVENT_GAME_OVER, {"score": score, "wave": wave})
        self.context["last_result"] = {"score": score, "wave": wave}

        self.context["high_score_repository"].add(HighScore(player_name="PLAYER", score=score, wave=wave))
        self.context["progress_repository"].save(Progress(level=1, wave=wave, lives=0, score=score))

        self.context["scene_manager"].change_scene(SceneName.GAME_OVER.value)

    def _cleanup_entities(self, world_h: float) -> None:
        self.player_bullets = [b for b in self.player_bullets if b.alive and b.y + b.height > 0]
        self.enemy_bullets = [b for b in self.enemy_bullets if b.alive and b.y < world_h]
        self.enemies = [e for e in self.enemies if e.alive]
        self.shields = [s for s in self.shields if s.alive]
        self.explosions = [e for e in self.explosions if e.alive]
        self.powerups = [p for p in self.powerups if p.alive and p.y < world_h]

    def _update_enemies(self, delta_time: float) -> None:
        if not self.enemies:
            return

        move_x = self.enemy_direction * self.enemy_speed * delta_time
        hit_edge = False
        for enemy in self.enemies:
            enemy.x += move_x
            if enemy.x < 0 or enemy.x + enemy.width > 480:
                hit_edge = True

        if hit_edge:
            self.enemy_direction *= -1
            for enemy in self.enemies:
                enemy.y += 10

    def _maybe_enemy_shoot(self, delta_time: float) -> None:
        if not self.enemies:
            return

        config = self.context["level_service"].current_config()
        chance = config.fire_chance_per_second * delta_time
        if random.random() > chance:
            return

        shooter = random.choice(self.enemies)
        bullet = self._bullet_factory.create_enemy_bullet(
            x=shooter.x + shooter.width / 2 - 1,
            y=shooter.y + shooter.height,
        )
        self.enemy_bullets.append(bullet)

    def update(self, delta_time: float) -> None:
        self.player.tick(delta_time)

        if self.rapid_fire_timer > 0:
            self.rapid_fire_timer = max(0.0, self.rapid_fire_timer - delta_time)
            self.player.shoot_cooldown = 0.1
        else:
            self.player.shoot_cooldown = 0.25

        for bullet in self.player_bullets:
            bullet.update(delta_time)
        for bullet in self.enemy_bullets:
            bullet.update(delta_time)
        for explosion in self.explosions:
            explosion.update(delta_time)
        for powerup in self.powerups:
            powerup.update(delta_time)

        if self.state == GameSceneState.READY:
            self.state_timer -= delta_time
            if self.state_timer <= 0:
                self.state = GameSceneState.PLAYING
            self._cleanup_entities(world_h=360)
            return

        if self.state == GameSceneState.PLAYER_DIED:
            self.state_timer -= delta_time
            if self.state_timer <= 0:
                if self.player.lives <= 0:
                    self._trigger_game_over()
                    return
                self.player.invulnerable_time = 1.0
                self.player.x = 220
                self.player.y = 320
                self.state = GameSceneState.PLAYING
            self._cleanup_entities(world_h=360)
            return

        if self.state == GameSceneState.LEVEL_CLEARED:
            self.state_timer -= delta_time
            if self.state_timer <= 0:
                self.context["level_service"].next_wave()
                self._spawn_wave()
                self.state = GameSceneState.PLAYING
            self._cleanup_entities(world_h=360)
            return

        if self.state != GameSceneState.PLAYING:
            return

        snapshot = self.context["input_snapshot"]
        actions = self._controller.update_player(self.player, snapshot, delta_time, world_width=480)

        if actions.pause:
            self.context["resume_game"] = True
            self.context["scene_manager"].change_scene(SceneName.PAUSE.value)
            return

        if actions.shoot:
            self.player_bullets.append(
                self._bullet_factory.create_player_bullet(
                    x=self.player.x + self.player.width / 2 - 1,
                    y=self.player.y - 8,
                )
            )
            self.context["stats_repository"].increment(shots_fired=1)

        self._update_enemies(delta_time)
        self._maybe_enemy_shoot(delta_time)

        report = self.context["collision_service"].resolve(
            player=self.player,
            enemies=self.enemies,
            player_bullets=self.player_bullets,
            enemy_bullets=self.enemy_bullets,
            shields=self.shields,
            powerups=self.powerups,
        )

        destroyed_count = len(report.enemies_destroyed)
        if destroyed_count:
            for enemy in report.enemies_destroyed:
                new_score = self.context["score_service"].add(enemy.points)
                self.context["event_bus"].publish(EVENT_ENEMY_DESTROYED, {"points": enemy.points})
                self.context["event_bus"].publish(EVENT_SCORE_CHANGED, {"score": new_score})
                self.explosions.append(Explosion(x=enemy.x, y=enemy.y, width=enemy.width, height=enemy.height))

                maybe_power = self._powerup_factory.maybe_spawn(enemy.x, enemy.y)
                if maybe_power:
                    self.powerups.append(maybe_power)

            self.context["stats_repository"].increment(enemies_destroyed=destroyed_count, shots_hit=destroyed_count)

        if report.player_hit:
            self.context["event_bus"].publish(EVENT_PLAYER_HIT, {})
            self.player.lives -= 1
            self.state = GameSceneState.PLAYER_DIED
            self.state_timer = 1.0

        if report.collected_powerups:
            self.rapid_fire_timer = max(self.rapid_fire_timer, 4.0)

        if any(enemy.y + enemy.height >= self.player.y for enemy in self.enemies):
            self.player.lives = 0

        if self.player.lives <= 0:
            self._trigger_game_over()
            return

        if not self.enemies:
            self.context["event_bus"].publish(
                EVENT_LEVEL_COMPLETED,
                {"wave": self.context["level_service"].current_wave},
            )
            self.state = GameSceneState.LEVEL_CLEARED
            self.state_timer = 1.2

        self._cleanup_entities(world_h=360)
        self.context["debug_info"] = {
            "entities": len(self.enemies) + len(self.player_bullets) + len(self.enemy_bullets),
            "player_x": round(self.player.x, 1),
            "player_y": round(self.player.y, 1),
        }

    def render(self) -> None:
        surface = self.context["surface"]
        asset_manager = self.context["asset_manager"]

        self._game_view.render(
            surface=surface,
            player=self.player,
            enemies=self.enemies,
            player_bullets=self.player_bullets,
            enemy_bullets=self.enemy_bullets,
            shields=self.shields,
            explosions=self.explosions,
            powerups=self.powerups,
        )
        self._hud_view.render(
            surface=surface,
            score=self.context["score_service"].score,
            lives=self.player.lives,
            wave=self.context["level_service"].current_wave,
            font=asset_manager.get_font(20),
        )

        if self.state in (GameSceneState.READY, GameSceneState.PLAYER_DIED, GameSceneState.LEVEL_CLEARED):
            label = {
                GameSceneState.READY: "READY",
                GameSceneState.PLAYER_DIED: "PLAYER HIT",
                GameSceneState.LEVEL_CLEARED: "WAVE CLEARED",
            }[self.state]
            text = asset_manager.get_font(36).render(label, True, (240, 240, 240))
            surface.blit(text, (surface.get_width() // 2 - text.get_width() // 2, 150))
