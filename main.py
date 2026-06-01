#!/usr/bin/env python3
# ============================================================
#  main.py  –  QUIZ QUEST  |  8-bit platformer + trivia
#
#  Usage:
#    export OPENAI_API_KEY=sk-...
#    python main.py
#
#  Controls:
#    ← → / A D    move
#    SPACE / W    jump  |  talk to NPC
#    A-B-C-D      answer quiz options
#    ENTER        confirm / advance
# ============================================================

import sys
import pygame

from game.constants  import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TITLE
from game.game_manager import GameManager


def main() -> None:
    pygame.init()
    pygame.display.set_caption(TITLE)

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock  = pygame.time.Clock()

    manager = GameManager(screen)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            else:
                manager.handle_event(event)

        manager.update()
        manager.draw()
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    main()
