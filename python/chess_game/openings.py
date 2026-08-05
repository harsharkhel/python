"""
Opening recognition database.

Maps move sequences to ~45 named openings with ECO codes
and strategic descriptions.
"""

import chess

# (name, eco_code, [uci_moves], strategic_description)
_OPENINGS = [
    # ── e4 replies ────────────────────────────────────────
    ("King's Pawn Opening", "B00", ["e2e4"],
     "Controls the center and opens lines for the queen and bishop."),

    # Italian
    ("Italian Game", "C50",
     ["e2e4", "e7e5", "g1f3", "b8c6", "f1c4"],
     "Classic development. Aim for d4 break, kingside castle."),
    ("Giuoco Piano", "C53",
     ["e2e4", "e7e5", "g1f3", "b8c6", "f1c4", "f8c5"],
     "The 'Quiet Game.' Both sides develop; White aims for d4."),
    ("Two Knights Defense", "C55",
     ["e2e4", "e7e5", "g1f3", "b8c6", "f1c4", "g8f6"],
     "Sharp counterattack. Black develops rapidly and fights for initiative."),

    # Ruy Lopez
    ("Ruy Lopez", "C60",
     ["e2e4", "e7e5", "g1f3", "b8c6", "f1b5"],
     "Pressure on Black's center through the c6-knight."),
    ("Ruy Lopez: Morphy Defense", "C65",
     ["e2e4", "e7e5", "g1f3", "b8c6", "f1b5", "a7a6"],
     "Main line. Black asks the bishop to declare its intentions."),
    ("Ruy Lopez: Berlin Defense", "C65",
     ["e2e4", "e7e5", "g1f3", "b8c6", "f1b5", "g8f6"],
     "Ultra-solid. Often leads to an endgame — the 'Berlin Wall'."),

    # Scotch / Vienna / King's Gambit
    ("Scotch Game", "C45",
     ["e2e4", "e7e5", "g1f3", "b8c6", "d2d4"],
     "Immediate central break. Open, tactical positions."),
    ("Vienna Game", "C25",
     ["e2e4", "e7e5", "b1c3"],
     "Flexible. White prepares f4 or quiet development."),
    ("King's Gambit", "C30",
     ["e2e4", "e7e5", "f2f4"],
     "Romantic gambit! Sacrifice a pawn for rapid attack."),

    # Sicilian
    ("Sicilian Defense", "B20",
     ["e2e4", "c7c5"],
     "Most popular reply to e4. Asymmetric, fighting chess."),
    ("Sicilian: Open", "B32",
     ["e2e4", "c7c5", "g1f3", "b8c6", "d2d4"],
     "Main-line Sicilian. Rich tactical and strategic play."),
    ("Sicilian Najdorf", "B90",
     ["e2e4", "c7c5", "g1f3", "d7d6", "d2d4", "c5d4", "f3d4", "g8f6", "b1c3", "a7a6"],
     "Fischer & Kasparov's weapon. Extremely flexible."),
    ("Sicilian Dragon", "B70",
     ["e2e4", "c7c5", "g1f3", "d7d6", "d2d4", "c5d4", "f3d4", "g8f6", "b1c3", "g7g6"],
     "Fianchetto bishop for powerful long-diagonal counterplay."),
    ("Sicilian Alapin", "B22",
     ["e2e4", "c7c5", "c2c3"],
     "White prepares d4 immediately. Avoids deep Sicilian theory."),

    # French
    ("French Defense", "C00",
     ["e2e4", "e7e6"],
     "Solid. Black locks the center and counterattacks with c5/d5."),
    ("French: Advance", "C02",
     ["e2e4", "e7e6", "d2d4", "d7d5", "e4e5"],
     "White gains space. Black attacks the chain with c5 and f6."),
    ("French: Exchange", "C01",
     ["e2e4", "e7e6", "d2d4", "d7d5", "e4d5"],
     "Symmetric structure. Equal but can be drawish."),
    ("French: Winawer", "C15",
     ["e2e4", "e7e6", "d2d4", "d7d5", "b1c3", "f8b4"],
     "Double-edged. Black provokes weaknesses in White's structure."),

    # Caro-Kann
    ("Caro-Kann Defense", "B10",
     ["e2e4", "c7c6"],
     "Very solid. Black prepares d5 with c6 support."),
    ("Caro-Kann: Advance", "B12",
     ["e2e4", "c7c6", "d2d4", "d7d5", "e4e5"],
     "White gains space. Black targets the base of the pawn chain."),

    # Scandinavian / Pirc / Alekhine / Modern
    ("Scandinavian Defense", "B01",
     ["e2e4", "d7d5"],
     "Direct challenge. After exd5 Qxd5, the queen is exposed early."),
    ("Pirc Defense", "B07",
     ["e2e4", "d7d6", "d2d4", "g8f6", "b1c3", "g7g6"],
     "Hypermodern: let White build a center, then undermine it."),
    ("Alekhine Defense", "B02",
     ["e2e4", "g8f6"],
     "Provocative! Invites pawns forward, then attacks them."),
    ("Modern Defense", "B06",
     ["e2e4", "g7g6"],
     "Flexible. Black delays committing until White shows a plan."),
    ("Philidor Defense", "C41",
     ["e2e4", "e7e5", "g1f3", "d7d6"],
     "Solid but passive. Supports e5 but blocks the dark bishop."),
    ("Petrov Defense", "C42",
     ["e2e4", "e7e5", "g1f3", "g8f6"],
     "Symmetric and solid. Often leads to drawish positions."),

    # ── d4 openings ───────────────────────────────────────
    ("Queen's Pawn Opening", "A40",
     ["d2d4"],
     "Solid, strategic. Controls center and prepares development."),
    ("Queen's Gambit", "D06",
     ["d2d4", "d7d5", "c2c4"],
     "Offer a pawn for central control. One of the oldest openings."),
    ("Queen's Gambit Declined", "D30",
     ["d2d4", "d7d5", "c2c4", "e7e6"],
     "Solid. Black holds d5 and plans a c5 break."),
    ("Queen's Gambit Accepted", "D20",
     ["d2d4", "d7d5", "c2c4", "d5c4"],
     "Black takes the pawn. Plans to return it while developing."),
    ("Slav Defense", "D10",
     ["d2d4", "d7d5", "c2c4", "c7c6"],
     "Solid support for d5. Keeps the light-squared bishop active."),

    # Indian systems
    ("King's Indian Defense", "E60",
     ["d2d4", "g8f6", "c2c4", "g7g6"],
     "Hypermodern. Fianchetto, then strike with e5 or c5."),
    ("Nimzo-Indian Defense", "E20",
     ["d2d4", "g8f6", "c2c4", "e7e6", "b1c3", "f8b4"],
     "Strategic masterpiece. Pin the knight, fight for e4."),
    ("Queen's Indian Defense", "E15",
     ["d2d4", "g8f6", "c2c4", "e7e6", "g1f3", "b7b6"],
     "Quiet, positional. Control e4 via the fianchetto."),
    ("Gr\u00fcnfeld Defense", "D70",
     ["d2d4", "g8f6", "c2c4", "g7g6", "b1c3", "d7d5"],
     "Counter-attack. Concede the center, then destroy it."),
    ("Catalan Opening", "E01",
     ["d2d4", "g8f6", "c2c4", "e7e6", "g2g3"],
     "White fianchettoes for queenside pressure."),
    ("Dutch Defense", "A80",
     ["d2d4", "f7f5"],
     "Aggressive. Fight for e4 immediately, but weakens the king."),

    # London / Trompowsky
    ("London System", "D02",
     ["d2d4", "d7d5", "c1f4"],
     "Solid system. Develop bishop before blocking with e3."),
    ("London System", "D02",
     ["d2d4", "g8f6", "c1f4"],
     "Solid system. Works against many Black setups."),

    # ── Flank openings ────────────────────────────────────
    ("English Opening", "A10",
     ["c2c4"],
     "Flexible, hypermodern. Control d5 from the flank."),
    ("R\u00e9ti Opening", "A09",
     ["g1f3", "d7d5", "c2c4"],
     "Hypermodern. Strike at the center from the flanks."),
    ("Bird's Opening", "A02",
     ["f2f4"],
     "Uncommon. White aims for kingside control."),
]


def recognize(board):
    """
    Identify the opening from *board*'s move history.

    Returns ``(name, eco, description)`` or ``None``.
    Prefers the longest completely-matched opening.
    """
    game_moves = [m.uci() for m in board.move_stack]
    if not game_moves:
        return None

    best = None
    best_len = 0

    for name, eco, moves, desc in _OPENINGS:
        n = len(moves)
        g = len(game_moves)
        if n > g:
            # Opening is longer than the game so far — check partial
            if all(game_moves[i] == moves[i] for i in range(g)):
                if g > best_len:
                    best_len = g
                    best = (name + "...", eco, desc)
            continue
        # Full opening fits inside the game
        if all(game_moves[i] == moves[i] for i in range(n)):
            if n > best_len:
                best_len = n
                best = (name, eco, desc)

    return best
