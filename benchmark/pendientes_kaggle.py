"""Lista, por task, los modelos que faltan: sin ejecución completa o con casos sin respuesta (error de la API).

Sale en el formato que lee encolar_kaggle.sh: «task modelo» por línea, con el slug del CLI.

    .venv/Scripts/python.exe benchmark/pendientes_kaggle.py > benchmark/resultados/pendientes.txt
"""

from pathlib import Path

from kaggle_resultados import leer

TASKS = ["deadline-math-direct", "deadline-math-hard-direct", "deadline-math-hard-reasoned", "deadline-math-reasoned"]
SIN_SERVICIO = {"grok-4.5-0708", "grok-4.6"}  # el proxy responde 404 «model not found»
MODELOS = Path(__file__).parent / "resultados" / "modelos-kaggle-2026-10-03.txt"


def normal(slug: str) -> str:
    """'anthropic/claude-opus-4-8@default' y 'claude-opus-4-8-default' -> 'claude-opus-4-8-default'."""
    slug = slug.split("/")[-1].replace("@", "-")
    return slug.removesuffix("-it")


cli = [linea.split()[0] for linea in MODELOS.read_text(encoding="utf-8").splitlines()[2:] if linea.strip()]

if __name__ == "__main__":
    for task in TASKS:
        por_modelo, _ = leer(task)
        completos = {normal(m) for m, casos in por_modelo.items() if casos and None not in casos.values()}
        for modelo in cli:
            if modelo not in SIN_SERVICIO and normal(modelo) not in completos:
                print(task, modelo)
