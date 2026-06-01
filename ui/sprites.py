# ============================================================
#  sprites.py  –  Pure-pixel 8-bit art drawing utilities
#  All "sprites" are drawn procedurally with pygame.draw
# ============================================================

import pygame
from game.constants import *


# ── helpers ─────────────────────────────────────────────────

def _rect(surf, color, x, y, w, h):
    pygame.draw.rect(surf, color, (x, y, w, h))


# ── Player ──────────────────────────────────────────────────

def draw_player(surf, x, y, facing_right=True, frame=0):
    """Draw 8-bit stick-hero (Mario-ish silhouette)."""
    px, py = int(x), int(y)
    # hat
    _rect(surf, RED,      px+6,  py,    16, 6)
    _rect(surf, RED,      px+2,  py+6,  24, 4)
    # face
    _rect(surf, SKIN,     px+4,  py+10, 20, 12)
    # eyes
    _rect(surf, BLACK,    px+8,  py+13, 4,  4)
    _rect(surf, BLACK,    px+16, py+13, 4,  4)
    # moustache
    _rect(surf, DARK_BROWN, px+6, py+19, 16, 3)
    # body
    _rect(surf, BLUE,     px+4,  py+22, 20, 10)
    # overalls belt
    _rect(surf, DARK_BROWN, px+4, py+22, 20, 3)
    # legs
    _rect(surf, RED,      px+4,  py+32, 8,  4)
    _rect(surf, RED,      px+16, py+32, 8,  4)
    # shoes
    _rect(surf, DARK_BROWN, px+2, py+35, 10, 4) if facing_right else \
        _rect(surf, DARK_BROWN, px+16, py+35, 10, 4)
    _rect(surf, DARK_BROWN, px+16, py+35, 10, 4) if facing_right else \
        _rect(surf, DARK_BROWN, px+2,  py+35, 10, 4)


# ── NPC / Question character ─────────────────────────────────

def draw_npc(surf, x, y):
    """Draw a wizard-style NPC."""
    px, py = int(x), int(y)
    # hat (pointy)
    points = [(px+20, py), (px+6, py+18), (px+34, py+18)]
    pygame.draw.polygon(surf, PURPLE, points)
    _rect(surf, PURPLE,   px+4,  py+18, 32, 6)
    # star on hat
    _rect(surf, YELLOW,   px+17, py+8,  6,  6)
    # face
    _rect(surf, SKIN,     px+8,  py+24, 24, 16)
    # eyes
    _rect(surf, BLACK,    px+13, py+28, 4,  4)
    _rect(surf, BLACK,    px+23, py+28, 4,  4)
    # beard
    _rect(surf, WHITE,    px+6,  py+37, 28, 6)
    _rect(surf, WHITE,    px+10, py+43, 20, 4)
    # robe
    _rect(surf, PURPLE,   px+4,  py+40, 32, 18)
    # staff
    _rect(surf, BROWN,    px+38, py+20, 4,  38)
    _rect(surf, YELLOW,   px+36, py+16, 8,  8)


# ── Ground block ────────────────────────────────────────────

def draw_ground_block(surf, x, y, w=BLOCK_W, h=BLOCK_H):
    _rect(surf, BROWN,      x,   y,   w,   h)
    _rect(surf, DARK_BROWN, x,   y+h-4, w, 4)
    _rect(surf, (160, 90, 30), x+1, y+1, w-2, 4)  # highlight


def draw_brick(surf, x, y, w=BLOCK_W, h=BLOCK_H):
    _rect(surf, ORANGE,     x,   y,   w,   h)
    _rect(surf, DARK_BROWN, x,   y,   w,   2)
    _rect(surf, DARK_BROWN, x,   y,   2,   h)
    _rect(surf, DARK_BROWN, x,   y+h//2, w, 2)
    _rect(surf, DARK_BROWN, x+w//2, y+h//2, 2, h//2)


def draw_flag(surf, x, y, color=GREEN):
    """Draw a small flag (goal)."""
    pole_x = x + 4
    pygame.draw.line(surf, DARK_GREY, (pole_x, y-60), (pole_x, y+4), 4)
    points = [(pole_x, y-60), (pole_x+28, y-48), (pole_x, y-36)]
    pygame.draw.polygon(surf, color, points)
    # "WIN" text drawn by level, not here


# ── HUD ─────────────────────────────────────────────────────

def draw_hud(surf, lives, score, level_name, font):
    pygame.draw.rect(surf, DARK_GREY, (0, 0, SCREEN_WIDTH, UI_HEIGHT))
    pygame.draw.line(surf, YELLOW, (0, UI_HEIGHT), (SCREEN_WIDTH, UI_HEIGHT), 2)

    # Hearts / lives
    heart_text = font.render("❤ " * lives, True, RED)
    surf.blit(heart_text, (10, 12))

    # Score
    score_text = font.render(f"SCORE: {score:05d}", True, YELLOW)
    surf.blit(score_text, (SCREEN_WIDTH//2 - score_text.get_width()//2, 12))

    # Level
    lvl_text = font.render(level_name, True, WHITE)
    surf.blit(lvl_text, (SCREEN_WIDTH - lvl_text.get_width() - 12, 12))


# ── Stars (background decoration) ───────────────────────────

def draw_stars(surf, star_positions):
    for (sx, sy, size) in star_positions:
        pygame.draw.rect(surf, WHITE, (sx, sy, size, size))


# ── Clouds ──────────────────────────────────────────────────

def draw_cloud(surf, x, y, color=(220, 220, 255)):
    for dx, dy, r in [(0,0,18),(20,-8,22),(40,0,18),(60,-4,16)]:
        pygame.draw.circle(surf, color, (x+dx, y+dy), r)


# ── Flame (hell decoration) ──────────────────────────────────

def draw_flame(surf, x, y, frame=0):
    colors = [RED, ORANGE, YELLOW]
    for i, (dx, h) in enumerate([(0,24),(6,32),(12,20),(18,28)]):
        c = colors[(i + frame) % 3]
        _rect(surf, c, x+dx, y-h, 6, h)


# ── Coin ────────────────────────────────────────────────────

def draw_coin(surf, x, y, frame=0):
    w = max(4, 16 - abs((frame % 16) - 8) * 2)
    pygame.draw.ellipse(surf, YELLOW, (x + (16-w)//2, y, w, 16))
