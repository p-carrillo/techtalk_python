from __future__ import annotations


class HudView:
    def render(self, surface: object, score: int, lives: int, wave: int, font: object) -> None:
        score_s = font.render(f"Score: {score}", True, (235, 235, 235))
        lives_s = font.render(f"Lives: {lives}", True, (235, 235, 235))
        wave_s = font.render(f"Wave: {wave}", True, (235, 235, 235))

        surface.blit(score_s, (8, 6))
        surface.blit(lives_s, (190, 6))
        surface.blit(wave_s, (330, 6))
