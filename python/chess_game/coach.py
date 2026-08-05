"""
Coaching engine — move classification, tips, and AI-move explanations.
"""

import random
import chess
from engine import MATE_SCORE

# ── Move Classification ─────────────────────────────────────

#  (label, symbol, colour-RGB)
_CLASSES = {
    "brilliant":   ("Brilliant",   "!!",  (0, 180, 230)),
    "great":       ("Great",       "!",   (90, 200, 120)),
    "good":        ("Good",        "\u2713", (160, 200, 120)),
    "inaccuracy":  ("Inaccuracy",  "?!",  (230, 200, 60)),
    "mistake":     ("Mistake",     "?",   (230, 150, 50)),
    "blunder":     ("Blunder",     "??",  (220, 60, 60)),
}


def classify(cp_loss):
    """Return ``(key, label, symbol, colour)`` for the given centipawn loss."""
    if cp_loss <= 10:
        k = "great"
    elif cp_loss <= 30:
        k = "good"
    elif cp_loss <= 100:
        k = "inaccuracy"
    elif cp_loss <= 300:
        k = "mistake"
    else:
        k = "blunder"
    lbl, sym, col = _CLASSES[k]
    return k, lbl, sym, col


# ── Eval Formatting ─────────────────────────────────────────

def format_eval(eval_cp):
    """Format centipawn value for display (e.g. ``+1.2``, ``-M3``)."""
    if abs(eval_cp) >= MATE_SCORE - 100:
        dist = MATE_SCORE - abs(eval_cp)
        return f"M{dist}" if eval_cp > 0 else f"-M{dist}"
    v = eval_cp / 100.0
    return f"+{v:.1f}" if v >= 0 else f"{v:.1f}"


# ── Game Phase ──────────────────────────────────────────────

def game_phase(board):
    """Return ``'opening'``, ``'middlegame'``, or ``'endgame'``."""
    n_moves = len(board.move_stack)
    pieces = sum(1 for sq in chess.SQUARES
                 if (p := board.piece_at(sq)) is not None
                 and p.piece_type not in (chess.KING, chess.PAWN))
    if n_moves < 10 and pieces >= 10:
        return "opening"
    if pieces <= 6:
        return "endgame"
    return "middlegame"


# ── Coaching Tips ───────────────────────────────────────────

_OPENING_TIPS = [
    "Develop knights and bishops toward the center.",
    "Castle early to safeguard your king.",
    "Don't move the same piece twice without a reason.",
    "Control the center with pawns and pieces.",
    "Avoid bringing your queen out too early.",
    "Connect your rooks by completing development.",
]

_MID_TIPS = [
    "Look for tactics: forks, pins, skewers.",
    "Improve your worst-placed piece.",
    "Create a concrete plan before choosing a move.",
    "Consider your opponent's threats first.",
    "Place rooks on open or semi-open files.",
    "Knights love outpost squares (supported by a pawn).",
    "Bishops thrive on open diagonals.",
    "Look for pawn breaks to open the position.",
]

_END_TIPS = [
    "Activate your king — it's a fighting piece now!",
    "Push passed pawns toward promotion.",
    "Rooks belong behind passed pawns.",
    "In K+P endings, opposition is everything.",
    "Centralize your king before anything else.",
    "A rook on the 7th rank is extremely powerful.",
]

_BLUNDER_TIPS = [
    "Check all opponent threats before moving.",
    "Ask: 'Is my piece safe on the new square?'",
    "Look for checks, captures, and threats (CCT).",
    "Use the process of elimination on candidate moves.",
]

_PRAISE = [
    "Nice move!",
    "Well played!",
    "Solid choice.",
    "Good thinking!",
    "Strong move!",
]


def tip(phase, classification):
    """Return a coaching tip relevant to *phase* and *classification*."""
    if classification in ("blunder", "mistake"):
        return random.choice(_BLUNDER_TIPS)

    if classification in ("great", "brilliant", "good"):
        praise = random.choice(_PRAISE)
        pool = {"opening": _OPENING_TIPS,
                "endgame": _END_TIPS}.get(phase, _MID_TIPS)
        return f"{praise} {random.choice(pool)}"

    pool = {"opening": _OPENING_TIPS,
            "endgame": _END_TIPS}.get(phase, _MID_TIPS)
    return random.choice(pool)


# ── AI Move Explanation ─────────────────────────────────────

def explain_ai_move(board_before, move, board_after):
    """
    Generate a brief natural-language explanation of *move*.
    *board_before* is the position before the move.
    """
    parts = []
    san = board_before.san(move)

    if board_before.is_castling(move):
        side = "kingside" if chess.square_file(move.to_square) > 4 else "queenside"
        parts.append(f"Castling {side} to secure the king and connect the rooks.")
    elif board_before.is_capture(move):
        victim = board_before.piece_at(move.to_square)
        if victim:
            vn = chess.piece_name(victim.piece_type).capitalize()
            parts.append(f"Capturing the {vn} to improve the material balance.")
        else:
            parts.append("Capturing en passant — removing the pawn.")
    elif move.promotion:
        parts.append("Promoting the pawn to a Queen!")
    else:
        pc = board_before.piece_at(move.from_square)
        if pc:
            pn = chess.piece_name(pc.piece_type).capitalize()
            if pc.piece_type in (chess.KNIGHT, chess.BISHOP):
                parts.append(f"Developing the {pn} to a more active square.")
            elif pc.piece_type == chess.ROOK:
                parts.append(f"Activating the Rook on a better file.")
            elif pc.piece_type == chess.PAWN:
                parts.append("Advancing a pawn to gain space.")
            elif pc.piece_type == chess.QUEEN:
                parts.append("Repositioning the Queen for more influence.")
            elif pc.piece_type == chess.KING:
                parts.append("Improving the King's position.")

    if board_after.is_check():
        parts.append("Check!")

    return " ".join(parts) if parts else f"Playing {san}."
