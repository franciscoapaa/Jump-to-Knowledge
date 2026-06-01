# ============================================================
#  quiz_api.py  –  Banco de preguntas hardcodeado
#  3 preguntas por tema: Arte, Música, Historia
# ============================================================

import random

QUESTIONS = {
    "Arte": [
        {
            "question": "¿Quién pintó la Mona Lisa?",
            "answer": "Leonardo da Vinci",
            "options": [
                "A) Miguel Ángel",
                "B) Leonardo da Vinci",
                "C) Rafael Sanzio",
                "D) Sandro Botticelli",
            ],
        },
        {
            "question": "¿En qué museo se encuentra 'La noche estrellada' de Van Gogh?",
            "answer": "Museo de Arte Moderno de Nueva York",
            "options": [
                "A) Museo del Louvre",
                "B) Museo del Prado",
                "C) Museo de Arte Moderno de Nueva York",
                "D) Galería Uffizi",
            ],
        },
        {
            "question": "¿Qué artista es conocido por el cubismo y por el cuadro 'Guernica'?",
            "answer": "Pablo Picasso",
            "options": [
                "A) Salvador Dalí",
                "B) Francisco Goya",
                "C) Joan Miró",
                "D) Pablo Picasso",
            ],
        },
    ],
    "Música": [
        {
            "question": "¿Cuántas sinfonías compuso Ludwig van Beethoven?",
            "answer": "9",
            "options": [
                "A) 6",
                "B) 7",
                "C) 9",
                "D) 12",
            ],
        },
        {
            "question": "¿De qué país es originario el género musical del Tango?",
            "answer": "Argentina",
            "options": [
                "A) Brasil",
                "B) España",
                "C) Cuba",
                "D) Argentina",
            ],
        },
        {
            "question": "¿Cómo se llama la banda británica formada por Freddie Mercury?",
            "answer": "Queen",
            "options": [
                "A) The Beatles",
                "B) Queen",
                "C) Led Zeppelin",
                "D) The Rolling Stones",
            ],
        },
    ],
    "Historia": [
        {
            "question": "¿En qué año llegó Cristóbal Colón a América?",
            "answer": "1492",
            "options": [
                "A) 1489",
                "B) 1492",
                "C) 1500",
                "D) 1510",
            ],
        },
        {
            "question": "¿Qué civilización construyó las pirámides de Giza?",
            "answer": "Los egipcios",
            "options": [
                "A) Los romanos",
                "B) Los griegos",
                "C) Los mayas",
                "D) Los egipcios",
            ],
        },
        {
            "question": "¿En qué año comenzó la Primera Guerra Mundial?",
            "answer": "1914",
            "options": [
                "A) 1905",
                "B) 1910",
                "C) 1914",
                "D) 1918",
            ],
        },
    ],
}


def fetch_question(topic: str) -> dict:
    """
    Devuelve una pregunta aleatoria del tema indicado.
    Mantiene la misma interfaz que la versión con OpenAI,
    así el resto del código no necesita cambios.
    """
    preguntas = QUESTIONS.get(topic)
    if not preguntas:
        raise ValueError(f"Tema desconocido: {topic}")
    return random.choice(preguntas)
