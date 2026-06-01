# ============================================================
#  level1.py  –  LEVEL 1: Night World → reach the wizard NPC
# ============================================================

import pygame
import random
from game.constants import *
from ui.sprites import (
    draw_ground_block, draw_brick, draw_npc,
    draw_hud, draw_stars, draw_coin,
)


# ── Level geometry ──────────────────────────────────────────
WORLD_W = 4800          # total scrollable width

def _build_platforms() -> list[pygame.Rect]:
    plats = []

    # Ground (continuous base with gaps)
    ground_y = SCREEN_HEIGHT - UI_HEIGHT - 24

    # Segments with intentional gaps to jump over
    segments = [
        (0,    480),
        (560,  820),
        (900, 1200),
        (1280, 1600),
        (1680, 2000),
        (2100, 2440),
        (2520, 2900),
        (2980, 3380),
        (3460, 3860),
        (3940, 4800),
    ]
    for sx, ex in segments:
        w = ex - sx
        plats.append(pygame.Rect(sx, ground_y, w, 24))

    # Floating platforms (step-up / step-down patterns)
    floats = [
        (300,  ground_y - 96,  144),
        (500,  ground_y - 160, 96),
        (650,  ground_y - 80,  192),
        (900,  ground_y - 112, 120),
        (1080, ground_y - 192, 96),
        (1200, ground_y - 80,  144),
        (1400, ground_y - 144, 120),
        (1600, ground_y - 80,  168),
        (1800, ground_y - 160, 96),
        (1950, ground_y - 96,  120),
        (2160, ground_y - 128, 144),
        (2350, ground_y - 80,  120),
        (2560, ground_y - 160, 96),
        (2700, ground_y - 112, 144),
        (2900, ground_y - 80,  120),
        (3100, ground_y - 144, 96),
        (3260, ground_y - 80,  168),
        (3500, ground_y - 128, 144),
        (3700, ground_y - 80,  120),
        (3900, ground_y - 160, 96),
        (4100, ground_y - 96,  144),
        (4350, ground_y - 80,  200),
    ]
    for fx, fy, fw in floats:
        plats.append(pygame.Rect(fx, fy, fw, BLOCK_H))

    return plats


def _build_coins(platforms) -> list[dict]:
    coins = []
    ground_y = SCREEN_HEIGHT - UI_HEIGHT - 24
    for plat in platforms:
        if plat.y < ground_y:                 # only floating platforms
            cx = plat.x + plat.width // 2 - 8
            cy = plat.y - 28
            coins.append({"rect": pygame.Rect(cx, cy, 16, 16),
                          "collected": False})
    return coins


class Level1:
    SPAWN_X = 60.0
    SPAWN_Y = float(SCREEN_HEIGHT - UI_HEIGHT - 24 - PLAYER_H - 4)
    NPC_X   = WORLD_W - 180
    NPC_Y   = float(SCREEN_HEIGHT - UI_HEIGHT - 24 - 58)

    def __init__(self):
        self.platforms = _build_platforms()
        self.coins     = _build_coins(self.platforms)
        self.cam_x     = 0
        self.stars     = [
            (random.randint(0, WORLD_W), random.randint(UI_HEIGHT, SCREEN_HEIGHT-80),
             random.choice([1, 1, 1, 2]))
            for _ in range(280)
        ]
        self._coin_frame = 0
        self._frame_tick = 0

    def world_width(self) -> int:
        return WORLD_W

    def spawn(self):
        return self.SPAWN_X, self.SPAWN_Y

    def npc_rect(self) -> pygame.Rect:
        return pygame.Rect(self.NPC_X, self.NPC_Y, 40, 58)

    def update(self, player):
        # Camera follow
        target = player.x - SCREEN_WIDTH // 3
        self.cam_x = max(0, min(target, WORLD_W - SCREEN_WIDTH))

        # Coin collection
        pr = player.rect
        for coin in self.coins:
            if not coin["collected"]:
                if pr.colliderect(coin["rect"]):
                    coin["collected"] = True
                    player.score += 100

        # Animation
        self._frame_tick += 1
        if self._frame_tick >= 6:
            self._frame_tick = 0
            self._coin_frame = (self._coin_frame + 1) % 16

    def draw(self, surf: pygame.Surface, player, font):
        # Background
        surf.fill(BG_NIGHT)
        draw_stars(surf, [
            (sx - self.cam_x // 3, sy, sz)   # parallax
            for sx, sy, sz in self.stars
        ])

        # Moon
        pygame.draw.circle(surf, (240, 240, 200),
                           (SCREEN_WIDTH - 120, 90), 45)
        pygame.draw.circle(surf, BG_NIGHT,
                           (SCREEN_WIDTH - 100, 80), 38)

        cx = self.cam_x

        # Platforms
        for plat in self.platforms:
            px = plat.x - cx
            if -BLOCK_W < px < SCREEN_WIDTH + BLOCK_W:
                ground_y = SCREEN_HEIGHT - UI_HEIGHT - 24
                if plat.y >= ground_y:
                    # draw ground tile by tile
                    for tx in range(plat.x, plat.x + plat.width, BLOCK_W):
                        draw_ground_block(surf, tx - cx, plat.y - UI_HEIGHT,
                                          min(BLOCK_W, plat.x + plat.width - tx),
                                          24)
                else:
                    for tx in range(plat.x, plat.x + plat.width, BLOCK_W):
                        draw_brick(surf, tx - cx, plat.y - UI_HEIGHT,
                                   min(BLOCK_W, plat.x + plat.width - tx),
                                   BLOCK_H)

        # Coins
        for coin in self.coins:
            if not coin["collected"]:
                draw_coin(surf, coin["rect"].x - cx,
                          coin["rect"].y - UI_HEIGHT, self._coin_frame)

        # NPC
        npc_screen_x = self.NPC_X - cx
        if -60 < npc_screen_x < SCREEN_WIDTH + 60:
            draw_npc(surf, npc_screen_x, self.NPC_Y - UI_HEIGHT)
            if abs(player.x - self.NPC_X) < 220:
                tip = font.render("¡Acércate! [ → ]  Hablar: [ ESPACIO ]",
                                  True, YELLOW)
                surf.blit(tip, (SCREEN_WIDTH//2 - tip.get_width()//2,
                                UI_HEIGHT + 12))

        # Player
        player.draw(surf, cx)

        # HUD
        draw_hud(surf, player.lives, player.score, "NIVEL 1 – MUNDO OSCURO", font)

        # Proximity trigger hint arrow
        if player.x > WORLD_W - 600 and player.x < self.NPC_X - 50:
            arr = font.render("→ EL MAGO TE ESPERA →", True, PURPLE)
            surf.blit(arr, (SCREEN_WIDTH//2 - arr.get_width()//2,
                            SCREEN_HEIGHT - 40))
