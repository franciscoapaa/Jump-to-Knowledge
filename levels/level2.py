# ============================================================
#  level2.py  –  LEVEL 2: Sky (correct) or Hell (wrong)
#                 Reach the flag to WIN the game.
# ============================================================

import pygame
import random
from game.constants import *
from ui.sprites import (
    draw_ground_block, draw_brick, draw_flag,
    draw_hud, draw_coin, draw_cloud, draw_flame,
)


WORLD_W = 5200

def _build_platforms(hell: bool) -> list[pygame.Rect]:
    plats  = []
    ground_y = SCREEN_HEIGHT - UI_HEIGHT - 24

    # Ground with wider gaps (harder level)
    segments = [
        (0,    360),
        (440,  760),
        (860,  1140),
        (1260, 1580),
        (1700, 2060),
        (2200, 2580),
        (2700, 3100),
        (3200, 3620),
        (3720, 4180),
        (4300, 5200),
    ]
    for sx, ex in segments:
        plats.append(pygame.Rect(sx, ground_y, ex - sx, 24))

    # Floating platforms – more vertical variation
    floats = [
        (200,  ground_y - 100, 120),
        (380,  ground_y - 170, 96),
        (600,  ground_y - 90,  144),
        (820,  ground_y - 150, 96),
        (1000, ground_y - 80,  168),
        (1200, ground_y - 140, 96),
        (1400, ground_y - 90,  144),
        (1620, ground_y - 170, 96),
        (1840, ground_y - 100, 120),
        (2060, ground_y - 150, 96),
        (2280, ground_y - 90,  168),
        (2520, ground_y - 160, 96),
        (2750, ground_y - 90,  144),
        (2980, ground_y - 140, 120),
        (3200, ground_y - 90,  168),
        (3450, ground_y - 160, 96),
        (3700, ground_y - 90,  144),
        (3960, ground_y - 140, 120),
        (4220, ground_y - 90,  168),
        (4500, ground_y - 160, 96),
        (4750, ground_y - 90,  200),
    ]
    for fx, fy, fw in floats:
        plats.append(pygame.Rect(fx, fy, fw, BLOCK_H))

    return plats


def _build_coins(platforms) -> list[dict]:
    coins = []
    ground_y = SCREEN_HEIGHT - UI_HEIGHT - 24
    for plat in platforms:
        if plat.y < ground_y:
            cx = plat.x + plat.width // 2 - 8
            cy = plat.y - 28
            coins.append({"rect": pygame.Rect(cx, cy, 16, 16),
                          "collected": False})
    return coins


class Level2:
    SPAWN_X = 60.0
    SPAWN_Y = float(SCREEN_HEIGHT - UI_HEIGHT - 24 - PLAYER_H - 4)
    FLAG_X  = WORLD_W - 120
    FLAG_Y  = float(SCREEN_HEIGHT - UI_HEIGHT - 24)

    def __init__(self, correct_answer: bool):
        self.correct  = correct_answer
        self.bg_color = BG_SKY if correct_answer else BG_HELL
        self.platforms = _build_platforms(not correct_answer)
        self.coins     = _build_coins(self.platforms)
        self.cam_x     = 0
        self.won       = False
        self._coin_frame = 0
        self._frame_tick = 0
        self._flame_tick = 0

        # Clouds (sky only)
        self.clouds = [
            (random.randint(0, WORLD_W),
             random.randint(UI_HEIGHT + 10, SCREEN_HEIGHT // 2),
             random.uniform(0.3, 0.8))
            for _ in range(30)
        ]
        # Flames (hell only)
        self.flames = [
            (random.randint(0, WORLD_W - 30),
             SCREEN_HEIGHT - UI_HEIGHT - 24)
            for _ in range(40)
        ]

    def world_width(self) -> int:
        return WORLD_W

    def spawn(self):
        return self.SPAWN_X, self.SPAWN_Y

    def flag_rect(self) -> pygame.Rect:
        return pygame.Rect(self.FLAG_X - 20, self.FLAG_Y - 80, 60, 84)

    def update(self, player):
        target = player.x - SCREEN_WIDTH // 3
        self.cam_x = max(0, min(target, WORLD_W - SCREEN_WIDTH))

        # Coin collection
        pr = player.rect
        for coin in self.coins:
            if not coin["collected"] and pr.colliderect(coin["rect"]):
                coin["collected"] = True
                player.score += 150

        # Flag touch
        if pr.colliderect(self.flag_rect()):
            self.won = True

        # Anim
        self._frame_tick += 1
        if self._frame_tick >= 6:
            self._frame_tick = 0
            self._coin_frame = (self._coin_frame + 1) % 16

        self._flame_tick += 1
        if self._flame_tick >= 10:
            self._flame_tick = 0

    def draw(self, surf: pygame.Surface, player, font):
        surf.fill(self.bg_color)
        cx = self.cam_x

        if self.correct:
            # Clouds
            for cl_x, cl_y, speed in self.clouds:
                draw_cloud(surf, int(cl_x - cx * speed), cl_y)
            # Sun
            pygame.draw.circle(surf, YELLOW,
                               (SCREEN_WIDTH - 90, 80), 50)
            pygame.draw.circle(surf, (255, 230, 100),
                               (SCREEN_WIDTH - 90, 80), 60, 6)
        else:
            # Hell cracks / lava hints
            for i in range(0, SCREEN_WIDTH, 60):
                pygame.draw.line(surf, (140, 0, 0),
                                 (i, SCREEN_HEIGHT - UI_HEIGHT - 24),
                                 (i + 30, SCREEN_HEIGHT - UI_HEIGHT - 44), 2)
            # Flames
            for fx, fy in self.flames:
                sx = fx - cx
                if -30 < sx < SCREEN_WIDTH + 30:
                    draw_flame(surf, sx, fy - UI_HEIGHT,
                               self._flame_tick)

        # Platforms
        ground_y = SCREEN_HEIGHT - UI_HEIGHT - 24
        for plat in self.platforms:
            px = plat.x - cx
            if -BLOCK_W < px < SCREEN_WIDTH + BLOCK_W:
                if plat.y >= ground_y:
                    for tx in range(plat.x, plat.x + plat.width, BLOCK_W):
                        draw_ground_block(surf, tx - cx, plat.y - UI_HEIGHT,
                                          min(BLOCK_W, plat.x + plat.width - tx), 24)
                else:
                    col = CYAN if self.correct else ORANGE
                    for tx in range(plat.x, plat.x + plat.width, BLOCK_W):
                        bx = tx - cx
                        by = plat.y - UI_HEIGHT
                        bw = min(BLOCK_W, plat.x + plat.width - tx)
                        pygame.draw.rect(surf, col,        (bx, by, bw, BLOCK_H))
                        pygame.draw.rect(surf, DARK_BROWN, (bx, by, bw, 2))
                        pygame.draw.rect(surf, DARK_BROWN, (bx, by, 2, BLOCK_H))

        # Coins
        for coin in self.coins:
            if not coin["collected"]:
                draw_coin(surf, coin["rect"].x - cx,
                          coin["rect"].y - UI_HEIGHT, self._coin_frame)

        # Flag (goal)
        flag_sx = self.FLAG_X - cx
        if -60 < flag_sx < SCREEN_WIDTH + 60:
            flag_color = GREEN
            draw_flag(surf, flag_sx, self.FLAG_Y - UI_HEIGHT, flag_color)
            # WIN label on flag
            win_t = font.render("¡META!", True, GREEN)
            surf.blit(win_t, (flag_sx - win_t.get_width()//2 + 16,
                              self.FLAG_Y - UI_HEIGHT - 76))

        # Player
        player.draw(surf, cx)

        # HUD
        lvl_name = "NIVEL 2 – CIELO ★" if self.correct else "NIVEL 2 – INFIERNO ☠"
        draw_hud(surf, player.lives, player.score, lvl_name, font)

        # Banner at top
        banner_color = CYAN if self.correct else RED
        banner_msg = ("¡Respondiste bien! El cielo te espera."
                      if self.correct else
                      "¡Respuesta incorrecta! ¡Sobrevive al infierno!")
        bt = font.render(banner_msg, True, banner_color)
        surf.blit(bt, (SCREEN_WIDTH//2 - bt.get_width()//2, UI_HEIGHT + 10))
