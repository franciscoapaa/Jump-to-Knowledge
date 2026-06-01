# ============================================================
#  player.py  –  Player entity + physics
# ============================================================

import pygame
from game.constants import *
from ui.sprites import draw_player


class Player:
    """Handles position, velocity, collision and rendering."""

    def __init__(self, x: float, y: float):
        self.x        = float(x)
        self.y        = float(y)
        self.vx       = 0.0
        self.vy       = 0.0
        self.on_ground = False
        self.facing_right = True
        self.lives    = MAX_LIVES
        self.score    = 0
        self.dead     = False      # dead this frame (fell off)
        self._frame   = 0
        self._walk_timer = 0

    # ── rect for collision ──────────────────────────────────
    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(int(self.x), int(self.y), PLAYER_W, PLAYER_H)

    # ── input + physics ────────────────────────────────────
    def update(self, platforms: list, world_width: int):
        keys = pygame.key.get_pressed()

        # Horizontal
        self.vx = 0
        if keys[pygame.K_LEFT]  or keys[pygame.K_a]:
            self.vx = -PLAYER_SPEED
            self.facing_right = False
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vx = PLAYER_SPEED
            self.facing_right = True

        # Jump
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]) \
                and self.on_ground:
            self.vy = JUMP_FORCE
            self.on_ground = False

        # Gravity
        self.vy += GRAVITY
        if self.vy > 18:
            self.vy = 18          # terminal velocity

        # Move X
        self.x += self.vx
        self.x = max(0, min(self.x, world_width - PLAYER_W))
        self._resolve_x(platforms)

        # Move Y
        self.y += self.vy
        self.on_ground = False
        self._resolve_y(platforms)

        # Walk animation
        if self.vx != 0:
            self._walk_timer += 1
            if self._walk_timer >= 8:
                self._frame ^= 1
                self._walk_timer = 0

        # Fell off screen?
        if self.y > SCREEN_HEIGHT + 200:
            self.die()

    def _resolve_x(self, platforms):
        pr = self.rect
        for plat in platforms:
            if pr.colliderect(plat):
                if self.vx > 0:
                    self.x = plat.left - PLAYER_W
                elif self.vx < 0:
                    self.x = plat.right
                self.vx = 0
                pr = self.rect

    def _resolve_y(self, platforms):
        pr = self.rect
        for plat in platforms:
            if pr.colliderect(plat):
                if self.vy > 0:                 # falling
                    self.y = plat.top - PLAYER_H
                    self.on_ground = True
                elif self.vy < 0:               # hitting ceiling
                    self.y = plat.bottom
                self.vy = 0
                pr = self.rect

    def die(self):
        """Lose a life; reset position handled by level."""
        self.lives -= 1
        self.dead = True

    def revive(self, x: float, y: float):
        self.x, self.y = float(x), float(y)
        self.vx = self.vy = 0.0
        self.on_ground = False
        self.dead = False

    # ── draw (world-space, caller does camera offset) ───────
    def draw(self, surf: pygame.Surface, cam_x: int):
        draw_player(surf, self.x - cam_x, self.y - UI_HEIGHT,
                    self.facing_right, self._frame)
