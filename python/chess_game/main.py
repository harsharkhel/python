"""
GrandMaster AI — Chess Coach & Trainer
Entry point.

Run with:
    python main.py
"""

import sys
import pygame
from constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, FPS,
    TIME_CONTROLS, GAME_MODES, DIFFICULTY_NAMES,
    ACCENT, ACCENT_HOVER, BUTTON_BG, BUTTON_HOVER,
)
from game import Game
from ui import Button, draw_enhanced_menu, draw_stats_screen
import profile as profile_mod


def main():
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.init()

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("\u2654 GrandMaster AI")
    clock = pygame.time.Clock()

    # ── state ──
    state = "menu"                # menu | playing | stats
    game = None
    selected_mode = 1             # default: vs AI
    selected_diff = 2             # default: Medium
    selected_tc = 2               # default: 5 min

    # ── menu buttons ──
    menu_buttons = {}

    # Game mode buttons
    mode_btn_w, mode_btn_h = 130, 42
    mode_gap = 12
    mode_total = len(GAME_MODES) * mode_btn_w + (len(GAME_MODES) - 1) * mode_gap
    mode_sx = (WINDOW_WIDTH - mode_total) // 2
    mode_y = 175
    for i, (label, _) in enumerate(GAME_MODES):
        bx = mode_sx + i * (mode_btn_w + mode_gap)
        menu_buttons[f"mode_{i}"] = Button(
            (bx, mode_y, mode_btn_w, mode_btn_h), label, font_size=15,
        )

    # Difficulty buttons
    diff_btn_w, diff_btn_h = 95, 38
    diff_gap = 8
    diff_total = len(DIFFICULTY_NAMES) * diff_btn_w + \
                 (len(DIFFICULTY_NAMES) - 1) * diff_gap
    diff_sx = (WINDOW_WIDTH - diff_total) // 2
    diff_y = 270
    for i, name in enumerate(DIFFICULTY_NAMES):
        bx = diff_sx + i * (diff_btn_w + diff_gap)
        menu_buttons[f"diff_{i}"] = Button(
            (bx, diff_y, diff_btn_w, diff_btn_h), name, font_size=13,
        )

    # Time-control buttons
    tc_btn_w, tc_btn_h = 95, 42
    tc_gap = 10
    tc_total = len(TIME_CONTROLS) * tc_btn_w + (len(TIME_CONTROLS) - 1) * tc_gap
    tc_sx = (WINDOW_WIDTH - tc_total) // 2
    tc_y = 362
    for i, (label, _) in enumerate(TIME_CONTROLS):
        bx = tc_sx + i * (tc_btn_w + tc_gap)
        menu_buttons[f"tc_{i}"] = Button(
            (bx, tc_y, tc_btn_w, tc_btn_h), label, font_size=15,
        )

    # Start & Stats buttons
    menu_buttons["start"] = Button(
        (WINDOW_WIDTH // 2 - 120, tc_y + 72, 240, 50),
        "Start Game",
        color=ACCENT, hover_color=ACCENT_HOVER,
        font_size=20, border_radius=10,
    )
    menu_buttons["stats"] = Button(
        (WINDOW_WIDTH // 2 - 80, tc_y + 135, 160, 36),
        "Player Stats", font_size=14,
    )

    # Stats-screen back button
    stats_back = Button(
        (WINDOW_WIDTH // 2 - 80, WINDOW_HEIGHT - 70, 160, 40),
        "Back to Menu",
        color=ACCENT, hover_color=ACCENT_HOVER, font_size=15,
    )

    # ── main loop ──
    while True:
        dt = clock.tick(FPS) / 1000.0
        mouse = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # ── MENU ──
            if state == "menu":
                for btn in menu_buttons.values():
                    btn.update(mouse)

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    # Mode selection
                    for i in range(len(GAME_MODES)):
                        if menu_buttons[f"mode_{i}"].is_clicked(event):
                            selected_mode = i

                    # Difficulty selection
                    for i in range(len(DIFFICULTY_NAMES)):
                        if menu_buttons[f"diff_{i}"].is_clicked(event):
                            selected_diff = i

                    # TC selection
                    for i in range(len(TIME_CONTROLS)):
                        if menu_buttons[f"tc_{i}"].is_clicked(event):
                            selected_tc = i

                    # Start
                    if menu_buttons["start"].is_clicked(event):
                        _, mode_key = GAME_MODES[selected_mode]
                        _, secs = TIME_CONTROLS[selected_tc]
                        game = Game(secs, mode=mode_key,
                                    difficulty=selected_diff + 1)
                        state = "playing"

                    # Stats
                    if menu_buttons["stats"].is_clicked(event):
                        state = "stats"

            # ── STATS ──
            elif state == "stats":
                stats_back.update(mouse)
                if stats_back.is_clicked(event):
                    state = "menu"

            # ── PLAYING ──
            elif state == "playing" and game:
                action = game.handle_event(event)
                if action == "menu":
                    state = "menu"
                    game = None
                elif action == "new_game":
                    _, mode_key = GAME_MODES[selected_mode]
                    _, secs = TIME_CONTROLS[selected_tc]
                    game = Game(secs, mode=mode_key,
                                difficulty=selected_diff + 1)

        # Update
        if state == "playing" and game:
            game.update(dt)

        # Draw
        if state == "menu":
            for btn in menu_buttons.values():
                btn.update(mouse)
            draw_enhanced_menu(screen, menu_buttons,
                               selected_mode, selected_diff, selected_tc)

        elif state == "stats":
            stats_back.update(mouse)
            p = profile_mod.load()
            draw_stats_screen(screen, p, stats_back)

        elif state == "playing" and game:
            game.draw(screen)

        pygame.display.flip()


if __name__ == "__main__":
    main()
