"""
Chess clock with independent countdown timers for both players.
"""

import chess


class ChessClock:
    """Manages two countdown timers, one per player."""

    def __init__(self, time_seconds):
        """
        Args:
            time_seconds: Starting time for each player in seconds,
                         or None for unlimited.
        """
        self.unlimited = time_seconds is None
        self.time = {
            chess.WHITE: float(time_seconds) if time_seconds else 0,
            chess.BLACK: float(time_seconds) if time_seconds else 0,
        }
        self.active = chess.WHITE
        self.running = False
        self.flagged = None  # Which color flagged (ran out of time)

    def start(self):
        """Start the clock."""
        self.running = True

    def stop(self):
        """Stop the clock."""
        self.running = False

    def switch(self):
        """Switch active player (call after each move)."""
        self.active = not self.active

    def update(self, dt):
        """
        Update the active timer.

        Args:
            dt: Delta time in seconds since last update.
        """
        if self.unlimited or not self.running or self.flagged is not None:
            return

        self.time[self.active] -= dt
        if self.time[self.active] <= 0:
            self.time[self.active] = 0
            self.flagged = self.active

    def get_time(self, color):
        """Get remaining time for a color in seconds."""
        if self.unlimited:
            return None
        return max(0.0, self.time[color])

    def format_time(self, color):
        """Get formatted time string MM:SS (or M:SS.t when under 10s)."""
        if self.unlimited:
            return "\u221e"

        t = max(0.0, self.time[color])
        minutes = int(t) // 60
        seconds = int(t) % 60

        if t < 10:
            tenths = int((t % 1) * 10)
            return f"{minutes}:{seconds:02d}.{tenths}"

        return f"{minutes}:{seconds:02d}"

    def is_low_time(self, color, threshold=30):
        """Check if a player is low on time."""
        if self.unlimited:
            return False
        return self.time[color] <= threshold
