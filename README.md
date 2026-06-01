# QUIZ QUEST — 8-bit Platformer + Trivia
> Plataformer estilo Mario Bros con quiz de IA integrado

---

## Estructura del proyecto

```
mario_quiz/
│
├── main.py                  ← único punto de entrada
│
├── game/
│   ├── constants.py         ← todas las constantes globales
│   ├── player.py            ← entidad jugador + física
│   └── game_manager.py      ← máquina de estados principal
│
├── levels/
│   ├── level1.py            ← Mundo Oscuro (llega al mago)
│   └── level2.py            ← Cielo ☀ o Infierno 🔥 (llega a la bandera)
│
├── ui/
│   ├── sprites.py           ← todo el pixel art procedural
│   └── quiz_screen.py       ← overlay del quiz (selección + respuesta)
│
└── api/
    └── quiz_api.py          ← llamada a OpenAI (aislada, sin pygame)
```

---

## Instalación

```bash
pip install pygame
```

---

## Configuración de la API

```bash
export OPENAI_API_KEY=sk-...          # Linux / macOS
set    OPENAI_API_KEY=sk-...          # Windows CMD
$env:OPENAI_API_KEY = "sk-..."        # Windows PowerShell
```

---

## Ejecutar

```bash
cd mario_quiz
python main.py
```

---

## Controles

| Tecla            | Acción                        |
|------------------|-------------------------------|
| `← →` / `A D`   | Moverse                       |
| `SPACE` / `W`    | Saltar / Hablar con el mago   |
| `A` `B` `C` `D`  | Elegir respuesta del quiz     |
| `1` `2` `3`      | Elegir tema del quiz          |
| `ENTER`          | Confirmar / avanzar           |
| `ESC`            | Salir                         |

---

## Flujo del juego

```
MENÚ
  ↓ [ENTER]
NIVEL 1 – Mundo Oscuro
  · 3 vidas  · plataformas con brechas
  · llegar al mago al final del nivel
  ↓ [ESPACIO cerca del mago]
QUIZ
  · elegir tema: Arte / Música / Historia
  · se genera pregunta vía OpenAI GPT-4o-mini
  · responder A / B / C / D
  ↓
  ┌─ Correcto → NIVEL 2 – CIELO (fondo celeste)
  └─ Incorrecto → NIVEL 2 – INFIERNO (fondo rojo)
  
NIVEL 2 – llegar a la bandera verde
  · morir → perder vida y reiniciar en el nivel
  · sin vidas → GAME OVER
  · llegar a la bandera → ¡GANASTE!
```

---

## Puntuación

- Moneda recogida en nivel 1: **+100 pts**
- Moneda recogida en nivel 2: **+150 pts**
