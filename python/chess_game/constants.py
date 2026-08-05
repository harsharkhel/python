"""
Constants for the Chess Game — GrandMaster AI edition.
Layout, colors, piece symbols, time controls, AI/coaching constants.
"""

# === Layout ===
SQUARE_SIZE = 80
BOARD_SQUARES = 8
BOARD_PX = SQUARE_SIZE * BOARD_SQUARES  # 640

# Eval bar sits to the left of the board
EVAL_BAR_X = 8
EVAL_BAR_WIDTH = 22

BOARD_X = 50   # Board left edge (shifted right for eval bar + rank labels)
BOARD_Y = 40   # Board top edge

LABEL_FONT_SIZE = 16

PANEL_X = BOARD_X + BOARD_PX + 20       # 710
PANEL_Y = BOARD_Y
PANEL_WIDTH = 280
PANEL_HEIGHT = BOARD_PX                  # 640

CLOCK_HEIGHT = 50
COACH_HEIGHT = 145                       # Coaching info area between clocks

WINDOW_WIDTH = PANEL_X + PANEL_WIDTH + 20   # 1010
WINDOW_HEIGHT = BOARD_Y + BOARD_PX + 45     # 725

# === Colors ===
BG_COLOR = (26, 26, 46)

LIGHT_SQUARE = (240, 217, 181)
DARK_SQUARE = (181, 136, 99)

SELECTED_TINT = (255, 255, 100)
LEGAL_MOVE_COLOR = (100, 200, 100)
LAST_MOVE_TINT = (100, 160, 255)
CHECK_TINT = (255, 50, 50)

PANEL_BG = (30, 30, 52)
PANEL_BORDER = (55, 55, 85)

TEXT_PRIMARY = (230, 230, 240)
TEXT_SECONDARY = (150, 150, 170)
TEXT_DIM = (100, 100, 120)

ACCENT = (90, 130, 255)
ACCENT_HOVER = (120, 155, 255)
DANGER = (255, 70, 70)
SUCCESS = (80, 200, 120)

WHITE_PIECE = (255, 255, 255)
WHITE_PIECE_OUTLINE = (50, 50, 50)
BLACK_PIECE = (40, 40, 40)
BLACK_PIECE_OUTLINE = (200, 200, 200)

CLOCK_BG = (35, 35, 58)
CLOCK_ACTIVE_BG = (45, 55, 75)
CLOCK_LOW_TIME = (255, 60, 60)

BUTTON_BG = (50, 50, 80)
BUTTON_HOVER = (65, 65, 100)
BUTTON_TEXT = (220, 220, 235)

MODAL_BG = (35, 35, 60)

# Move-classification badge colours
CLS_BRILLIANT  = (0, 180, 230)
CLS_GREAT      = (90, 200, 120)
CLS_GOOD       = (160, 200, 120)
CLS_INACCURACY = (230, 200, 60)
CLS_MISTAKE    = (230, 150, 50)
CLS_BLUNDER    = (220, 60, 60)

# === Time Controls ===
TIME_CONTROLS = [
    ("1 min", 60),
    ("3 min", 180),
    ("5 min", 300),
    ("10 min", 600),
    ("30 min", 1800),
    ("\u221e", None),       # ∞ for unlimited
]

# === Game Modes ===
GAME_MODES = [
    ("vs Player", "pvp"),
    ("vs AI",     "pvai"),
    ("Coaching",  "coaching"),
]

DIFFICULTY_NAMES = [
    "Beginner", "Easy", "Medium", "Hard", "Expert", "Master",
]

# === Piece Unicode Symbols ===
PIECE_SYMBOLS = {
    "K": "\u2654", "Q": "\u2655", "R": "\u2656",
    "B": "\u2657", "N": "\u2658", "P": "\u2659",
    "k": "\u265a", "q": "\u265b", "r": "\u265c",
    "b": "\u265d", "n": "\u265e", "p": "\u265f",
}

FILES = "abcdefgh"
RANKS = "87654321"

FPS = 60
