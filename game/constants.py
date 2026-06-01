# ============================================================
#  constants.py  –  Global game configuration
#  DO NOT modify during runtime (treat as compile-time consts)
# ============================================================

import pygame

# ── Window ──────────────────────────────────────────────────
SCREEN_WIDTH  = 960
SCREEN_HEIGHT = 540
FPS           = 60
TITLE         = "QUIZ QUEST  |  8-BIT EDITION"

# ── Physics ─────────────────────────────────────────────────
GRAVITY        = 0.6
JUMP_FORCE     = -13
PLAYER_SPEED   = 5
SCROLL_THRESH  = SCREEN_WIDTH // 3     # camera starts scrolling here

# ── Player ──────────────────────────────────────────────────
PLAYER_W = 28
PLAYER_H = 36
MAX_LIVES = 3

# ── Block / platform ────────────────────────────────────────
BLOCK_W = 48
BLOCK_H = 24

# ── Colours (8-bit palette) ──────────────────────────────────
BLACK      = (  0,   0,   0)
WHITE      = (255, 255, 255)
RED        = (200,  30,  30)
GREEN      = ( 34, 177,  76)
BLUE       = ( 30, 100, 200)
YELLOW     = (255, 200,   0)
ORANGE     = (220, 110,  20)
BROWN      = (120,  60,  20)
DARK_BROWN = ( 80,  40,  10)
CYAN       = ( 80, 210, 230)
PURPLE     = (140,  40, 180)
DARK_GREY  = ( 40,  40,  40)
LIGHT_GREY = (180, 180, 180)
SKIN       = (255, 200, 140)
DARK_BLUE  = ( 10,  20,  80)

# Background presets
BG_NIGHT   = ( 10,  10,  40)      # level 1 – night
BG_SKY     = ( 80, 180, 255)      # level 2 correct – sky
BG_HELL    = ( 80,  10,  10)      # level 2 wrong  – inferno

# ── UI ──────────────────────────────────────────────────────
UI_HEIGHT   = 48          # top HUD bar height
FONT_LARGE  = 28
FONT_MEDIUM = 20
FONT_SMALL  = 14

# ── Topics available for the quiz ───────────────────────────
QUIZ_TOPICS = ["Arte", "Música", "Historia"]
