"""
Player profile — persistent stats tracking across games (JSON file).
"""

import json
import os
from datetime import datetime

PROFILE_PATH = os.path.join(os.path.dirname(__file__), "player_profile.json")

_DEFAULT = {
    "games_played": 0,
    "wins": 0,
    "losses": 0,
    "draws": 0,
    "total_moves": 0,
    "total_cp_loss": 0.0,
    "blunders": 0,
    "mistakes": 0,
    "great_moves": 0,
    "favorite_openings": {},
    "last_played": None,
}


def load():
    """Load the player profile from disk (or return defaults)."""
    if os.path.exists(PROFILE_PATH):
        try:
            with open(PROFILE_PATH, "r") as fh:
                data = json.load(fh)
            profile = dict(_DEFAULT)
            profile.update(data)
            return profile
        except (json.JSONDecodeError, IOError):
            pass
    return dict(_DEFAULT)


def save(profile):
    """Persist the profile to disk."""
    try:
        with open(PROFILE_PATH, "w") as fh:
            json.dump(profile, fh, indent=2)
    except IOError:
        pass


def update_after_game(result, opening_name=None, move_classifications=None):
    """
    Update stats after a game.

    Args:
        result: ``"win"`` | ``"loss"`` | ``"draw"``
        opening_name: recognised opening (may be None)
        move_classifications: list of ``(cls_name, cp_loss)`` tuples
    """
    p = load()
    p["games_played"] += 1

    if result == "win":
        p["wins"] += 1
    elif result == "loss":
        p["losses"] += 1
    else:
        p["draws"] += 1

    if opening_name:
        op = p.get("favorite_openings", {})
        op[opening_name] = op.get(opening_name, 0) + 1
        p["favorite_openings"] = op

    if move_classifications:
        for cls, cpl in move_classifications:
            p["total_moves"] += 1
            p["total_cp_loss"] += cpl
            if cls == "blunder":
                p["blunders"] += 1
            elif cls == "mistake":
                p["mistakes"] += 1
            elif cls in ("great", "brilliant"):
                p["great_moves"] += 1

    p["last_played"] = datetime.now().isoformat()
    save(p)
    return p


def accuracy(profile):
    """Average accuracy percentage (0–100)."""
    if profile["total_moves"] == 0:
        return 0.0
    avg = profile["total_cp_loss"] / profile["total_moves"]
    return round(max(0.0, min(100.0, 100.0 - avg / 2.0)), 1)


def win_rate(profile):
    """Win rate percentage."""
    t = profile["games_played"]
    return round(profile["wins"] / t * 100, 1) if t else 0.0
