import random
import sys
from dataclasses import dataclass

import pygame


# --- Config ---
WIDTH, HEIGHT = 900, 700
FPS = 60
PLAYER_SPEED = 6
PLAYER_BULLET_SPEED = 10
ENEMY_BULLET_SPEED = 5
MAX_PLAYER_BULLETS = 3
ENEMY_SHOOT_CHANCE = 0.0025


@dataclass
class Bullet:
    rect: pygame.Rect
    speed: int
    from_enemy: bool


class Player:
    def __init__(self, x: int, y: int):
        self.rect = pygame.Rect(x, y, 64, 28)
        self.lives = 3
        self.cooldown = 0

    def update(self, keys: pygame.key.ScancodeWrapper):
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += PLAYER_SPEED

        self.rect.x = max(12, min(WIDTH - self.rect.width - 12, self.rect.x))

        if self.cooldown > 0:
            self.cooldown -= 1

    def try_shoot(self, bullets: list[Bullet]):
        if self.cooldown > 0:
            return

        active_player_bullets = sum(1 for b in bullets if not b.from_enemy)
        if active_player_bullets >= MAX_PLAYER_BULLETS:
            return

        bullet_rect = pygame.Rect(self.rect.centerx - 3, self.rect.top - 14, 6, 14)
        bullets.append(Bullet(bullet_rect, -PLAYER_BULLET_SPEED, from_enemy=False))
        self.cooldown = 12

    def draw(self, surface: pygame.Surface):
        # Cuerpo de la nave
        pygame.draw.rect(surface, (110, 230, 160), self.rect, border_radius=8)
        # Cabina
        cabin = pygame.Rect(self.rect.centerx - 12, self.rect.top - 9, 24, 9)
        pygame.draw.rect(surface, (170, 255, 220), cabin, border_radius=4)


class Invader:
    def __init__(self, x: int, y: int):
        self.rect = pygame.Rect(x, y, 40, 28)
        self.alive = True

    def draw(self, surface: pygame.Surface):
        if not self.alive:
            return
        pygame.draw.rect(surface, (235, 95, 120), self.rect, border_radius=6)
        eye1 = pygame.Rect(self.rect.x + 9, self.rect.y + 8, 6, 6)
        eye2 = pygame.Rect(self.rect.x + 25, self.rect.y + 8, 6, 6)
        pygame.draw.rect(surface, (255, 230, 230), eye1)
        pygame.draw.rect(surface, (255, 230, 230), eye2)


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Space Invaders - Python")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

        self.font = pygame.font.SysFont("consolas", 26)
        self.big_font = pygame.font.SysFont("consolas", 52, bold=True)

        self.running = True
        self.reset()

    def reset(self):
        self.player = Player(WIDTH // 2 - 32, HEIGHT - 70)
        self.bullets: list[Bullet] = []

        self.invaders: list[Invader] = []
        self.invader_direction = 1
        self.invader_speed = 1.0
        self.wave = 1
        self.score = 0

        self._spawn_wave(self.wave)
        self.state = "playing"  # playing | game_over | win

    def _spawn_wave(self, wave: int):
        self.invaders.clear()
        rows = min(6, 3 + wave // 2)
        cols = 10
        start_x = 110
        start_y = 90
        gap_x = 62
        gap_y = 50

        for row in range(rows):
            for col in range(cols):
                x = start_x + col * gap_x
                y = start_y + row * gap_y
                self.invaders.append(Invader(x, y))

        self.invader_speed = min(4.0, 0.8 + wave * 0.35)

    def _alive_invaders(self) -> list[Invader]:
        return [i for i in self.invaders if i.alive]

    def _update_invaders(self):
        alive = self._alive_invaders()
        if not alive:
            self.wave += 1
            if self.wave > 8:
                self.state = "win"
                return
            self._spawn_wave(self.wave)
            return

        step = self.invader_direction * self.invader_speed
        for inv in alive:
            inv.rect.x += int(step)

        min_x = min(inv.rect.left for inv in alive)
        max_x = max(inv.rect.right for inv in alive)

        if min_x <= 16 or max_x >= WIDTH - 16:
            self.invader_direction *= -1
            for inv in alive:
                inv.rect.y += 22

        # Si llegan abajo, se pierde
        if any(inv.rect.bottom >= self.player.rect.top for inv in alive):
            self.state = "game_over"

        # Disparo enemigo aleatorio
        if random.random() < ENEMY_SHOOT_CHANCE + self.wave * 0.0005:
            shooter = random.choice(alive)
            b = pygame.Rect(shooter.rect.centerx - 3, shooter.rect.bottom + 4, 6, 14)
            self.bullets.append(Bullet(b, ENEMY_BULLET_SPEED + self.wave // 2, from_enemy=True))

    def _update_bullets(self):
        for b in self.bullets:
            b.rect.y += b.speed

        # Quitar balas fuera de pantalla
        self.bullets = [b for b in self.bullets if -20 < b.rect.y < HEIGHT + 20]

        # Colisiones
        remaining: list[Bullet] = []
        for b in self.bullets:
            if b.from_enemy:
                if b.rect.colliderect(self.player.rect):
                    self.player.lives -= 1
                    if self.player.lives <= 0:
                        self.state = "game_over"
                    continue
            else:
                hit = False
                for inv in self.invaders:
                    if inv.alive and b.rect.colliderect(inv.rect):
                        inv.alive = False
                        self.score += 10
                        hit = True
                        break
                if hit:
                    continue
            remaining.append(b)

        self.bullets = remaining

    def _draw_background(self):
        self.screen.fill((8, 10, 22))
        # Estrellas simples
        for i in range(55):
            x = (i * 137) % WIDTH
            y = (i * 211 + pygame.time.get_ticks() // 30) % HEIGHT
            self.screen.set_at((x, y), (130, 140, 170))

    def _draw_hud(self):
        text = f"PUNTOS: {self.score}   VIDAS: {self.player.lives}   OLEADA: {self.wave}"
        surface = self.font.render(text, True, (230, 235, 255))
        self.screen.blit(surface, (20, 18))

        help_text = "A/D o <-/-> mover, ESPACIO disparar, R reiniciar, ESC salir"
        h = self.font.render(help_text, True, (140, 150, 180))
        self.screen.blit(h, (20, HEIGHT - 34))

    def _draw_overlay(self):
        if self.state == "playing":
            return

        if self.state == "game_over":
            title = "GAME OVER"
            subtitle = "Pulsa R para volver a empezar"
            color = (255, 120, 130)
        else:
            title = "VICTORIA"
            subtitle = "Has eliminado todas las oleadas. Pulsa R para jugar otra vez"
            color = (120, 255, 180)

        t = self.big_font.render(title, True, color)
        s = self.font.render(subtitle, True, (230, 235, 255))

        box = pygame.Rect(120, HEIGHT // 2 - 100, WIDTH - 240, 200)
        pygame.draw.rect(self.screen, (18, 22, 44), box, border_radius=16)
        pygame.draw.rect(self.screen, color, box, width=3, border_radius=16)

        self.screen.blit(t, (WIDTH // 2 - t.get_width() // 2, HEIGHT // 2 - 54))
        self.screen.blit(s, (WIDTH // 2 - s.get_width() // 2, HEIGHT // 2 + 18))

    def draw(self):
        self._draw_background()

        self.player.draw(self.screen)
        for inv in self.invaders:
            inv.draw(self.screen)

        for b in self.bullets:
            color = (255, 240, 130) if not b.from_enemy else (255, 110, 120)
            pygame.draw.rect(self.screen, color, b.rect, border_radius=3)

        self._draw_hud()
        self._draw_overlay()
        pygame.display.flip()

    def run(self):
        while self.running:
            self.clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    elif event.key == pygame.K_r:
                        self.reset()
                    elif event.key == pygame.K_SPACE and self.state == "playing":
                        self.player.try_shoot(self.bullets)

            keys = pygame.key.get_pressed()

            if self.state == "playing":
                self.player.update(keys)

                # Disparo continuo al mantener espacio
                if keys[pygame.K_SPACE]:
                    self.player.try_shoot(self.bullets)

                self._update_invaders()
                self._update_bullets()

            self.draw()

        pygame.quit()


def main():
    try:
        Game().run()
    except pygame.error as exc:
        print("Error de pygame:", exc)
        print("Asegurate de tener una salida grafica disponible y pygame instalado.")
        sys.exit(1)


if __name__ == "__main__":
    main()
