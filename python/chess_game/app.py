"""
GrandMaster AI — Flask Web Server.

Exposes the chess engine, coaching, and profile systems
as a REST API, served alongside the HTML/JS/CSS frontend.

Run with:
    python app.py
"""

import time
import chess
from flask import Flask, jsonify, request, render_template

from engine import ChessEngine, evaluate
from coach import classify, tip as coach_tip, game_phase, explain_ai_move, format_eval
from openings import recognize as recognize_opening
import profile as profile_mod

app = Flask(__name__)

# ── In-memory game session ─────────────────────────────────

_session = {
    "board": None,
    "engine": None,
    "mode": "pvp",
    "difficulty": 3,
    "player_color": True,          # chess.WHITE
    "time_seconds": 300,
    "clock_white": 300.0,
    "clock_black": 300.0,
    "clock_active": True,          # chess.WHITE
    "clock_running": False,
    "clock_last_tick": None,
    "unlimited": False,
    "flagged": None,
    "last_move": None,
    "move_count": 0,
    "move_log": [],
    "current_eval": 0,
    "last_analysis": None,
    "coach_tip": "",
    "ai_explanation": "",
    "opening_info": None,
    "move_classifications": [],
    "state": "menu",               # menu | playing | game_over
    "result_text": "",
    "reason_text": "",
}


def _tick_clock():
    """Update the active clock based on real elapsed time."""
    s = _session
    if s["unlimited"] or not s["clock_running"] or s["flagged"] is not None:
        return
    now = time.time()
    if s["clock_last_tick"] is not None:
        dt = now - s["clock_last_tick"]
        if s["clock_active"]:
            s["clock_white"] -= dt
            if s["clock_white"] <= 0:
                s["clock_white"] = 0
                s["flagged"] = True  # WHITE flagged
        else:
            s["clock_black"] -= dt
            if s["clock_black"] <= 0:
                s["clock_black"] = 0
                s["flagged"] = False  # BLACK flagged
    s["clock_last_tick"] = now


def _format_time(seconds):
    """Format seconds → MM:SS or M:SS.t string."""
    if seconds is None:
        return "∞"
    t = max(0.0, seconds)
    minutes = int(t) // 60
    secs = int(t) % 60
    if t < 10:
        tenths = int((t % 1) * 10)
        return f"{minutes}:{secs:02d}.{tenths}"
    return f"{minutes}:{secs:02d}"


def _check_end():
    """Check if the game has ended by board rules."""
    s = _session
    board = s["board"]
    if board.is_checkmate():
        w = "White" if board.turn == chess.BLACK else "Black"
        _end_game(f"{w} Wins!", "by Checkmate")
    elif board.is_stalemate():
        _end_game("Draw", "by Stalemate")
    elif board.is_insufficient_material():
        _end_game("Draw", "Insufficient Material")
    elif board.can_claim_threefold_repetition():
        _end_game("Draw", "Threefold Repetition")
    elif board.can_claim_fifty_moves():
        _end_game("Draw", "Fifty-Move Rule")


def _end_game(result, reason):
    """Finalize the game."""
    s = _session
    s["result_text"] = result
    s["reason_text"] = reason
    s["state"] = "game_over"
    s["clock_running"] = False

    # Update profile (AI modes only)
    if s["mode"] != "pvp":
        if "Wins" in result:
            winner = result.split()[0]
            p_name = "White" if s["player_color"] else "Black"
            gr = "win" if winner == p_name else "loss"
        else:
            gr = "draw"
        op_name = s["opening_info"][0] if s["opening_info"] else None
        profile_mod.update_after_game(gr, op_name, s["move_classifications"])


def _make_move(move, is_ai=False):
    """Execute a move and update all session state."""
    s = _session
    board = s["board"]
    board_before = board.copy()

    is_capture = board.is_capture(move)
    is_castle = board.is_castling(move)

    san = board.san(move)
    board.push(move)
    s["move_log"].append(san)
    s["last_move"] = move.uci()
    s["move_count"] += 1

    # Clock
    if s["move_count"] == 1:
        s["clock_running"] = True
        s["clock_last_tick"] = time.time()
    s["clock_active"] = not s["clock_active"]
    s["clock_last_tick"] = time.time()

    # Sound hint for the frontend
    if board.is_check():
        sound = "check"
    elif is_castle:
        sound = "castle"
    elif is_capture:
        sound = "capture"
    else:
        sound = "move"

    # Opening recognition
    s["opening_info"] = recognize_opening(board)

    # Eval update
    if s["engine"]:
        s["current_eval"] = s["engine"].quick_eval(board)

    # Check for end
    _check_end()

    return {
        "san": san,
        "sound": sound,
        "board_before": board_before,
    }


def _get_state():
    """Build the full state dict for the frontend."""
    s = _session
    _tick_clock()

    # Check time-based game end
    if s["flagged"] is not None and s["state"] == "playing":
        fc = "White" if s["flagged"] else "Black"
        wc = "Black" if fc == "White" else "White"
        _end_game(f"{wc} Wins!", f"{fc} ran out of time")

    board = s["board"]
    state = {
        "fen": board.fen() if board else None,
        "state": s["state"],
        "mode": s["mode"],
        "difficulty": s["difficulty"],
        "turn": "white" if board and board.turn == chess.WHITE else "black",
        "player_color": "white" if s["player_color"] else "black",
        "is_check": board.is_check() if board else False,
        "clock_white": _format_time(None if s["unlimited"] else s["clock_white"]),
        "clock_black": _format_time(None if s["unlimited"] else s["clock_black"]),
        "clock_white_raw": None if s["unlimited"] else s["clock_white"],
        "clock_black_raw": None if s["unlimited"] else s["clock_black"],
        "clock_active": "white" if s["clock_active"] else "black",
        "unlimited": s["unlimited"],
        "last_move": s["last_move"],
        "move_log": s["move_log"],
        "current_eval": s["current_eval"],
        "eval_formatted": format_eval(s["current_eval"]),
        "last_analysis": s["last_analysis"],
        "coach_tip": s["coach_tip"],
        "ai_explanation": s["ai_explanation"],
        "opening_info": s["opening_info"],
        "result_text": s["result_text"],
        "reason_text": s["reason_text"],
        "move_count": s["move_count"],
    }

    # Legal moves for the current side (if human's turn)
    if board and s["state"] == "playing":
        legal = []
        for m in board.legal_moves:
            legal.append({
                "from": chess.square_name(m.from_square),
                "to": chess.square_name(m.to_square),
                "promotion": chess.piece_name(m.promotion) if m.promotion else None,
                "uci": m.uci(),
            })
        state["legal_moves"] = legal

        # Check square (king in check)
        if board.is_check():
            king_sq = board.king(board.turn)
            state["check_square"] = chess.square_name(king_sq)
        else:
            state["check_square"] = None
    else:
        state["legal_moves"] = []
        state["check_square"] = None

    return state


# ── Routes ─────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/new", methods=["POST"])
def new_game():
    data = request.get_json(force=True)
    mode = data.get("mode", "pvai")
    difficulty = data.get("difficulty", 3)
    time_secs = data.get("time", 300)  # None for unlimited

    s = _session
    s["board"] = chess.Board()
    s["mode"] = mode
    s["difficulty"] = difficulty
    s["player_color"] = True  # chess.WHITE
    s["time_seconds"] = time_secs
    s["unlimited"] = time_secs is None
    s["clock_white"] = float(time_secs) if time_secs else 0
    s["clock_black"] = float(time_secs) if time_secs else 0
    s["clock_active"] = True  # chess.WHITE starts
    s["clock_running"] = False
    s["clock_last_tick"] = None
    s["flagged"] = None
    s["last_move"] = None
    s["move_count"] = 0
    s["move_log"] = []
    s["current_eval"] = 0
    s["last_analysis"] = None
    s["coach_tip"] = ""
    s["ai_explanation"] = ""
    s["opening_info"] = None
    s["move_classifications"] = []
    s["state"] = "playing"
    s["result_text"] = ""
    s["reason_text"] = ""

    if mode != "pvp":
        s["engine"] = ChessEngine()
        s["current_eval"] = s["engine"].quick_eval(s["board"])
    else:
        s["engine"] = None

    return jsonify(_get_state())


@app.route("/api/state", methods=["GET"])
def get_state():
    if _session["board"] is None:
        return jsonify({"state": "menu"})
    return jsonify(_get_state())


@app.route("/api/move", methods=["POST"])
def make_move():
    s = _session
    board = s["board"]
    if board is None or s["state"] != "playing":
        return jsonify({"error": "No active game"}), 400

    data = request.get_json(force=True)
    from_sq = data.get("from")
    to_sq = data.get("to")
    promotion = data.get("promotion")

    # Parse squares
    try:
        from_square = chess.parse_square(from_sq)
        to_square = chess.parse_square(to_sq)
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid square"}), 400

    # Build the move
    promo_piece = None
    if promotion:
        promo_map = {"queen": chess.QUEEN, "rook": chess.ROOK,
                     "bishop": chess.BISHOP, "knight": chess.KNIGHT}
        promo_piece = promo_map.get(promotion)

    move = chess.Move(from_square, to_square, promotion=promo_piece)

    # Validate
    if move not in board.legal_moves:
        return jsonify({"error": "Illegal move"}), 400

    # Check if this is a human move on human's turn
    is_human_turn = (s["mode"] == "pvp" or board.turn == s["player_color"])
    if not is_human_turn:
        return jsonify({"error": "Not your turn"}), 400

    # Execute the human move
    board_before = board.copy()
    result = _make_move(move)

    response = {
        "sound": result["sound"],
        "ai_move": None,
        "ai_sound": None,
    }

    # If AI mode and game not over, run the engine
    if (s["engine"] and s["mode"] != "pvp"
            and s["state"] == "playing"
            and board.turn != s["player_color"]):

        # 1. Analyse the human's move
        adepth = max(2, min(3, {1: 1, 2: 2, 3: 2, 4: 3, 5: 3, 6: 4}.get(s["difficulty"], 2)))
        analysis = s["engine"].analyze_move(board_before, move, adepth)
        key, lbl, sym, col = classify(analysis["cp_loss"])
        s["last_analysis"] = {
            "key": key, "label": lbl, "symbol": sym,
            "color": list(col), "cp_loss": analysis["cp_loss"],
            "best_move": analysis["best_move"].uci() if analysis["best_move"] else None,
        }
        phase = game_phase(board)
        s["coach_tip"] = coach_tip(phase, key)
        s["move_classifications"].append((key, analysis["cp_loss"]))

        # 2. Compute AI move
        if not board.is_game_over():
            ai_result = s["engine"]._find_best(board, s["difficulty"])
            if ai_result["move"]:
                ai_board_before = board.copy()
                ai_info = _make_move(ai_result["move"], is_ai=True)
                s["ai_explanation"] = explain_ai_move(
                    ai_board_before, ai_result["move"], board
                )
                s["current_eval"] = s["engine"].quick_eval(board)
                response["ai_move"] = ai_result["move"].uci()
                response["ai_sound"] = ai_info["sound"]

        # Update eval
        s["current_eval"] = s["engine"].quick_eval(board)

    response["state"] = _get_state()
    return jsonify(response)


@app.route("/api/resign", methods=["POST"])
def resign():
    s = _session
    if s["board"] is None or s["state"] != "playing":
        return jsonify({"error": "No active game"}), 400

    board = s["board"]
    loser = "White" if board.turn == chess.WHITE else "Black"
    winner = "Black" if loser == "White" else "White"
    _end_game(f"{winner} Wins!", f"{loser} Resigned")

    return jsonify(_get_state())


@app.route("/api/profile", methods=["GET"])
def get_profile():
    p = profile_mod.load()
    return jsonify({
        "games_played": p["games_played"],
        "wins": p["wins"],
        "losses": p["losses"],
        "draws": p["draws"],
        "total_moves": p["total_moves"],
        "great_moves": p["great_moves"],
        "mistakes": p["mistakes"],
        "blunders": p["blunders"],
        "accuracy": profile_mod.accuracy(p),
        "win_rate": profile_mod.win_rate(p),
        "favorite_openings": p.get("favorite_openings", {}),
        "last_played": p.get("last_played"),
    })


if __name__ == "__main__":
    print("♔ GrandMaster AI — Web Edition")
    print("  Open http://localhost:5000 in your browser")
    app.run(debug=True, port=5000)
