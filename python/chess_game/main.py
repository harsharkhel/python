"""
Chess Game — main entry point.

Run with:
    python main.py
"""

import sys
import pygame
from constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, FPS,
    TIME_CONTROLS,
    ACCENT, ACCENT_HOVER, BUTTON_BG, BUTTON_HOVER,
)
from game import Game
from ui import Button, draw_main_menu


def main():
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.init()

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("\u2654 Chess")
    clock = pygame.time.Clock()

    # ── state ──
    state = "menu"          # menu | playing
    game = None
    selected_tc = 2         # default: 5 min

    # ── menu buttons ──
    menu_buttons = {}
    tc_btn_w, tc_btn_h = 110, 48
    tc_gap = 12
    total = len(TIME_CONTROLS) * tc_btn_w + (len(TIME_CONTROLS) - 1) * tc_gap
    start_x = (WINDOW_WIDTH - total) // 2
    tc_y = 240

    for i, (name, _) in enumerate(TIME_CONTROLS):
        bx = start_x + i * (tc_btn_w + tc_gap)
        menu_buttons[f"tc_{i}"] = Button(
            (bx, tc_y, tc_btn_w, tc_btn_h), name, font_size=17,
        )

    menu_buttons["start"] = Button(
        (WINDOW_WIDTH // 2 - 110, tc_y + 90, 220, 52),
        "Start Game",
        color=ACCENT, hover_color=ACCENT_HOVER,
        font_size=20, border_radius=10,
    )

    # ── main loop ──
    while True:
        dt = clock.tick(FPS) / 1000.0
        mouse = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if state == "menu":
                for btn in menu_buttons.values():
                    btn.update(mouse)

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for i in range(len(TIME_CONTROLS)):
                        if menu_buttons[f"tc_{i}"].is_clicked(event):
                            selected_tc = i

                    if menu_buttons["start"].is_clicked(event):
                        _, secs = TIME_CONTROLS[selected_tc]
                        game = Game(secs)
                        state = "playing"

            elif state == "playing" and game:
                action = game.handle_event(event)
                if action == "menu":
                    state = "menu"
                    game = None
                elif action == "new_game":
                    _, secs = TIME_CONTROLS[selected_tc]
                    game = Game(secs)

        # Update
        if state == "playing" and game:
            game.update(dt)

        # Draw
        if state == "menu":
            # keep hover states fresh
            for btn in menu_buttons.values():
                btn.update(mouse)
            draw_main_menu(screen, menu_buttons, selected_tc)
        elif state == "playing" and game:
            game.draw(screen)

        pygame.display.flip()


if __name__ == "__main__":
    main()
