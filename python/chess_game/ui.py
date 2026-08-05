"""
UI components — buttons, menus, promotion dialog, game-over overlay,
enhanced GrandMaster AI menu, and player stats screen.
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
    GAME_MODES, DIFFICULTY_NAMES,
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
# Enhanced Main Menu (GrandMaster AI)
# ═══════════════════════════════════════════════════════════

def draw_enhanced_menu(surface, buttons, selected_mode, selected_diff, selected_tc):
    """Render the GrandMaster AI main menu."""
    surface.fill(BG_COLOR)

    # Decorative board pattern
    ps = 40
    pa = 12
    pat = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
    for r in range(WINDOW_HEIGHT // ps + 1):
        for c in range(WINDOW_WIDTH // ps + 1):
            if (r + c) % 2:
                pygame.draw.rect(pat, (255, 255, 255, pa),
                                 (c * ps, r * ps, ps, ps))
    surface.blit(pat, (0, 0))

    # ── Title ──
    tf = pygame.font.SysFont("Helvetica, Arial", 48, bold=True)
    sf = pygame.font.SysFont("Helvetica, Arial", 17)

    title = tf.render("\u2654 GrandMaster AI", True, TEXT_PRIMARY)
    surface.blit(title, title.get_rect(centerx=WINDOW_WIDTH // 2, y=48))

    sub = sf.render("AI Chess Coach & Trainer", True, ACCENT)
    surface.blit(sub, sub.get_rect(centerx=WINDOW_WIDTH // 2, y=110))

    lbl_font = pygame.font.SysFont("Helvetica, Arial", 12)

    # ── GAME MODE ──
    lbl = lbl_font.render("GAME MODE", True, TEXT_DIM)
    surface.blit(lbl, lbl.get_rect(centerx=WINDOW_WIDTH // 2, y=155))
    for i, (name, _) in enumerate(GAME_MODES):
        btn = buttons[f"mode_{i}"]
        if i == selected_mode:
            btn.color = ACCENT
            btn.hover_color = ACCENT_HOVER
        else:
            btn.color = BUTTON_BG
            btn.hover_color = BUTTON_HOVER
        btn.draw(surface)

    # ── AI DIFFICULTY (only for non-pvp) ──
    mode_key = GAME_MODES[selected_mode][1]
    if mode_key != "pvp":
        lbl = lbl_font.render("AI DIFFICULTY", True, TEXT_DIM)
        surface.blit(lbl, lbl.get_rect(centerx=WINDOW_WIDTH // 2, y=250))
        for i in range(len(DIFFICULTY_NAMES)):
            btn = buttons[f"diff_{i}"]
            if i == selected_diff:
                btn.color = ACCENT
                btn.hover_color = ACCENT_HOVER
            else:
                btn.color = BUTTON_BG
                btn.hover_color = BUTTON_HOVER
            btn.draw(surface)
    # Descriptive label for selected difficulty
        desc_font = pygame.font.SysFont("Helvetica, Arial", 11)
        elo_map = ["~600 Elo", "~900 Elo", "~1200 Elo",
                   "~1400 Elo", "~1600 Elo", "~1800 Elo"]
        desc = desc_font.render(
            f"{DIFFICULTY_NAMES[selected_diff]} \u2022 {elo_map[selected_diff]}",
            True, TEXT_SECONDARY)
        surface.blit(desc, desc.get_rect(centerx=WINDOW_WIDTH // 2, y=310))

    # ── TIME CONTROL ──
    tc_label_y = 340 if mode_key != "pvp" else 250
    lbl = lbl_font.render("TIME CONTROL", True, TEXT_DIM)
    surface.blit(lbl, lbl.get_rect(centerx=WINDOW_WIDTH // 2, y=tc_label_y))
    for i in range(len(TIME_CONTROLS)):
        btn = buttons[f"tc_{i}"]
        if mode_key == "pvp":
            # Shift TC buttons up when difficulty is hidden
            orig_y = btn.rect.y
            btn.rect.y = tc_label_y + 22 + (orig_y - 362)
        if i == selected_tc:
            btn.color = ACCENT
            btn.hover_color = ACCENT_HOVER
        else:
            btn.color = BUTTON_BG
            btn.hover_color = BUTTON_HOVER
        btn.draw(surface)
        if mode_key == "pvp":
            btn.rect.y = orig_y  # restore

    # ── Start button ──
    start_y = tc_label_y + 90
    start_btn = buttons["start"]
    if mode_key == "pvp":
        orig_y = start_btn.rect.y
        start_btn.rect.y = start_y
    start_btn.draw(surface)
    if mode_key == "pvp":
        start_btn.rect.y = orig_y

    # ── Stats button ──
    stats_btn = buttons["stats"]
    if mode_key == "pvp":
        orig_y = stats_btn.rect.y
        stats_btn.rect.y = start_y + 60
    stats_btn.draw(surface)
    if mode_key == "pvp":
        stats_btn.rect.y = orig_y

    # ── Footer ──
    ff = pygame.font.SysFont("Helvetica, Arial", 11)
    foot = ff.render("Built-in AI engine \u2022 All standard rules \u2022 Coaching & analysis",
                     True, TEXT_DIM)
    surface.blit(foot, foot.get_rect(centerx=WINDOW_WIDTH // 2,
                                     y=WINDOW_HEIGHT - 30))


# ═══════════════════════════════════════════════════════════
# Player Stats Screen
# ═══════════════════════════════════════════════════════════

def draw_stats_screen(surface, profile, back_btn):
    """Render the player statistics screen."""
    from profile import accuracy, win_rate
    surface.fill(BG_COLOR)

    tf = pygame.font.SysFont("Helvetica, Arial", 36, bold=True)
    title = tf.render("\u2654 Player Statistics", True, TEXT_PRIMARY)
    surface.blit(title, title.get_rect(centerx=WINDOW_WIDTH // 2, y=40))

    cx = WINDOW_WIDTH // 2
    y = 110
    hf = pygame.font.SysFont("Helvetica, Arial", 16, bold=True)
    nf = pygame.font.SysFont("Menlo, Consolas, monospace", 22, bold=True)
    sf = pygame.font.SysFont("Helvetica, Arial", 14)

    gp = profile["games_played"]

    # Card helper
    def card(label, value, ypos, color=TEXT_PRIMARY):
        lt = sf.render(label, True, TEXT_DIM)
        vt = nf.render(str(value), True, color)
        surface.blit(lt, lt.get_rect(centerx=cx, y=ypos))
        surface.blit(vt, vt.get_rect(centerx=cx, y=ypos + 18))
        return ypos + 52

    y = card("Games Played", gp, y)

    # Record
    rec = f"{profile['wins']}W / {profile['losses']}L / {profile['draws']}D"
    y = card("Record", rec, y)
    y = card("Win Rate", f"{win_rate(profile):.1f}%", y, ACCENT)
    y = card("Accuracy", f"{accuracy(profile):.1f}%", y, (90, 200, 120))

    # Move quality
    lbl_font = pygame.font.SysFont("Helvetica, Arial", 12)
    lbl = lbl_font.render("MOVE QUALITY", True, TEXT_DIM)
    surface.blit(lbl, lbl.get_rect(centerx=cx, y=y))
    y += 18
    mf = sf
    cols = [(90, 200, 120), (230, 150, 50), (220, 60, 60)]
    labels = [f"Great: {profile['great_moves']}",
              f"Mistakes: {profile['mistakes']}",
              f"Blunders: {profile['blunders']}"]
    total_w = sum(mf.size(l)[0] for l in labels) + 40
    sx = cx - total_w // 2
    for i, (l, c) in enumerate(zip(labels, cols)):
        t = mf.render(l, True, c)
        surface.blit(t, (sx, y))
        sx += t.get_width() + 20
    y += 35

    # Top openings
    fav = profile.get("favorite_openings", {})
    if fav:
        lbl = lbl_font.render("TOP OPENINGS", True, TEXT_DIM)
        surface.blit(lbl, lbl.get_rect(centerx=cx, y=y))
        y += 20
        sorted_op = sorted(fav.items(), key=lambda x: x[1], reverse=True)[:5]
        for i, (name, count) in enumerate(sorted_op):
            txt = sf.render(f"{i+1}. {name}  ({count} games)", True, TEXT_SECONDARY)
            surface.blit(txt, txt.get_rect(centerx=cx, y=y))
            y += 22

    # Back button
    back_btn.draw(surface)


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
    """Draw pawn-promotion overlay."""
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
