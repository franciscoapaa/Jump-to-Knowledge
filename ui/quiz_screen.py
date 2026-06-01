# ============================================================
#  quiz_screen.py  –  In-game quiz overlay (topic select + Q&A)
# ============================================================

import pygame
from game.constants import *


class QuizScreen:
    """
    Two-phase overlay drawn on top of the game surface.

    Phase 1 – TOPIC:  player picks Arte / Música / Historia
    Phase 2 – QUESTION: player types/selects an answer
    """

    PHASE_TOPIC    = "topic"
    PHASE_QUESTION = "question"
    PHASE_RESULT   = "result"
    PHASE_DONE     = "done"

    def __init__(self, font_large, font_med, font_small):
        self.fl = font_large
        self.fm = font_med
        self.fs = font_small
        self.phase        = self.PHASE_TOPIC
        self.selected_topic = None
        self.question_data  = None      # dict from api
        self.answer_correct = False
        self.loading        = False
        self.error_msg      = ""
        self._result_timer  = 0
        self._input_text    = ""        # typed answer (fallback)
        self._selected_opt  = -1        # 0-3 for A-D

    # ── public API ─────────────────────────────────────────
    def reset(self):
        self.__init__(self.fl, self.fm, self.fs)

    def set_question(self, data: dict):
        self.question_data = data
        self.loading = False
        self.phase   = self.PHASE_QUESTION

    def set_error(self, msg: str):
        self.error_msg = msg
        self.loading   = False

    # ── event handling ─────────────────────────────────────
    def handle_event(self, event) -> str | None:
        """
        Returns one of: None (keep going), "loading",
        "correct", "wrong".
        """
        if self.phase == self.PHASE_TOPIC:
            return self._handle_topic(event)
        if self.phase == self.PHASE_QUESTION:
            return self._handle_question(event)
        if self.phase == self.PHASE_RESULT:
            return self._handle_result(event)
        return None

    def _handle_topic(self, event):
        if event.type == pygame.KEYDOWN:
            key_map = {
                pygame.K_1: 0, pygame.K_KP1: 0,
                pygame.K_2: 1, pygame.K_KP2: 1,
                pygame.K_3: 2, pygame.K_KP3: 2,
            }
            if event.key in key_map:
                self.selected_topic = QUIZ_TOPICS[key_map[event.key]]
                self.loading = True
                self.phase   = self.PHASE_QUESTION
                return "loading"
        return None

    def _handle_question(self, event):
        if self.loading or not self.question_data:
            return None
        if event.type == pygame.KEYDOWN:
            key_map = {
                pygame.K_a: 0, pygame.K_1: 0, pygame.K_KP1: 0,
                pygame.K_b: 1, pygame.K_2: 1, pygame.K_KP2: 1,
                pygame.K_c: 2, pygame.K_3: 2, pygame.K_KP3: 2,
                pygame.K_d: 3, pygame.K_4: 3, pygame.K_KP4: 3,
            }
            if event.key in key_map:
                idx = key_map[event.key]
                opts = self.question_data.get("options", [])
                if idx < len(opts):
                    self._selected_opt = idx
                    chosen = opts[idx][3:].strip()   # remove "A) "
                    correct = self.question_data["answer"].strip()
                    self.answer_correct = (
                        chosen.lower() == correct.lower()
                        or correct.lower() in chosen.lower()
                        or chosen.lower() in correct.lower()
                    )
                    self.phase = self.PHASE_RESULT
                    return "correct" if self.answer_correct else "wrong"
        return None

    def _handle_result(self, event):
        if event.type == pygame.KEYDOWN and event.key in (
            pygame.K_RETURN, pygame.K_SPACE
        ):
            self.phase = self.PHASE_DONE
            return "correct" if self.answer_correct else "wrong"
        return None

    # ── drawing ─────────────────────────────────────────────
    def draw(self, surf: pygame.Surface):
        # Dark translucent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 190))
        surf.blit(overlay, (0, 0))

        if self.phase in (self.PHASE_TOPIC, self.PHASE_QUESTION) and self.loading:
            self._draw_loading(surf)
        elif self.phase == self.PHASE_TOPIC:
            self._draw_topic_select(surf)
        elif self.phase == self.PHASE_QUESTION and self.question_data:
            self._draw_question(surf)
        elif self.phase == self.PHASE_RESULT:
            self._draw_result(surf)

        if self.error_msg:
            err = self.fs.render(f"ERROR: {self.error_msg[:80]}", True, RED)
            surf.blit(err, (20, SCREEN_HEIGHT - 30))

    # ── sub-drawers ─────────────────────────────────────────
    def _draw_box(self, surf, x, y, w, h, title=""):
        pygame.draw.rect(surf, DARK_GREY, (x, y, w, h), border_radius=8)
        pygame.draw.rect(surf, YELLOW,    (x, y, w, h), 3, border_radius=8)
        if title:
            t = self.fl.render(title, True, YELLOW)
            surf.blit(t, (x + w//2 - t.get_width()//2, y + 14))

    def _draw_loading(self, surf):
        self._draw_box(surf, 300, 200, 360, 120, "CARGANDO...")
        dots = self.fm.render("Consultando al oráculo...", True, WHITE)
        surf.blit(dots, (SCREEN_WIDTH//2 - dots.get_width()//2, 270))

    def _draw_topic_select(self, surf):
        bx, by, bw, bh = 200, 120, 560, 300
        self._draw_box(surf, bx, by, bw, bh, "★ ELIGE UN TEMA ★")

        npc_lines = [
            "¡Hola, aventurero!",
            "Demuestra tu sabiduría.",
            "Elige un tema:",
        ]
        for i, line in enumerate(npc_lines):
            t = self.fm.render(line, True, CYAN)
            surf.blit(t, (bx + bw//2 - t.get_width()//2, by + 60 + i*26))

        for i, topic in enumerate(QUIZ_TOPICS):
            label = f"[{i+1}]  {topic}"
            color = YELLOW if i == 0 else (WHITE if i == 1 else ORANGE)
            t = self.fl.render(label, True, color)
            surf.blit(t, (bx + bw//2 - t.get_width()//2, by + 170 + i*38))

    def _draw_question(self, surf):
        qd   = self.question_data
        bx, by, bw, bh = 60, 80, 840, 380
        self._draw_box(surf, bx, by, bw, bh,
                       f"★ {self.selected_topic.upper()} ★")

        # question text (word wrap)
        question = qd["question"]
        words = question.split()
        lines, line = [], ""
        for w in words:
            test = line + ("" if not line else " ") + w
            if self.fm.size(test)[0] > bw - 40:
                lines.append(line)
                line = w
            else:
                line = test
        if line:
            lines.append(line)

        for i, ln in enumerate(lines[:4]):
            t = self.fm.render(ln, True, WHITE)
            surf.blit(t, (bx + 20, by + 55 + i * 26))

        # options
        opts = qd.get("options", [])
        key_labels = ["A", "B", "C", "D"]
        colors_opt = [CYAN, GREEN, YELLOW, ORANGE]
        for i, opt in enumerate(opts[:4]):
            label = f"[{key_labels[i]}]  {opt}"
            t = self.fm.render(label[:70], True, colors_opt[i])
            col = bx + 30 if i % 2 == 0 else bx + bw//2
            row = by + 175 + (i // 2) * 40
            surf.blit(t, (col, row))

        hint = self.fs.render("Presioná A / B / C / D para responder", True, LIGHT_GREY)
        surf.blit(hint, (bx + bw//2 - hint.get_width()//2, by + bh - 28))

    def _draw_result(self, surf):
        if self.answer_correct:
            color, msg, emoji = GREEN,  "¡CORRECTO!", "★"
            sub = f"La respuesta era: {self.question_data['answer']}"
        else:
            color, msg, emoji = RED,    "¡INCORRECTO!", "✗"
            sub = f"Respuesta correcta: {self.question_data['answer']}"

        self._draw_box(surf, 220, 160, 520, 220, "")
        big = self.fl.render(f"{emoji}  {msg}  {emoji}", True, color)
        surf.blit(big, (SCREEN_WIDTH//2 - big.get_width()//2, 195))
        s = self.fm.render(sub[:60], True, WHITE)
        surf.blit(s, (SCREEN_WIDTH//2 - s.get_width()//2, 250))
        hint = self.fs.render("[ ENTER / ESPACIO ] para continuar", True, LIGHT_GREY)
        surf.blit(hint, (SCREEN_WIDTH//2 - hint.get_width()//2, 320))
