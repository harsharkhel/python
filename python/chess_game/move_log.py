"""
Move history panel — displays moves in algebraic notation.
"""

import pygame
from constants import (
    PANEL_BG, PANEL_BORDER, TEXT_PRIMARY, TEXT_SECONDARY, TEXT_DIM, ACCENT,
)


class MoveLog:
    """Scrollable move history in SAN notation."""

    def __init__(self):
        self.moves = []       # List of SAN move strings
        self.scroll_offset = 0
        self.font = None
        self.line_height = 22
        self._max_height = 400  # Updated on each draw()

    def _init_font(self):
        if self.font is None:
            self.font = pygame.font.SysFont("Menlo, Consolas, monospace", 14)

    def add_move(self, san_move):
        """Add a move in SAN notation."""
        self.moves.append(san_move)
        self._auto_scroll()

    def clear(self):
        """Clear all moves."""
        self.moves = []
        self.scroll_offset = 0

    # ── scrolling ──────────────────────────────────────────

    def _auto_scroll(self):
        """Scroll to show the latest moves."""
        move_pairs = (len(self.moves) + 1) // 2
        visible = max(1, (self._max_height - 30) // self.line_height)
        if move_pairs > visible:
            self.scroll_offset = move_pairs - visible

    def handle_scroll(self, direction):
        """Handle mouse wheel (+1 = scroll down, -1 = scroll up)."""
        self.scroll_offset = max(0, self.scroll_offset + direction)
        move_pairs = (len(self.moves) + 1) // 2
        visible = max(1, (self._max_height - 30) // self.line_height)
        self.scroll_offset = min(self.scroll_offset, max(0, move_pairs - visible))

    # ── drawing ────────────────────────────────────────────

    def draw(self, surface, rect):
        """
        Render the move-history panel.

        Args:
            surface: Pygame surface to draw on.
            rect: (x, y, width, height) tuple.
        """
        self._init_font()
        x, y, w, h = rect
        self._max_height = h

        # Background
        pygame.draw.rect(surface, PANEL_BG, (x, y, w, h), border_radius=8)
        pygame.draw.rect(surface, PANEL_BORDER, (x, y, w, h), 1, border_radius=8)

        # Title
        title = self.font.render("Moves", True, TEXT_SECONDARY)
        surface.blit(title, (x + 10, y + 6))

        # Clip area for the move list
        list_y = y + 30
        clip_rect = pygame.Rect(x, list_y, w, h - 30)
        old_clip = surface.get_clip()
        surface.set_clip(clip_rect)

        total_pairs = (len(self.moves) + 1) // 2
        for i in range(self.scroll_offset, total_pairs):
            row_y = list_y + (i - self.scroll_offset) * self.line_height
            if row_y + self.line_height > y + h:
                break

            move_num = i + 1
            white_san = self.moves[i * 2] if i * 2 < len(self.moves) else ""
            black_san = self.moves[i * 2 + 1] if i * 2 + 1 < len(self.moves) else ""

            # Move number
            num_text = self.font.render(f"{move_num}.", True, TEXT_DIM)
            surface.blit(num_text, (x + 10, row_y))

            # White move
            if white_san:
                is_last = i * 2 == len(self.moves) - 1
                color = ACCENT if is_last else TEXT_PRIMARY
                surface.blit(self.font.render(white_san, True, color), (x + 45, row_y))

            # Black move
            if black_san:
                is_last = i * 2 + 1 == len(self.moves) - 1
                color = ACCENT if is_last else TEXT_PRIMARY
                surface.blit(self.font.render(black_san, True, color), (x + 135, row_y))

        surface.set_clip(old_clip)
