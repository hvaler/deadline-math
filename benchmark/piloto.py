"""Piloto de Deadline Math: los 20 casos contra un modelo, con respuesta, acierto y coste por caso.

Mismo prompt y mismo parser que la task de Kaggle (deadline_math.py). Un proceso por modelo y modo
(«reasoned», razonamiento libre; «direct», solo la respuesta):

    .venv/Scripts/python.exe benchmark/piloto.py google/gemini-3-flash-preview direct          # juego «standard»
    .venv/Scripts/python.exe benchmark/piloto.py google/gemini-3-flash-preview direct hard     # nivel difícil
    .venv/Scripts/python.exe benchmark/piloto.py --resumen      # tabla con lo que haya en resultados/
"""

import json
import sys
import time
from collections import defaultdict
from pathlib import Path

import kaggle_benchmarks as kbench

import re

from deadline_math import ALL_CASES, CASE_SETS, PROMPTS, parse_answer

# Sin el prefijo ANSWER: la última fecha y hora del texto, para separar «fallo de formato» de «hora mal».
LOOSE_RE = re.compile(r"(\d{4}-\d{2}-\d{2})[ T](\d{1,2}):(\d{2})")


def loose_answer(response: str) -> str | None:
    answer = parse_answer(response)
    if answer:
        return answer
    loose = LOOSE_RE.findall(response.split("</think>")[-1])
    return f"{loose[-1][0]} {int(loose[-1][1]):02d}:{loose[-1][2]}" if loose else None

RESULTADOS = Path(__file__).parent / "resultados"


def correr(modelo: str, modo: str, juego: str = "standard") -> None:
    llm = kbench.llms[modelo]
    RESULTADOS.mkdir(exist_ok=True)
    salida = RESULTADOS / f"piloto-{'' if juego == 'standard' else juego + '-'}{modo}-{modelo.replace('/', '_').replace('@', '_')}.jsonl"
    # Reanuda: se conservan las respuestas buenas y solo se repiten los casos que dieron error de la API.
    hechas = {}
    if salida.exists():
        for linea in salida.open(encoding="utf-8"):
            fila = json.loads(linea)
            if not fila["response"].startswith("ERROR"):
                hechas[fila["id"]] = linea
    salida.write_text("".join(hechas.values()), encoding="utf-8")  # si se corta a mitad, no se pierde nada
    with salida.open("a", encoding="utf-8") as f:
        for case in CASE_SETS[juego]:
            if case.id in hechas:
                continue
            for intento in range(5):  # 429 «heavy load» en los modelos abiertos: esperar y reintentar
                with kbench.chats.new(f"piloto-{case.id}") as chat:
                    try:
                        response = llm.prompt(PROMPTS[modo].format(reader=case.reader, statement=case.statement, target=case.target))
                    except Exception as error:  # se anota y se sigue: un fallo de red no invalida el resto
                        response = f"ERROR: {error}"
                    usage = chat.usage
                if not response.startswith("ERROR"):
                    break
                time.sleep(20 * (intento + 1))
            answer = parse_answer(response)
            costs = (usage.input_tokens_cost_nanodollars, usage.output_tokens_cost_nanodollars)
            fila = {
                "modelo": modelo,
                "modo": modo,
                "id": case.id,
                "category": case.category,
                "expected": case.expected,
                "answer": answer,
                "ok": answer == case.expected,
                "format_ok": answer is not None,
                "ok_ignoring_format": loose_answer(response) == case.expected,
                "input_tokens": usage.input_tokens,
                "output_tokens": usage.output_tokens,
                "cost_usd": None if None in costs else sum(costs) / 1e9,  # algunos modelos no informan del coste
                "response": response,
            }
            f.write(json.dumps(fila, ensure_ascii=False) + "\n")
            f.flush()
            print(f"{case.id:10} {'OK ' if fila['ok'] else 'MAL'} {answer} (esperado {case.expected})", flush=True)


def resumen() -> None:
    filas = [json.loads(l) for p in sorted(RESULTADOS.glob("piloto-*.jsonl")) for l in p.open(encoding="utf-8")]
    errores = defaultdict(int)
    for r in filas:
        if r["response"].startswith("ERROR"):
            errores[f"{r['modelo']} [{r.get('modo', 'reasoned')}]"] += 1
    filas = [r for r in filas if not r["response"].startswith("ERROR")]  # un error de la API no es un fallo
    for r in filas:
        r.setdefault("modo", "reasoned")
        r["ok_ignoring_format"] = loose_answer(r["response"]) == r["expected"]
        juego = "hard" if r["id"].startswith("h-") else "standard"
        r["modelo"] = f"{r['modelo']} [{juego} {r['modo']}]"
    modelos = sorted({r["modelo"] for r in filas})
    categorias = list(dict.fromkeys(c.category for c in ALL_CASES))
    tabla = defaultdict(lambda: [0, 0])
    for r in filas:
        for clave in ((r["modelo"], r["category"]), (r["modelo"], "TOTAL")):
            tabla[clave][0] += r["ok"]
            tabla[clave][1] += 1
    print("| modelo | " + " | ".join(categorias + ["TOTAL", "sin formato", "ok ignorando formato", "coste $"]) + " |")
    print("|---" * (len(categorias) + 5) + "|")
    for m in modelos:
        celdas = [f"{tabla[(m, c)][0]}/{tabla[(m, c)][1]}" if tabla[(m, c)][1] else "·" for c in categorias + ["TOTAL"]]
        mias = [r for r in filas if r["modelo"] == m]
        sin_formato = sum(r.get("answer") is None for r in mias)
        ok_suelto = sum(r["ok_ignoring_format"] for r in mias)
        costes = [r["cost_usd"] for r in mias if r["cost_usd"] is not None]
        coste = f"{sum(costes):.4f}" if len(costes) == len(mias) else "n/d"
        print(f"| {m} | " + " | ".join(celdas) + f" | {sin_formato} | {ok_suelto}/{len(mias)} | {coste} |")
    if errores:
        print("\nSin respuesta por error de la API (fuera de la tabla): " + ", ".join(f"{m}: {n}" for m, n in errores.items()))
    print("\nFallos:")
    for r in filas:
        if not r["ok"]:
            print(f"- {r['modelo']} · {r['id']}: respondió {r['answer']}, esperado {r['expected']}")


if __name__ == "__main__":
    resumen() if sys.argv[1] == "--resumen" else correr(*sys.argv[1:4])
