"""
Core chess game — ties together board, clock, move log, and UI.
"""

import math
import array
import pygame
import chess
from constants import (
    BG_COLOR, BOARD_X, BOARD_Y, BOARD_PX,
    PANEL_X, PANEL_WIDTH, PANEL_Y, PANEL_HEIGHT,
    CLOCK_HEIGHT, CLOCK_BG, CLOCK_ACTIVE_BG, CLOCK_LOW_TIME,
    PANEL_BG, PANEL_BORDER,
    TEXT_PRIMARY, TEXT_SECONDARY, ACCENT,
    BUTTON_BG, BUTTON_HOVER,
    WINDOW_WIDTH, WINDOW_HEIGHT,
    SQUARE_SIZE,
)
from board_render import BoardRenderer
from timer import ChessClock
from move_log import MoveLog
from ui import (
    Button, draw_promotion_dialog, draw_game_over, get_promotion_rects,
)


class Game:
    """Full chess game session with board, clocks, and move history."""

    def __init__(self, time_seconds):
        self.board = chess.Board()
        self.clock = ChessClock(time_seconds)
        self.move_log = MoveLog()
        self.renderer = BoardRenderer()

        # Selection
        self.selected_square = None
        self.legal_moves = set()       # Destination squares for selected piece
        self.last_move = None

        # State machine: playing | promotion | game_over
        self.state = "playing"
        self.promotion_move = None     # Pending promotion base-move
        self.result_text = ""
        self.reason_text = ""

        self.move_count = 0

        self._init_ui()
        self._init_sounds()

    # ── UI setup ───────────────────────────────────────────

    def _init_ui(self):
        btn_y = BOARD_Y + BOARD_PX + 8
        bw, bh, gap = 82, 28, 8

        self.resign_btn = Button(
            (PANEL_X, btn_y, bw, bh), "Resign",
            color=(100, 40, 40), hover_color=(130, 50, 50), font_size=13,
        )
        self.new_game_btn = Button(
            (PANEL_X + bw + gap, btn_y, bw, bh), "New Game", font_size=13,
        )
        self.menu_btn = Button(
            (PANEL_X + 2 * (bw + gap), btn_y, bw, bh), "Menu", font_size=13,
        )
        self._in_game_btns = [self.resign_btn, self.new_game_btn, self.menu_btn]

        # Game-over dialog buttons
        go_cx = WINDOW_WIDTH // 2
        go_cy = WINDOW_HEIGHT // 2
        self.go_new_btn = Button(
            (go_cx - 140, go_cy + 50, 130, 40), "New Game",
            color=ACCENT, hover_color=(120, 155, 255),
        )
        self.go_menu_btn = Button(
            (go_cx + 10, go_cy + 50, 130, 40), "Main Menu",
        )

    # ── Sounds (synthesized, no external files) ────────────

    def _init_sounds(self):
        self.sounds = {}
        try:
            sr = 44100

            def tone(freq, dur_ms, vol=0.15):
                n = int(sr * dur_ms / 1000)
                buf = array.array("h")
                for i in range(n):
                    t = i / sr
                    fade = min(i, n - i - 1, 600) / 600.0
                    fade = max(fade, 0.0)
                    v = math.sin(2 * math.pi * freq * t) * vol * fade
                    s = int(v * 32767)
                    buf.append(s)   # L
                    buf.append(s)   # R
                return pygame.mixer.Sound(buffer=buf.tobytes())

            self.sounds["move"]      = tone(600, 70)
            self.sounds["capture"]   = tone(400, 110)
            self.sounds["check"]     = tone(800, 140)
            self.sounds["castle"]    = tone(500, 90)
            self.sounds["game_over"] = tone(300, 280)
        except Exception:
            self.sounds = {}

    def _play(self, name):
        snd = self.sounds.get(name)
        if snd:
            try:
                snd.play()
            except Exception:
                pass

    # ── helpers ─────────────────────────────────────────────

    def _check_square(self):
        """Return king square if in check, else None."""
        if self.board.is_check():
            return self.board.king(self.board.turn)
        return None

    def _select(self, square):
        """Select a piece and populate legal destinations."""
        piece = self.board.piece_at(square)
        if piece and piece.color == self.board.turn:
            self.selected_square = square
            self.legal_moves = {
                m.to_square for m in self.board.legal_moves
                if m.from_square == square
            }
        else:
            self.selected_square = None
            self.legal_moves = set()

    def _make_move(self, move):
        """Execute *move* on the board and update all state."""
        is_capture = self.board.is_capture(move)
        is_castle = self.board.is_castling(move)

        san = self.board.san(move)
        self.board.push(move)
        self.move_log.add_move(san)

        self.last_move = move
        self.selected_square = None
        self.legal_moves = set()
        self.move_count += 1

        # Clock management
        if self.move_count == 1:
            self.clock.start()
        self.clock.switch()

        # Sound
        if self.board.is_check():
            self._play("check")
        elif is_castle:
            self._play("castle")
        elif is_capture:
            self._play("capture")
        else:
            self._play("move")

        self._check_end()

    def _check_end(self):
        """Detect checkmate / draw conditions."""
        if self.board.is_checkmate():
            w = "White" if self.board.turn == chess.BLACK else "Black"
            self._end(f"{w} Wins!", "by Checkmate")
        elif self.board.is_stalemate():
            self._end("Draw", "by Stalemate")
        elif self.board.is_insufficient_material():
            self._end("Draw", "Insufficient Material")
        elif self.board.can_claim_threefold_repetition():
            self._end("Draw", "Threefold Repetition")
        elif self.board.can_claim_fifty_moves():
            self._end("Draw", "Fifty-Move Rule")

    def _end(self, result, reason):
        self.result_text = result
        self.reason_text = reason
        self.state = "game_over"
        self.clock.stop()
        self._play("game_over")

    # ── event handling ─────────────────────────────────────

    def handle_event(self, event):
        """
        Process a single pygame event.

        Returns
        -------
        str or None
            ``'menu'`` → go to main menu,
            ``'new_game'`` → start a fresh game,
            ``None`` → no navigation.
        """
        mouse = pygame.mouse.get_pos()
        for b in self._in_game_btns:
            b.update(mouse)

        # ── game over ──
        if self.state == "game_over":
            self.go_new_btn.update(mouse)
            self.go_menu_btn.update(mouse)
            if self.go_new_btn.is_clicked(event):
                return "new_game"
            if self.go_menu_btn.is_clicked(event):
                return "menu"
            return None

        # ── promotion ──
        if self.state == "promotion":
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for rect, pt in get_promotion_rects():
                    if rect.collidepoint(event.pos):
                        move = chess.Move(
                            self.promotion_move.from_square,
                            self.promotion_move.to_square,
                            promotion=pt,
                        )
                        self.state = "playing"
                        self._make_move(move)
                        return None
            return None

        # ── playing ──
        if event.type != pygame.MOUSEBUTTONDOWN:
            if event.type == pygame.MOUSEWHEEL:
                self.move_log.handle_scroll(-event.y)
            return None

        if event.button != 1:
            return None

        # In-game buttons
        if self.resign_btn.is_clicked(event):
            loser = "White" if self.board.turn == chess.WHITE else "Black"
            winner = "Black" if loser == "White" else "White"
            self._end(f"{winner} Wins!", f"{loser} Resigned")
            return None
        if self.new_game_btn.is_clicked(event):
            return "new_game"
        if self.menu_btn.is_clicked(event):
            return "menu"

        # Board click
        sq = self.renderer.pixel_to_square(event.pos)
        if sq is None:
            return None

        if self.selected_square is not None and sq in self.legal_moves:
            piece = self.board.piece_at(self.selected_square)
            # Promotion?
            if (piece and piece.piece_type == chess.PAWN
                    and chess.square_rank(sq) in (0, 7)):
                self.promotion_move = chess.Move(self.selected_square, sq)
                self.state = "promotion"
            else:
                # Find the matching legal move object
                move = None
                for lm in self.board.legal_moves:
                    if (lm.from_square == self.selected_square
                            and lm.to_square == sq):
                        move = lm
                        break
                if move:
                    self._make_move(move)
        else:
            self._select(sq)

        return None

    # ── update ─────────────────────────────────────────────

    def update(self, dt):
        """Tick clocks; detect time-out."""
        if self.state != "playing":
            return
        self.clock.update(dt)
        if self.clock.flagged is not None:
            fc = "White" if self.clock.flagged == chess.WHITE else "Black"
            wc = "Black" if fc == "White" else "White"
            self._end(f"{wc} Wins!", f"{fc} ran out of time")

    # ── drawing ────────────────────────────────────────────

    def _draw_clock(self, surface, color, rect, is_active):
        x, y, w, h = rect
        bg = CLOCK_ACTIVE_BG if is_active and self.state == "playing" else CLOCK_BG
        pygame.draw.rect(surface, bg, rect, border_radius=8)

        if is_active and self.state == "playing":
            pygame.draw.rect(surface, ACCENT, rect, 2, border_radius=8)
        else:
            pygame.draw.rect(surface, PANEL_BORDER, rect, 1, border_radius=8)

        # Player label
        lbl_font = pygame.font.SysFont("Helvetica, Arial", 14)
        sym_font = pygame.font.SysFont("Apple Symbols, Segoe UI Symbol", 20)

        name = "White" if color == chess.WHITE else "Black"
        sym = "\u2654" if color == chess.WHITE else "\u265a"

        st = sym_font.render(sym, True, TEXT_PRIMARY)
        surface.blit(st, (x + 10, y + h // 2 - st.get_height() // 2))

        nt = lbl_font.render(name, True, TEXT_PRIMARY)
        surface.blit(nt, (x + 36, y + h // 2 - nt.get_height() // 2))

        # Time
        time_font = pygame.font.SysFont("Menlo, Consolas, monospace", 26, bold=True)
        time_str = self.clock.format_time(color)
        low = self.clock.is_low_time(color)
        tc = CLOCK_LOW_TIME if low else TEXT_PRIMARY
        if low and is_active and self.state == "playing":
            if (pygame.time.get_ticks() // 500) % 2:
                tc = (255, 120, 120)

        tt = time_font.render(time_str, True, tc)
        surface.blit(tt, tt.get_rect(midright=(x + w - 12, y + h // 2)))

    def _draw_panel(self, surface):
        # Black clock (top)
        self._draw_clock(
            surface, chess.BLACK,
            (PANEL_X, PANEL_Y, PANEL_WIDTH, CLOCK_HEIGHT),
            self.board.turn == chess.BLACK,
        )

        # Move log
        log_y = PANEL_Y + CLOCK_HEIGHT + 10
        log_h = PANEL_HEIGHT - 2 * CLOCK_HEIGHT - 20
        self.move_log.draw(surface, (PANEL_X, log_y, PANEL_WIDTH, log_h))

        # White clock (bottom)
        self._draw_clock(
            surface, chess.WHITE,
            (PANEL_X, PANEL_Y + PANEL_HEIGHT - CLOCK_HEIGHT,
             PANEL_WIDTH, CLOCK_HEIGHT),
            self.board.turn == chess.WHITE,
        )

        # Buttons
        for b in self._in_game_btns:
            b.draw(surface)

    def draw(self, surface):
        """Render the complete game screen."""
        surface.fill(BG_COLOR)

        self.renderer.draw(
            surface, self.board,
            selected=self.selected_square,
            legal_moves=self.legal_moves,
            last_move=self.last_move,
            check_square=self._check_square(),
        )
        self._draw_panel(surface)

        if self.state == "promotion":
            draw_promotion_dialog(surface, self.board.turn)

        if self.state == "game_over":
            draw_game_over(surface, self.result_text, self.reason_text,
                           [self.go_new_btn, self.go_menu_btn])
