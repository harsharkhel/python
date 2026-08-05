"""
Evaluation bar — vertical bar beside the board showing who has the advantage.
"""

import math
import pygame


def _eval_to_pct(eval_cp):
    """Sigmoid: map centipawns → White's bar fraction (0.0–1.0)."""
    return 1.0 / (1.0 + math.exp(-eval_cp / 400.0))


class EvalBar:
    """Animated vertical evaluation bar."""

    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.target_pct = 0.5
        self.current_pct = 0.5
        self.eval_cp = 0
        self._font = None

    def set_eval(self, eval_cp):
        self.eval_cp = eval_cp
        self.target_pct = _eval_to_pct(eval_cp)

    def update(self, dt):
        diff = self.target_pct - self.current_pct
        self.current_pct += diff * min(1.0, 4.0 * dt)

    def draw(self, surface):
        if self._font is None:
            self._font = pygame.font.SysFont("Menlo, Consolas, monospace", 10, bold=True)

        x, y, w, h = self.x, self.y, self.w, self.h

        # Outline
        pygame.draw.rect(surface, (40, 40, 60), (x - 1, y - 1, w + 2, h + 2),
                         border_radius=3)

        white_h = int(h * self.current_pct)
        black_h = h - white_h

        # Black portion (top)
        if black_h > 0:
            r = pygame.Rect(x, y, w, black_h)
            pygame.draw.rect(surface, (50, 50, 55), r)
        # White portion (bottom)
        if white_h > 0:
            r = pygame.Rect(x, y + black_h, w, white_h)
            pygame.draw.rect(surface, (220, 220, 220), r)

        # Score label near division line
        from coach import format_eval  # local to avoid circular
        score = format_eval(self.eval_cp)
        on_white = self.current_pct > 0.5
        fg = (30, 30, 30) if on_white else (200, 200, 200)
        bg = (220, 220, 220, 190) if on_white else (50, 50, 55, 190)

        txt = self._font.render(score, True, fg)
        tx = x + w // 2 - txt.get_width() // 2
        ty = y + black_h
        ty = max(y + 2, min(ty - txt.get_height() // 2, y + h - txt.get_height() - 2))

        bg_surf = pygame.Surface((txt.get_width() + 4, txt.get_height() + 2),
                                 pygame.SRCALPHA)
        bg_surf.fill(bg)
        surface.blit(bg_surf, (tx - 2, ty - 1))
        surface.blit(txt, (tx, ty))
