# ============================================================
#  game_manager.py  –  Top-level state machine
#
#  States:
#    MENU → LEVEL1 → QUIZ → LEVEL2 → WIN / GAME_OVER
#
#  The manager owns the player, current level, quiz screen,
#  and drives the API call in a background thread so the
#  game loop never blocks.
# ============================================================

import pygame

from game.constants  import *
from game.player     import Player
from levels.level1   import Level1
from levels.level2   import Level2
from ui.quiz_screen  import QuizScreen
from ui.sprites      import draw_npc
from api.quiz_api    import fetch_question


# ── State labels ────────────────────────────────────────────
ST_MENU      = "menu"
ST_LEVEL1    = "level1"
ST_QUIZ      = "quiz"
ST_LEVEL2    = "level2"
ST_WIN       = "win"
ST_GAMEOVER  = "gameover"
ST_DEATH_WAIT = "death_wait"       # brief pause after dying


class GameManager:

    def __init__(self, screen: pygame.Surface):
        self.screen = screen

        # Fonts (8-bit feel via SysFont monospace)
        self.font_lg = pygame.font.SysFont("Courier",      FONT_LARGE,  bold=True)
        self.font_md = pygame.font.SysFont("Courier",      FONT_MEDIUM, bold=True)
        self.font_sm = pygame.font.SysFont("Courier",      FONT_SMALL,  bold=False)

        self.state       = ST_MENU
        self.player      = None
        self.level       = None
        self.quiz        = QuizScreen(self.font_lg, self.font_md, self.font_sm)
        self.quiz_active = False
        self._death_timer = 0
        self._win_timer   = 0
        self._correct_answer = False
        self._menu_tick   = 0

    # ── public entry points ─────────────────────────────────

    def handle_event(self, event: pygame.event.Event):
        if self.state == ST_MENU:
            if event.type == pygame.KEYDOWN and event.key in (
                pygame.K_RETURN, pygame.K_SPACE
            ):
                self._start_level1()

        elif self.state == ST_LEVEL1:
            if self.quiz_active:
                result = self.quiz.handle_event(event)
                self._process_quiz_result(result)
            else:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self._try_talk_to_npc()

        elif self.state == ST_LEVEL2:
            pass   # no special events; player moves freely

        elif self.state in (ST_WIN, ST_GAMEOVER):
            if event.type == pygame.KEYDOWN and event.key in (
                pygame.K_RETURN, pygame.K_r
            ):
                self._reset()

    def update(self):
        if self.state == ST_LEVEL1:
            self._update_level1()
        elif self.state == ST_LEVEL2:
            self._update_level2()
        elif self.state == ST_DEATH_WAIT:
            self._death_timer -= 1
            if self._death_timer <= 0:
                self._revive_player()
        elif self.state == ST_WIN:
            self._win_timer += 1
        self._menu_tick += 1

    def draw(self):
        s = self.screen
        if self.state == ST_MENU:
            self._draw_menu(s)
        elif self.state == ST_LEVEL1:
            self.level.draw(s, self.player, self.font_md)
            if self.quiz_active:
                self.quiz.draw(s)
        elif self.state == ST_LEVEL2:
            self.level.draw(s, self.player, self.font_md)
        elif self.state == ST_DEATH_WAIT:
            if self.level:
                self.level.draw(s, self.player, self.font_md)
            self._draw_death_flash(s)
        elif self.state == ST_WIN:
            self._draw_win(s)
        elif self.state == ST_GAMEOVER:
            self._draw_gameover(s)

    # ── internals ───────────────────────────────────────────

    def _start_level1(self):
        self.level  = Level1()
        self.player = Player(*self.level.spawn())
        self.quiz.reset()
        self.quiz_active = False
        self.state = ST_LEVEL1

    def _update_level1(self):
        if self.quiz_active:
            return                   # freeze world during quiz

        self.level.update(self.player)
        self.player.update(self.level.platforms, self.level.world_width())

        if self.player.dead:
            self._handle_death()

    def _try_talk_to_npc(self):
        npc = self.level.npc_rect()
        pr  = self.player.rect
        if abs(pr.centerx - npc.centerx) < 180 and not self.quiz_active:
            self.quiz_active = True
            self.quiz.reset()

    def _process_quiz_result(self, result: str | None):
        if result == "loading":
            # Preguntas hardcodeadas: respuesta inmediata, sin red
            try:
                data = fetch_question(self.quiz.selected_topic)
                self.quiz.set_question(data)
            except Exception as exc:
                self.quiz.set_error(str(exc)[:120])
        elif result in ("correct", "wrong") and self.quiz.phase == QuizScreen.PHASE_DONE:
            self._correct_answer = (result == "correct")
            self._go_to_level2()

    def _go_to_level2(self):
        self.level  = Level2(self._correct_answer)
        self.player.revive(*self.level.spawn())
        self.state  = ST_LEVEL2
        self.quiz_active = False

    def _update_level2(self):
        self.level.update(self.player)
        self.player.update(self.level.platforms, self.level.world_width())

        if self.level.won:
            self.state = ST_WIN
            self._win_timer = 0
            return

        if self.player.dead:
            self._handle_death()

    def _handle_death(self):
        if self.player.lives <= 0:
            self.state = ST_GAMEOVER
        else:
            self.state = ST_DEATH_WAIT
            self._death_timer = FPS * 2     # 2-second pause

    def _revive_player(self):
        self.player.revive(*self.level.spawn())
        self.state = ST_LEVEL1 if isinstance(self.level, Level1) else ST_LEVEL2

    def _reset(self):
        self.state = ST_MENU
        self.player = None
        self.level  = None

    # ── drawing helpers ─────────────────────────────────────

    def _draw_menu(self, surf):
        surf.fill(BG_NIGHT)
        # Starfield
        import random
        random.seed(42)
        for _ in range(200):
            sx = random.randint(0, SCREEN_WIDTH)
            sy = random.randint(0, SCREEN_HEIGHT)
            pygame.draw.rect(surf, WHITE, (sx, sy, 2, 2))

        # Title box
        bx, bw, bh = 160, 640, 280
        by = SCREEN_HEIGHT // 2 - 160
        pygame.draw.rect(surf, DARK_GREY,  (bx, by, bw, bh), border_radius=10)
        pygame.draw.rect(surf, YELLOW,     (bx, by, bw, bh), 3, border_radius=10)

        t1 = self.font_lg.render("★  QUIZ  QUEST  ★", True, YELLOW)
        surf.blit(t1, (SCREEN_WIDTH//2 - t1.get_width()//2, by + 24))

        t2 = self.font_md.render("8-BIT ADVENTURE", True, CYAN)
        surf.blit(t2, (SCREEN_WIDTH//2 - t2.get_width()//2, by + 70))

        # Animated NPC preview
        draw_npc(surf, SCREEN_WIDTH//2 - 20, by + 100)

        tips = [
            "FLECHAS / WASD  →  moverse",
            "ESPACIO / W     →  saltar / hablar",
            "A-B-C-D         →  responder",
        ]
        for i, tip in enumerate(tips):
            t = self.font_sm.render(tip, True, LIGHT_GREY)
            surf.blit(t, (SCREEN_WIDTH//2 - t.get_width()//2, by + 192 + i*22))

        # Blink
        if (self._menu_tick // 20) % 2 == 0:
            start_t = self.font_md.render("[ ENTER ]  COMENZAR", True, GREEN)
            surf.blit(start_t, (SCREEN_WIDTH//2 - start_t.get_width()//2, by + bh + 24))

    def _draw_death_flash(self, surf):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        alpha = min(160, self._death_timer * 5)
        overlay.fill((200, 0, 0, alpha))
        surf.blit(overlay, (0, 0))
        msg = self.font_lg.render("☠  PERDISTE UNA VIDA  ☠", True, WHITE)
        surf.blit(msg, (SCREEN_WIDTH//2 - msg.get_width()//2, SCREEN_HEIGHT//2 - 20))
        lives_left = self.font_md.render(
            f"Vidas restantes: {'❤ ' * self.player.lives}", True, RED)
        surf.blit(lives_left, (SCREEN_WIDTH//2 - lives_left.get_width()//2,
                               SCREEN_HEIGHT//2 + 28))

    def _draw_win(self, surf):
        surf.fill(BG_SKY)
        # Confetti-ish dots
        import random
        random.seed(self._win_timer // 3)
        for _ in range(120):
            rx = random.randint(0, SCREEN_WIDTH)
            ry = random.randint(0, SCREEN_HEIGHT)
            rc = random.choice([YELLOW, GREEN, CYAN, ORANGE, WHITE, RED])
            pygame.draw.rect(surf, rc, (rx, ry, 6, 6))

        bx, bw, bh = 180, 600, 240
        by = SCREEN_HEIGHT // 2 - 130
        pygame.draw.rect(surf, DARK_GREY, (bx, by, bw, bh), border_radius=10)
        pygame.draw.rect(surf, GREEN,     (bx, by, bw, bh), 4, border_radius=10)

        t1 = self.font_lg.render("★★★  GANASTE  ★★★", True, YELLOW)
        surf.blit(t1, (SCREEN_WIDTH//2 - t1.get_width()//2, by + 22))

        t2 = self.font_lg.render("¡EL JUEGO ES TUYO!", True, GREEN)
        surf.blit(t2, (SCREEN_WIDTH//2 - t2.get_width()//2, by + 66))

        score_t = self.font_md.render(
            f"PUNTAJE FINAL: {self.player.score:05d}", True, CYAN)
        surf.blit(score_t, (SCREEN_WIDTH//2 - score_t.get_width()//2, by + 116))

        # Green flag graphic
        pole_x = SCREEN_WIDTH//2
        pygame.draw.line(surf, DARK_GREY, (pole_x, by+160), (pole_x, by+220), 4)
        pygame.draw.polygon(surf, GREEN,
                            [(pole_x, by+160), (pole_x+44, by+175), (pole_x, by+192)])

        if (self._win_timer // 20) % 2 == 0:
            r = self.font_md.render("[ ENTER ]  VOLVER AL MENÚ", True, WHITE)
            surf.blit(r, (SCREEN_WIDTH//2 - r.get_width()//2, by + bh + 20))

    def _draw_gameover(self, surf):
        surf.fill(BG_HELL)
        bx, bw, bh = 200, 560, 220
        by = SCREEN_HEIGHT // 2 - 120
        pygame.draw.rect(surf, DARK_GREY, (bx, by, bw, bh), border_radius=10)
        pygame.draw.rect(surf, RED,       (bx, by, bw, bh), 4, border_radius=10)

        t1 = self.font_lg.render("☠  GAME  OVER  ☠", True, RED)
        surf.blit(t1, (SCREEN_WIDTH//2 - t1.get_width()//2, by + 22))

        t2 = self.font_md.render("Te quedaste sin vidas...", True, ORANGE)
        surf.blit(t2, (SCREEN_WIDTH//2 - t2.get_width()//2, by + 72))

        score_t = self.font_md.render(
            f"PUNTAJE: {self.player.score:05d}", True, YELLOW)
        surf.blit(score_t, (SCREEN_WIDTH//2 - score_t.get_width()//2, by + 110))

        r = self.font_md.render("[ ENTER / R ]  REINTENTAR", True, WHITE)
        surf.blit(r, (SCREEN_WIDTH//2 - r.get_width()//2, by + bh + 20))
