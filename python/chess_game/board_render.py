"""
Board rendering — draws the chess board, pieces, highlights, and labels.
"""

import pygame
import chess
from constants import (
    BOARD_X, BOARD_Y, BOARD_PX, SQUARE_SIZE,
    LIGHT_SQUARE, DARK_SQUARE,
    SELECTED_TINT, LEGAL_MOVE_COLOR, LAST_MOVE_TINT, CHECK_TINT,
    TEXT_SECONDARY, LABEL_FONT_SIZE, FILES,
    PIECE_SYMBOLS, WHITE_PIECE, WHITE_PIECE_OUTLINE,
    BLACK_PIECE, BLACK_PIECE_OUTLINE,
)


class BoardRenderer:
    """Handles drawing the chess board, pieces, and visual highlights."""

    def __init__(self):
        self._piece_font = None
        self._label_font = None
        self._fallback_font = None
        self._piece_cache = {}
        self._use_symbols = True   # False if chess symbols don't render

    # ── fonts ──────────────────────────────────────────────

    def _init_fonts(self):
        if self._piece_font is not None:
            return
        self._piece_font = pygame.font.SysFont(
            "Apple Symbols, Segoe UI Symbol, DejaVu Sans", 54
        )
        self._label_font = pygame.font.SysFont(
            "Helvetica, Arial, sans-serif", LABEL_FONT_SIZE
        )
        self._fallback_font = pygame.font.SysFont(
            "Helvetica, Arial, sans-serif", 40, bold=True
        )

        # Test if the font can render chess symbols
        test = self._piece_font.render("\u2654", True, (255, 255, 255))
        if test.get_width() < 10:
            self._use_symbols = False

    # ── coordinate helpers ─────────────────────────────────

    def square_to_pixel(self, square):
        """Convert a chess square (0–63) → pixel top-left."""
        f = chess.square_file(square)
        r = chess.square_rank(square)
        return BOARD_X + f * SQUARE_SIZE, BOARD_Y + (7 - r) * SQUARE_SIZE

    def pixel_to_square(self, pos):
        """Convert pixel position → chess square (or None)."""
        mx, my = pos
        col = (mx - BOARD_X) // SQUARE_SIZE
        row = (my - BOARD_Y) // SQUARE_SIZE
        if 0 <= col < 8 and 0 <= row < 8:
            return chess.square(col, 7 - row)
        return None

    # ── square drawing ─────────────────────────────────────

    def _draw_square(self, surface, square):
        x, y = self.square_to_pixel(square)
        f = chess.square_file(square)
        r = chess.square_rank(square)
        color = LIGHT_SQUARE if (f + r) % 2 == 1 else DARK_SQUARE
        pygame.draw.rect(surface, color, (x, y, SQUARE_SIZE, SQUARE_SIZE))

    def _draw_highlight(self, surface, square, tint, alpha=80):
        x, y = self.square_to_pixel(square)
        overlay = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
        overlay.fill((*tint, alpha))
        surface.blit(overlay, (x, y))

    def _draw_legal_dot(self, surface, square, board):
        x, y = self.square_to_pixel(square)
        s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
        cx, cy = SQUARE_SIZE // 2, SQUARE_SIZE // 2

        if board.piece_at(square):
            # Ring for capture targets
            pygame.draw.circle(s, (*LEGAL_MOVE_COLOR, 80), (cx, cy),
                               SQUARE_SIZE // 2 - 2, 5)
        else:
            # Dot for empty squares
            pygame.draw.circle(s, (*LEGAL_MOVE_COLOR, 110), (cx, cy), 13)

        surface.blit(s, (x, y))

    # ── piece rendering ────────────────────────────────────

    def _render_piece(self, piece_char):
        if piece_char in self._piece_cache:
            return self._piece_cache[piece_char]

        self._init_fonts()
        is_white = piece_char.isupper()
        main_color = WHITE_PIECE if is_white else BLACK_PIECE
        outline_color = WHITE_PIECE_OUTLINE if is_white else BLACK_PIECE_OUTLINE

        if self._use_symbols:
            symbol = PIECE_SYMBOLS[piece_char]
            font = self._piece_font
        else:
            symbol = piece_char.upper()
            font = self._fallback_font

        size = SQUARE_SIZE + 10
        surf = pygame.Surface((size, size), pygame.SRCALPHA)

        # Outline pass (render offset copies)
        for ox, oy in [(-2, 0), (2, 0), (0, -2), (0, 2),
                        (-1, -1), (1, -1), (-1, 1), (1, 1)]:
            glyph = font.render(symbol, True, outline_color)
            r = glyph.get_rect(center=(size // 2 + ox, size // 2 + oy))
            surf.blit(glyph, r)

        # Main pass
        glyph = font.render(symbol, True, main_color)
        r = glyph.get_rect(center=(size // 2, size // 2))
        surf.blit(glyph, r)

        self._piece_cache[piece_char] = surf
        return surf

    def _draw_piece(self, surface, piece_char, square):
        x, y = self.square_to_pixel(square)
        ps = self._render_piece(piece_char)
        px = x + SQUARE_SIZE // 2 - ps.get_width() // 2
        py = y + SQUARE_SIZE // 2 - ps.get_height() // 2
        surface.blit(ps, (px, py))

    # ── labels ─────────────────────────────────────────────

    def _draw_labels(self, surface):
        self._init_fonts()
        for i in range(8):
            # Rank labels (left side: 8 at top → 1 at bottom)
            rank_str = str(8 - i)
            y = BOARD_Y + i * SQUARE_SIZE + SQUARE_SIZE // 2
            lbl = self._label_font.render(rank_str, True, TEXT_SECONDARY)
            surface.blit(lbl, lbl.get_rect(midright=(BOARD_X - 8, y)))

            # File labels (bottom: a → h)
            file_str = FILES[i]
            x = BOARD_X + i * SQUARE_SIZE + SQUARE_SIZE // 2
            lbl = self._label_font.render(file_str, True, TEXT_SECONDARY)
            surface.blit(lbl, lbl.get_rect(midtop=(x, BOARD_Y + BOARD_PX + 6)))

    # ── public draw ────────────────────────────────────────

    def draw(self, surface, board, selected=None, legal_moves=None,
             last_move=None, check_square=None):
        """
        Draw the full board.

        Args:
            surface: pygame Surface.
            board: chess.Board instance.
            selected: Currently selected square (int) or None.
            legal_moves: Set of legal destination squares.
            last_move: chess.Move of the last move (or None).
            check_square: Square of the king in check (or None).
        """
        if legal_moves is None:
            legal_moves = set()

        # Board shadow / border
        pygame.draw.rect(surface, (15, 15, 30),
                         (BOARD_X - 3, BOARD_Y - 3, BOARD_PX + 6, BOARD_PX + 6),
                         border_radius=4)

        # Squares
        for sq in chess.SQUARES:
            self._draw_square(surface, sq)

        # Last-move highlight
        if last_move:
            self._draw_highlight(surface, last_move.from_square, LAST_MOVE_TINT, 70)
            self._draw_highlight(surface, last_move.to_square, LAST_MOVE_TINT, 70)

        # Selected highlight
        if selected is not None:
            self._draw_highlight(surface, selected, SELECTED_TINT, 100)

        # Check highlight
        if check_square is not None:
            self._draw_highlight(surface, check_square, CHECK_TINT, 120)

        # Legal-move dots
        for sq in legal_moves:
            self._draw_legal_dot(surface, sq, board)

        # Pieces
        for sq in chess.SQUARES:
            piece = board.piece_at(sq)
            if piece:
                self._draw_piece(surface, piece.symbol(), sq)

        # Rank / file labels
        self._draw_labels(surface)
