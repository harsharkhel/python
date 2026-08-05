"""
Core chess game — GrandMaster AI edition.

Ties together board rendering, chess engine, coaching, clocks,
move log, eval bar, and UI.
"""

import math
import array
import pygame
import chess
from constants import (
    BG_COLOR, BOARD_X, BOARD_Y, BOARD_PX,
    PANEL_X, PANEL_WIDTH, PANEL_Y, PANEL_HEIGHT,
    CLOCK_HEIGHT, CLOCK_BG, CLOCK_ACTIVE_BG, CLOCK_LOW_TIME,
    COACH_HEIGHT,
    PANEL_BG, PANEL_BORDER,
    TEXT_PRIMARY, TEXT_SECONDARY, TEXT_DIM, ACCENT,
    BUTTON_BG, BUTTON_HOVER,
    WINDOW_WIDTH, WINDOW_HEIGHT,
    SQUARE_SIZE,
    EVAL_BAR_X, EVAL_BAR_WIDTH,
)
from board_render import BoardRenderer
from timer import ChessClock
from move_log import MoveLog
from ui import (
    Button, draw_promotion_dialog, draw_game_over, get_promotion_rects,
)
from engine import ChessEngine
from eval_bar import EvalBar
from openings import recognize as recognize_opening
from coach import classify, tip as coach_tip, game_phase, explain_ai_move, format_eval
import profile as profile_mod


def _wrap(text, font, max_w):
    """Word-wrap *text* to fit within *max_w* pixels. Returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        test = (cur + " " + w) if cur else w
        if font.size(test)[0] <= max_w:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


class Game:
    """Full chess game session with board, clocks, AI, and coaching."""

    def __init__(self, time_seconds, mode="pvp", difficulty=3):
        self.board = chess.Board()
        self.clock = ChessClock(time_seconds)
        self.move_log = MoveLog()
        self.renderer = BoardRenderer()

        # Game mode
        self.mode = mode                     # "pvp" | "pvai" | "coaching"
        self.difficulty = difficulty         # 1–6
        self.player_color = chess.WHITE      # Human always plays White for now

        # Selection
        self.selected_square = None
        self.legal_moves = set()
        self.last_move = None

        # State machine: playing | promotion | game_over
        self.state = "playing"
        self.promotion_move = None
        self.result_text = ""
        self.reason_text = ""
        self.move_count = 0

        # AI / Coaching state
        self.engine = ChessEngine() if mode != "pvp" else None
        self.ai_thinking = False

        # Coaching feedback
        self.last_analysis = None          # classification dict
        self.current_eval = 0
        self.coach_tip_text = ""
        self.ai_explanation = ""
        self.opening_info = None           # (name, eco, desc)
        self.move_classifications = []     # for profile tracking

        # Eval bar
        self.eval_bar = None
        if mode != "pvp":
            self.eval_bar = EvalBar(
                EVAL_BAR_X, BOARD_Y, EVAL_BAR_WIDTH, BOARD_PX
            )
            self.current_eval = self.engine.quick_eval(self.board)
            self.eval_bar.set_eval(self.current_eval)

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
        if self.board.is_check():
            return self.board.king(self.board.turn)
        return None

    def _select(self, square):
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

    def _is_human_turn(self):
        """True if the current side is the human player."""
        if self.mode == "pvp":
            return True
        return self.board.turn == self.player_color

    # ── make move ──────────────────────────────────────────

    def _make_move(self, move, is_ai_move=False):
        """Execute *move* and update all state."""
        board_before = self.board.copy()

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

        # Opening recognition
        self.opening_info = recognize_opening(self.board)

        # Quick eval update
        if self.engine:
            self.current_eval = self.engine.quick_eval(self.board)
            if self.eval_bar:
                self.eval_bar.set_eval(self.current_eval)

        # Check for game end
        self._check_end()

        # Trigger AI thinking after human move (in AI modes)
        if (not is_ai_move
                and self.engine
                and self.mode != "pvp"
                and self.state == "playing"
                and not self._is_human_turn()):
            self.ai_thinking = True
            self.ai_explanation = ""
            self.engine.start_thinking(
                self.board, self.difficulty,
                analyze_board=board_before,
                analyze_move_obj=move,
            )

    # ── game-end detection ─────────────────────────────────

    def _check_end(self):
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

        # Update player profile (AI modes only)
        if self.mode != "pvp":
            if "Wins" in result:
                winner = result.split()[0]
                p_name = "White" if self.player_color == chess.WHITE else "Black"
                gr = "win" if winner == p_name else "loss"
            else:
                gr = "draw"
            op_name = self.opening_info[0] if self.opening_info else None
            profile_mod.update_after_game(gr, op_name, self.move_classifications)

    # ── event handling ─────────────────────────────────────

    def handle_event(self, event):
        """
        Process a single pygame event.
        Returns 'menu' | 'new_game' | None.
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
        # Block board clicks while AI is thinking
        if self.ai_thinking:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.resign_btn.is_clicked(event):
                    loser = "White" if self.board.turn == chess.WHITE else "Black"
                    winner = "Black" if loser == "White" else "White"
                    self._end(f"{winner} Wins!", f"{loser} Resigned")
                elif self.new_game_btn.is_clicked(event):
                    return "new_game"
                elif self.menu_btn.is_clicked(event):
                    return "menu"
            return None

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

        # Board click (only on human's turn)
        if not self._is_human_turn():
            return None

        sq = self.renderer.pixel_to_square(event.pos)
        if sq is None:
            return None

        if self.selected_square is not None and sq in self.legal_moves:
            piece = self.board.piece_at(self.selected_square)
            if (piece and piece.piece_type == chess.PAWN
                    and chess.square_rank(sq) in (0, 7)):
                self.promotion_move = chess.Move(self.selected_square, sq)
                self.state = "promotion"
            else:
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
        """Tick clocks, eval bar, and process AI results."""
        if self.state == "playing":
            self.clock.update(dt)
            if self.clock.flagged is not None:
                fc = "White" if self.clock.flagged == chess.WHITE else "Black"
                wc = "Black" if fc == "White" else "White"
                self._end(f"{wc} Wins!", f"{fc} ran out of time")

        # Eval bar animation
        if self.eval_bar:
            self.eval_bar.update(dt)

        # AI result polling
        if self.ai_thinking and self.engine and not self.engine.is_thinking():
            result = self.engine.get_result()
            if result:
                self._process_ai_result(result)

    def _process_ai_result(self, result):
        """Handle engine background-thread completion."""
        # 1. Player's move analysis
        if "analysis" in result:
            a = result["analysis"]
            key, lbl, sym, col = classify(a["cp_loss"])
            self.last_analysis = {
                "key": key, "label": lbl, "symbol": sym,
                "color": col, "cp_loss": a["cp_loss"],
                "best_move": a["best_move"],
            }
            phase = game_phase(self.board)
            self.coach_tip_text = coach_tip(phase, key)
            self.move_classifications.append((key, a["cp_loss"]))

        # 2. Update eval
        if "eval" in result:
            self.current_eval = result["eval"]
            if self.eval_bar:
                self.eval_bar.set_eval(self.current_eval)

        # 3. Execute AI's move
        if "ai" in result and result["ai"].get("move") is not None:
            if self.state == "playing":
                ai_move = result["ai"]["move"]
                board_before = self.board.copy()
                self._make_move(ai_move, is_ai_move=True)
                self.ai_explanation = explain_ai_move(
                    board_before, ai_move, self.board
                )
                # Refresh eval after AI move
                self.current_eval = self.engine.quick_eval(self.board)
                if self.eval_bar:
                    self.eval_bar.set_eval(self.current_eval)

        self.ai_thinking = False

    # ── drawing ────────────────────────────────────────────

    def _draw_clock(self, surface, color, rect, is_active):
        x, y, w, h = rect
        bg = CLOCK_ACTIVE_BG if is_active and self.state == "playing" else CLOCK_BG
        pygame.draw.rect(surface, bg, rect, border_radius=8)

        if is_active and self.state == "playing":
            pygame.draw.rect(surface, ACCENT, rect, 2, border_radius=8)
        else:
            pygame.draw.rect(surface, PANEL_BORDER, rect, 1, border_radius=8)

        lbl_font = pygame.font.SysFont("Helvetica, Arial", 13)
        sym_font = pygame.font.SysFont("Apple Symbols, Segoe UI Symbol", 18)

        name = "White" if color == chess.WHITE else "Black"
        if self.mode != "pvp":
            if color == self.player_color:
                name += " (You)"
            else:
                name += " (AI)"
        sym = "\u2654" if color == chess.WHITE else "\u265a"

        st = sym_font.render(sym, True, TEXT_PRIMARY)
        surface.blit(st, (x + 8, y + h // 2 - st.get_height() // 2))

        nt = lbl_font.render(name, True, TEXT_PRIMARY)
        surface.blit(nt, (x + 30, y + h // 2 - nt.get_height() // 2))

        time_font = pygame.font.SysFont("Menlo, Consolas, monospace", 22, bold=True)
        time_str = self.clock.format_time(color)
        low = self.clock.is_low_time(color)
        tc = CLOCK_LOW_TIME if low else TEXT_PRIMARY
        if low and is_active and self.state == "playing":
            if (pygame.time.get_ticks() // 500) % 2:
                tc = (255, 120, 120)

        tt = time_font.render(time_str, True, tc)
        surface.blit(tt, tt.get_rect(midright=(x + w - 10, y + h // 2)))

    def _draw_coach_area(self, surface):
        """Draw the coaching feedback panel between the clocks."""
        x = PANEL_X
        y = PANEL_Y + CLOCK_HEIGHT + 8
        w = PANEL_WIDTH
        h = COACH_HEIGHT

        pygame.draw.rect(surface, PANEL_BG, (x, y, w, h), border_radius=8)
        pygame.draw.rect(surface, PANEL_BORDER, (x, y, w, h), 1, border_radius=8)

        tf = pygame.font.SysFont("Helvetica, Arial", 11)
        mf = pygame.font.SysFont("Helvetica, Arial", 13)
        tip_f = pygame.font.SysFont("Helvetica, Arial", 11)

        cy = y + 6

        # Section label
        lbl = tf.render("COACH", True, TEXT_DIM)
        surface.blit(lbl, (x + 8, cy))

        # Eval score (top-right corner of coach box)
        ev_txt = mf.render(format_eval(self.current_eval), True, TEXT_SECONDARY)
        surface.blit(ev_txt, (x + w - ev_txt.get_width() - 10, cy))
        cy += 18

        # Opening name
        if self.opening_info:
            name, eco, _desc = self.opening_info
            ot = mf.render(f"{name} ({eco})", True, ACCENT)
            # Clip if too long
            if ot.get_width() > w - 16:
                ot = mf.render(name, True, ACCENT)
            surface.blit(ot, (x + 8, cy))
            cy += 17

        # AI thinking indicator
        if self.ai_thinking:
            dots = "." * ((pygame.time.get_ticks() // 400) % 4)
            th = mf.render(f"AI thinking{dots}", True, TEXT_SECONDARY)
            surface.blit(th, (x + 8, cy))
            return

        # Last move classification
        if self.last_analysis:
            la = self.last_analysis
            badge_txt = f"{la['symbol']}  {la['label']}"
            bt = mf.render(badge_txt, True, la["color"])
            surface.blit(bt, (x + 8, cy))

            if la["cp_loss"] > 0:
                loss = tf.render(f"(-{la['cp_loss']} cp)", True, TEXT_DIM)
                surface.blit(loss, (x + 8 + bt.get_width() + 6,
                                    cy + 2))
            cy += 17

        # AI explanation (coaching mode)
        if self.ai_explanation and self.mode == "coaching":
            lines = _wrap(self.ai_explanation, tip_f, w - 16)
            for line in lines[:2]:
                lt = tip_f.render(line, True, (180, 200, 230))
                surface.blit(lt, (x + 8, cy))
                cy += 14
            cy += 2

        # Coaching tip
        if self.coach_tip_text:
            lines = _wrap(self.coach_tip_text, tip_f, w - 16)
            for line in lines[:3]:
                lt = tip_f.render(line, True, (160, 160, 185))
                surface.blit(lt, (x + 8, cy))
                cy += 14

    def _draw_panel(self, surface):
        has_coach = self.mode != "pvp"

        # Black clock (top)
        self._draw_clock(
            surface, chess.BLACK,
            (PANEL_X, PANEL_Y, PANEL_WIDTH, CLOCK_HEIGHT),
            self.board.turn == chess.BLACK,
        )

        if has_coach:
            self._draw_coach_area(surface)
            log_y = PANEL_Y + CLOCK_HEIGHT + 8 + COACH_HEIGHT + 8
        else:
            log_y = PANEL_Y + CLOCK_HEIGHT + 10

        # Move log
        log_bottom = PANEL_Y + PANEL_HEIGHT - CLOCK_HEIGHT - 10
        log_h = log_bottom - log_y
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

        # Eval bar (AI modes only)
        if self.eval_bar:
            self.eval_bar.draw(surface)

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
