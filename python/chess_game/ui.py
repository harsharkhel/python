"""
UI components — buttons, main menu, promotion dialog, game-over overlay.
"""

import pygame
import chess
from constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, BG_COLOR,
    BUTTON_BG, BUTTON_HOVER, BUTTON_TEXT,
    ACCENT, ACCENT_HOVER,
    TEXT_PRIMARY, TEXT_SECONDARY, TEXT_DIM,
    PANEL_BORDER, MODAL_BG,
    TIME_CONTROLS, WHITE_PIECE,
)


# ═══════════════════════════════════════════════════════════
# Button
# ═══════════════════════════════════════════════════════════

class Button:
    """Styled clickable button with hover effect."""

    def __init__(self, rect, text, *,
                 color=BUTTON_BG, hover_color=BUTTON_HOVER,
                 text_color=BUTTON_TEXT, font_size=16, border_radius=8):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.font_size = font_size
        self.border_radius = border_radius
        self.hovered = False
        self._font = None

    def _init_font(self):
        if self._font is None:
            self._font = pygame.font.SysFont("Helvetica, Arial", self.font_size)

    def update(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)

    def is_clicked(self, event):
        return (event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
                and self.rect.collidepoint(event.pos))

    def draw(self, surface):
        self._init_font()
        bg = self.hover_color if self.hovered else self.color
        pygame.draw.rect(surface, bg, self.rect,
                         border_radius=self.border_radius)
        border = tuple(min(c + 30, 255) for c in bg)
        pygame.draw.rect(surface, border, self.rect, 1,
                         border_radius=self.border_radius)
        lbl = self._font.render(self.text, True, self.text_color)
        surface.blit(lbl, lbl.get_rect(center=self.rect.center))


# ═══════════════════════════════════════════════════════════
# Main Menu
# ═══════════════════════════════════════════════════════════

def draw_main_menu(surface, buttons, selected_tc_idx):
    """Render the main-menu screen."""
    surface.fill(BG_COLOR)

    # ── decorative board pattern (subtle) ──
    pattern_size = 40
    pattern_alpha = 12
    pat = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
    for r in range(WINDOW_HEIGHT // pattern_size + 1):
        for c in range(WINDOW_WIDTH // pattern_size + 1):
            if (r + c) % 2:
                pygame.draw.rect(pat, (255, 255, 255, pattern_alpha),
                                 (c * pattern_size, r * pattern_size,
                                  pattern_size, pattern_size))
    surface.blit(pat, (0, 0))

    # ── title ──
    title_font = pygame.font.SysFont("Helvetica, Arial", 52, bold=True)
    sub_font = pygame.font.SysFont("Helvetica, Arial", 18)

    title = title_font.render("\u2654 Chess", True, TEXT_PRIMARY)
    surface.blit(title, title.get_rect(centerx=WINDOW_WIDTH // 2, y=80))

    sub = sub_font.render("Select time control and start playing",
                          True, TEXT_SECONDARY)
    surface.blit(sub, sub.get_rect(centerx=WINDOW_WIDTH // 2, y=148))

    # ── "TIME CONTROL" label ──
    tc_lbl_font = pygame.font.SysFont("Helvetica, Arial", 14)
    tc_lbl = tc_lbl_font.render("TIME CONTROL", True, TEXT_DIM)
    surface.blit(tc_lbl, tc_lbl.get_rect(centerx=WINDOW_WIDTH // 2, y=210))

    # ── time-control buttons ──
    for i in range(len(TIME_CONTROLS)):
        btn = buttons[f"tc_{i}"]
        if i == selected_tc_idx:
            btn.color = ACCENT
            btn.hover_color = ACCENT_HOVER
        else:
            btn.color = BUTTON_BG
            btn.hover_color = BUTTON_HOVER
        btn.draw(surface)

    # ── start button ──
    buttons["start"].draw(surface)

    # ── footer ──
    foot_font = pygame.font.SysFont("Helvetica, Arial", 12)
    foot = foot_font.render("Local multiplayer \u2022 All standard rules",
                            True, TEXT_DIM)
    surface.blit(foot, foot.get_rect(centerx=WINDOW_WIDTH // 2,
                                     y=WINDOW_HEIGHT - 40))


# ═══════════════════════════════════════════════════════════
# Promotion Dialog
# ═══════════════════════════════════════════════════════════

def get_promotion_rects():
    """Return list of (Rect, piece_type) for the 4 promotion choices."""
    dialog_w, dialog_h = 360, 140
    dx = (WINDOW_WIDTH - dialog_w) // 2
    dy = (WINDOW_HEIGHT - dialog_h) // 2
    spacing = dialog_w // 5
    pieces = [chess.QUEEN, chess.ROOK, chess.BISHOP, chess.KNIGHT]
    out = []
    for i, pt in enumerate(pieces):
        bx = dx + spacing * (i + 1) - 35
        by = dy + 50
        out.append((pygame.Rect(bx, by, 70, 70), pt))
    return out


def draw_promotion_dialog(surface, color):
    """Draw pawn-promotion overlay. Returns the option rects for hit-testing."""
    # Dark overlay
    ov = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
    ov.fill((0, 0, 0, 150))
    surface.blit(ov, (0, 0))

    dialog_w, dialog_h = 360, 140
    dx = (WINDOW_WIDTH - dialog_w) // 2
    dy = (WINDOW_HEIGHT - dialog_h) // 2

    pygame.draw.rect(surface, MODAL_BG,
                     (dx, dy, dialog_w, dialog_h), border_radius=12)
    pygame.draw.rect(surface, PANEL_BORDER,
                     (dx, dy, dialog_w, dialog_h), 2, border_radius=12)

    font = pygame.font.SysFont("Helvetica, Arial", 16)
    title = font.render("Promote pawn to:", True, TEXT_PRIMARY)
    surface.blit(title, title.get_rect(centerx=dx + dialog_w // 2, y=dy + 12))

    piece_font = pygame.font.SysFont("Apple Symbols, Segoe UI Symbol", 42)
    symbols = {
        chess.QUEEN:  "\u2655" if color == chess.WHITE else "\u265b",
        chess.ROOK:   "\u2656" if color == chess.WHITE else "\u265c",
        chess.BISHOP: "\u2657" if color == chess.WHITE else "\u265d",
        chess.KNIGHT: "\u2658" if color == chess.WHITE else "\u265e",
    }

    options = get_promotion_rects()
    mouse = pygame.mouse.get_pos()

    for rect, pt in options:
        hovered = rect.collidepoint(mouse)
        bg = BUTTON_HOVER if hovered else BUTTON_BG
        pygame.draw.rect(surface, bg, rect, border_radius=8)
        pygame.draw.rect(surface, PANEL_BORDER, rect, 1, border_radius=8)

        pc = WHITE_PIECE if color == chess.WHITE else (200, 200, 200)
        glyph = piece_font.render(symbols[pt], True, pc)
        surface.blit(glyph, glyph.get_rect(center=rect.center))

    return options


# ═══════════════════════════════════════════════════════════
# Game Over Overlay
# ═══════════════════════════════════════════════════════════

def draw_game_over(surface, result_text, reason_text, buttons):
    """Render the game-over modal."""
    ov = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
    ov.fill((0, 0, 0, 170))
    surface.blit(ov, (0, 0))

    dw, dh = 380, 220
    dx = (WINDOW_WIDTH - dw) // 2
    dy = (WINDOW_HEIGHT - dh) // 2

    pygame.draw.rect(surface, MODAL_BG, (dx, dy, dw, dh), border_radius=12)
    pygame.draw.rect(surface, PANEL_BORDER, (dx, dy, dw, dh), 2,
                     border_radius=12)

    rf = pygame.font.SysFont("Helvetica, Arial", 28, bold=True)
    res = rf.render(result_text, True, TEXT_PRIMARY)
    surface.blit(res, res.get_rect(centerx=dx + dw // 2, y=dy + 30))

    rsf = pygame.font.SysFont("Helvetica, Arial", 16)
    rsn = rsf.render(reason_text, True, TEXT_SECONDARY)
    surface.blit(rsn, rsn.get_rect(centerx=dx + dw // 2, y=dy + 75))

    for btn in buttons:
        btn.draw(surface)
