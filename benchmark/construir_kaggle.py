"""Genera en kaggle/ un fichero autocontenido por juego y modo, listo para `kaggle b t push`.

    .venv/Scripts/python.exe benchmark/construir_kaggle.py
    kaggle b t push deadline-math-direct -f benchmark/kaggle/deadline-math-direct.py --wait
"""

from pathlib import Path

AQUI = Path(__file__).parent
FUENTE = (AQUI / "deadline_math.py").read_text(encoding="utf-8")
LINEA = 'MODE = "direct"'
NOMBRE = 'name=f"deadline-math-{MODE}"'
JUEGO = 'SET = "standard"'
DESCRIPCION = FUENTE[FUENTE.index("    description=(\n"):FUENTE.index("    ),\n)\ndef deadline_math") + len("    ),\n")]

# Lo que ve quien abre cada task en Kaggle: en inglés, literal y de 255 caracteres como máximo.
MODO = {"direct": "answer-only mode", "reasoned": "reasoning allowed"}
TEMAS = {
    "standard": "Standard set, {modo}. Convert a published contest deadline to the reader's local time: day "
                "rollover, the weeks when the EU and US change clocks on different dates, 12 AM and AoE wording, "
                "non-hour offsets. Ground truth from zoneinfo.",
    "pairs": "Pre-registered paired set, {modo}. 50 trap/control pairs: the same deadline inside and outside the "
             "weeks when the EU and US change clocks on different dates, and durations that do or do not cross a "
             "clock change. Ground truth from zoneinfo.",
    "hard": "Exploratory hard set, {modo}. Convert deadlines to the reader's local time: relative dates, "
            "durations across a clock change, Unix and ISO timestamps, described dates, a traveling reader. "
            "Ground truth from zoneinfo.",
}

assert all(FUENTE.count(x) == 1 for x in (LINEA, NOMBRE, JUEGO, DESCRIPCION)), "faltan MODE, SET, nombre o descripción"
(AQUI / "kaggle").mkdir(exist_ok=True)
for juego in ("standard", "hard", "pairs"):
    for modo in ("direct", "reasoned"):
        nombre = f"deadline-math-{modo}" if juego == "standard" else f"deadline-math-{juego}-{modo}"
        descripcion = TEMAS[juego].format(modo=MODO[modo])
        assert len(descripcion) <= 255, (nombre, len(descripcion))
        destino = AQUI / "kaggle" / f"{nombre}.py"
        # El CLI lee el nombre del decorador sin ejecutar el código: tiene que ir literal, no en una f-string.
        texto = (FUENTE.replace(LINEA, f'MODE = "{modo}"').replace(JUEGO, f'SET = "{juego}"')
                 .replace(NOMBRE, f'name="{nombre}"')
                 .replace(DESCRIPCION, f"    description={descripcion!r},\n"))
        destino.write_text(texto, encoding="utf-8")
        print(destino.relative_to(AQUI.parent), len(descripcion))
