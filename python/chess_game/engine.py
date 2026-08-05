"""
Built-in chess AI engine.

Minimax with alpha-beta pruning, piece-square tables, quiescence search,
and adjustable difficulty (Beginner → Master).
"""

import chess
import random
import threading

INF = 30000
MATE_SCORE = 29000

# ── Piece Values (centipawns) ───────────────────────────────

PIECE_VAL = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 0,
}

# ── Piece-Square Tables ────────────────────────────────────
# From White's perspective.  Index 0 = a8, 63 = h1.

PAWN_PST = [
     0,  0,  0,  0,  0,  0,  0,  0,
    50, 50, 50, 50, 50, 50, 50, 50,
    10, 10, 20, 30, 30, 20, 10, 10,
     5,  5, 10, 25, 25, 10,  5,  5,
     0,  0,  0, 20, 20,  0,  0,  0,
     5, -5,-10,  0,  0,-10, -5,  5,
     5, 10, 10,-20,-20, 10, 10,  5,
     0,  0,  0,  0,  0,  0,  0,  0,
]

KNIGHT_PST = [
    -50,-40,-30,-30,-30,-30,-40,-50,
    -40,-20,  0,  0,  0,  0,-20,-40,
    -30,  0, 10, 15, 15, 10,  0,-30,
    -30,  5, 15, 20, 20, 15,  5,-30,
    -30,  0, 15, 20, 20, 15,  0,-30,
    -30,  5, 10, 15, 15, 10,  5,-30,
    -40,-20,  0,  5,  5,  0,-20,-40,
    -50,-40,-30,-30,-30,-30,-40,-50,
]

BISHOP_PST = [
    -20,-10,-10,-10,-10,-10,-10,-20,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -10,  0, 10, 10, 10, 10,  0,-10,
    -10,  5,  5, 10, 10,  5,  5,-10,
    -10,  0, 10, 10, 10, 10,  0,-10,
    -10, 10, 10, 10, 10, 10, 10,-10,
    -10,  5,  0,  0,  0,  0,  5,-10,
    -20,-10,-10,-10,-10,-10,-10,-20,
]

ROOK_PST = [
     0,  0,  0,  0,  0,  0,  0,  0,
     5, 10, 10, 10, 10, 10, 10,  5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
     0,  0,  0,  5,  5,  0,  0,  0,
]

QUEEN_PST = [
    -20,-10,-10, -5, -5,-10,-10,-20,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -10,  0,  5,  5,  5,  5,  0,-10,
     -5,  0,  5,  5,  5,  5,  0, -5,
      0,  0,  5,  5,  5,  5,  0, -5,
    -10,  5,  5,  5,  5,  5,  0,-10,
    -10,  0,  5,  0,  0,  0,  0,-10,
    -20,-10,-10, -5, -5,-10,-10,-20,
]

KING_MID_PST = [
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -20,-30,-30,-40,-40,-30,-30,-20,
    -10,-20,-20,-20,-20,-20,-20,-10,
     20, 20,  0,  0,  0,  0, 20, 20,
     20, 30, 10,  0,  0, 10, 30, 20,
]

KING_END_PST = [
    -50,-40,-30,-20,-20,-30,-40,-50,
    -30,-20,-10,  0,  0,-10,-20,-30,
    -30,-10, 20, 30, 30, 20,-10,-30,
    -30,-10, 30, 40, 40, 30,-10,-30,
    -30,-10, 30, 40, 40, 30,-10,-30,
    -30,-10, 20, 30, 30, 20,-10,-30,
    -30,-30,  0,  0,  0,  0,-30,-30,
    -50,-30,-30,-30,-30,-30,-30,-50,
]

_PST = {
    chess.PAWN:   PAWN_PST,
    chess.KNIGHT: KNIGHT_PST,
    chess.BISHOP: BISHOP_PST,
    chess.ROOK:   ROOK_PST,
    chess.QUEEN:  QUEEN_PST,
    chess.KING:   KING_MID_PST,
}

# ── Difficulty Presets ──────────────────────────────────────

DIFFICULTY = {
    1: {"name": "Beginner", "depth": 1, "noise": 150, "top_n": 5},
    2: {"name": "Easy",     "depth": 2, "noise": 80,  "top_n": 3},
    3: {"name": "Medium",   "depth": 2, "noise": 20,  "top_n": 2},
    4: {"name": "Hard",     "depth": 3, "noise": 0,   "top_n": 1},
    5: {"name": "Expert",   "depth": 3, "noise": 0,   "top_n": 1},
    6: {"name": "Master",   "depth": 4, "noise": 0,   "top_n": 1},
}

MAX_NODES = 120_000        # Safety limit for a single search call


# ── Helpers ─────────────────────────────────────────────────

def _pst_idx(square, is_white):
    """Map a python-chess square to a PST index."""
    r = chess.square_rank(square)
    f = chess.square_file(square)
    return (7 - r) * 8 + f if is_white else r * 8 + f


def _is_endgame(board):
    queens = len(board.pieces(chess.QUEEN, chess.WHITE)) + \
             len(board.pieces(chess.QUEEN, chess.BLACK))
    minor = sum(len(board.pieces(pt, c))
                for pt in (chess.KNIGHT, chess.BISHOP)
                for c in (chess.WHITE, chess.BLACK))
    rooks = len(board.pieces(chess.ROOK, chess.WHITE)) + \
            len(board.pieces(chess.ROOK, chess.BLACK))
    return queens == 0 or (queens <= 1 and rooks + minor <= 2)


# ── Static Evaluation ──────────────────────────────────────

def evaluate(board):
    """
    Evaluate position from White's perspective (centipawns).
    Positive = White advantage.
    """
    if board.is_checkmate():
        return -MATE_SCORE if board.turn == chess.WHITE else MATE_SCORE
    if board.is_stalemate() or board.is_insufficient_material():
        return 0

    endgame = _is_endgame(board)
    score = 0

    # Material + PST
    for sq in chess.SQUARES:
        pc = board.piece_at(sq)
        if pc is None:
            continue
        is_w = pc.color == chess.WHITE
        pt = pc.piece_type
        val = PIECE_VAL[pt]
        pst = KING_END_PST if pt == chess.KING and endgame else _PST[pt]
        val += pst[_pst_idx(sq, is_w)]
        score += val if is_w else -val

    # Bishop pair
    if len(board.pieces(chess.BISHOP, chess.WHITE)) >= 2:
        score += 30
    if len(board.pieces(chess.BISHOP, chess.BLACK)) >= 2:
        score -= 30

    # Doubled-pawn penalty
    for f in range(8):
        fm = chess.BB_FILES[f]
        wp = bin(board.pawns & board.occupied_co[chess.WHITE] & fm).count("1")
        bp = bin(board.pawns & board.occupied_co[chess.BLACK] & fm).count("1")
        if wp > 1:
            score -= 15 * (wp - 1)
        if bp > 1:
            score += 15 * (bp - 1)

    # Isolated-pawn penalty
    for color, sign in ((chess.WHITE, -1), (chess.BLACK, 1)):
        for sq in board.pieces(chess.PAWN, color):
            f = chess.square_file(sq)
            has_neighbor = False
            for af in (f - 1, f + 1):
                if 0 <= af <= 7:
                    if board.pawns & board.occupied_co[color] & chess.BB_FILES[af]:
                        has_neighbor = True
                        break
            if not has_neighbor:
                score += sign * 10

    # Castling-rights bonus
    for color, sign in ((chess.WHITE, 1), (chess.BLACK, -1)):
        if board.has_kingside_castling_rights(color) or \
           board.has_queenside_castling_rights(color):
            score += sign * 15

    return score


# ════════════════════════════════════════════════════════════
# ChessEngine
# ════════════════════════════════════════════════════════════

class ChessEngine:
    """Adjustable-difficulty chess engine with async support."""

    def __init__(self):
        self._thread = None
        self._result = None
        self._nodes = 0

    # ── quick eval ────────────────────────────────────────

    def quick_eval(self, board):
        return evaluate(board)

    # ── move ordering ─────────────────────────────────────

    def _order(self, board):
        def _score(m):
            s = 0
            if board.is_capture(m):
                victim = board.piece_at(m.to_square)
                attacker = board.piece_at(m.from_square)
                vv = PIECE_VAL.get(victim.piece_type, 100) if victim else 100
                av = PIECE_VAL.get(attacker.piece_type, 100) if attacker else 100
                s += 10 * vv - av + 10000
            if m.promotion:
                s += PIECE_VAL.get(m.promotion, 0) + 8000
            return s
        moves = list(board.legal_moves)
        moves.sort(key=_score, reverse=True)
        return moves

    # ── quiescence search ─────────────────────────────────

    def _quiesce(self, board, alpha, beta, qdepth=4):
        stand = evaluate(board)
        if qdepth <= 0:
            return stand

        if board.turn == chess.WHITE:
            if stand >= beta:
                return beta
            alpha = max(alpha, stand)
            for m in board.legal_moves:
                if not board.is_capture(m):
                    continue
                board.push(m)
                val = self._quiesce(board, alpha, beta, qdepth - 1)
                board.pop()
                alpha = max(alpha, val)
                if alpha >= beta:
                    return beta
            return alpha
        else:
            if stand <= alpha:
                return alpha
            beta = min(beta, stand)
            for m in board.legal_moves:
                if not board.is_capture(m):
                    continue
                board.push(m)
                val = self._quiesce(board, alpha, beta, qdepth - 1)
                board.pop()
                beta = min(beta, val)
                if beta <= alpha:
                    return alpha
            return beta

    # ── alpha-beta search ─────────────────────────────────

    def _search(self, board, depth, alpha, beta):
        self._nodes += 1
        if self._nodes > MAX_NODES:
            return evaluate(board)

        if board.is_game_over():
            if board.is_checkmate():
                return -MATE_SCORE if board.turn == chess.WHITE else MATE_SCORE
            return 0

        if depth <= 0:
            return self._quiesce(board, alpha, beta)

        if board.turn == chess.WHITE:
            best = -INF
            for m in self._order(board):
                board.push(m)
                val = self._search(board, depth - 1, alpha, beta)
                board.pop()
                best = max(best, val)
                alpha = max(alpha, val)
                if beta <= alpha:
                    break
            return best
        else:
            best = INF
            for m in self._order(board):
                board.push(m)
                val = self._search(board, depth - 1, alpha, beta)
                board.pop()
                best = min(best, val)
                beta = min(beta, val)
                if beta <= alpha:
                    break
            return best

    # ── find best move (iterative deepening) ──────────────

    def _find_best(self, board, difficulty):
        if board.is_game_over():
            return {"move": None, "eval": evaluate(board),
                    "top_moves": [], "nodes": 0}

        settings = DIFFICULTY[difficulty]
        max_depth = settings["depth"]
        noise = settings["noise"]
        top_n = settings["top_n"]

        self._nodes = 0
        best_scored = []

        for depth in range(1, max_depth + 1):
            scored = []
            for m in self._order(board):
                board.push(m)
                val = self._search(board, depth - 1, -INF, INF)
                board.pop()
                scored.append((m, val))
                if self._nodes > MAX_NODES:
                    break
            if scored:
                best_scored = scored
            if self._nodes > MAX_NODES:
                break

        is_white = board.turn == chess.WHITE
        best_scored.sort(key=lambda x: x[1], reverse=is_white)

        # Add noise for weaker levels
        if noise > 0:
            noisy = [(m, v + random.randint(-noise, noise))
                     for m, v in best_scored]
            noisy.sort(key=lambda x: x[1], reverse=is_white)
            best_scored = noisy

        candidates = best_scored[:min(top_n, len(best_scored))]
        chosen = random.choice(candidates) if candidates else (None, 0)

        return {
            "move": chosen[0] if isinstance(chosen, tuple) else chosen,
            "eval": best_scored[0][1] if best_scored else 0,
            "top_moves": best_scored[:3],
            "nodes": self._nodes,
        }

    # ── move analysis ─────────────────────────────────────

    def analyze_move(self, board, played_move, depth=3):
        """
        Compare *played_move* to the engine's best move.
        *board* must be the position BEFORE the move was made.
        Returns dict with best_move, best_eval, played_eval, cp_loss.
        """
        board = board.copy()
        self._nodes = 0
        is_white = board.turn == chess.WHITE

        scored = []
        for m in self._order(board):
            board.push(m)
            val = self._search(board, depth - 1, -INF, INF)
            board.pop()
            scored.append((m, val))
            if self._nodes > MAX_NODES:
                break

        scored.sort(key=lambda x: x[1], reverse=is_white)

        if not scored:
            return {"best_move": None, "best_eval": 0,
                    "played_eval": 0, "cp_loss": 0, "top_moves": []}

        best_move, best_eval = scored[0]

        played_eval = best_eval
        for m, v in scored:
            if m == played_move:
                played_eval = v
                break

        cp_loss = (best_eval - played_eval) if is_white \
                  else (played_eval - best_eval)
        cp_loss = max(0, cp_loss)

        return {
            "best_move": best_move,
            "best_eval": best_eval,
            "played_eval": played_eval,
            "cp_loss": cp_loss,
            "top_moves": scored[:3],
        }

    # ── async interface ───────────────────────────────────

    def start_thinking(self, board, difficulty,
                       analyze_board=None, analyze_move_obj=None):
        """Launch background thread: analyse prev move + compute AI move."""
        self._result = None
        self._thread = threading.Thread(
            target=self._bg_compute,
            args=(board.copy(), difficulty,
                  analyze_board.copy() if analyze_board else None,
                  analyze_move_obj),
            daemon=True,
        )
        self._thread.start()

    def is_thinking(self):
        return self._thread is not None and self._thread.is_alive()

    def get_result(self):
        if self._thread and not self._thread.is_alive():
            r = self._result
            self._thread = None
            return r
        return None

    def _bg_compute(self, board, difficulty, a_board, a_move):
        result = {}
        # 1. Analyse the previous (human) move
        if a_board is not None and a_move is not None:
            adepth = max(2, min(3, DIFFICULTY[difficulty]["depth"]))
            result["analysis"] = self.analyze_move(a_board, a_move, adepth)
        # 2. Compute AI move
        if not board.is_game_over():
            result["ai"] = self._find_best(board, difficulty)
        # 3. Current eval
        result["eval"] = evaluate(board)
        self._result = result
