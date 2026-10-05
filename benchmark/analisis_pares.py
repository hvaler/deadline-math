"""Análisis prerregistrado del conjunto de pares (docs/04-PREREGISTRO.md). No cambiar las medidas sin anotar una
desviación en el prerregistro.

    .venv/Scripts/python.exe benchmark/analisis_pares.py kaggle deadline-math-pairs-direct
    .venv/Scripts/python.exe benchmark/analisis_pares.py piloto direct      # resultados/piloto-pairs-direct-*.jsonl

Escribe la tabla en benchmark/resultados/pares-<origen>-<task o modo>.md y la muestra.
"""

import json
import random
import sys
from collections import defaultdict
from math import comb, sqrt
from pathlib import Path

import kaggle_resultados as kr
from deadline_math import CASES_PAIRS, parse_answer

SALIDA = Path(__file__).parent / "resultados"
TRAMPAS = [c for c in CASES_PAIRS if c.id.endswith("-T")]
CASO = {c.id: c for c in CASES_PAIRS}
BOOTSTRAP = 10_000


def wilson(aciertos: int, n: int, z: float = 1.96) -> tuple[float, float]:
    if n == 0:
        return (0.0, 1.0)
    p = aciertos / n
    centro = (p + z * z / (2 * n)) / (1 + z * z / n)
    margen = z * sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return (max(0.0, centro - margen), min(1.0, centro + margen))


def binomial_dos_colas(k: int, n: int) -> float:
    """p-valor exacto de que k de n discordantes caigan de un lado con p = 0,5 (McNemar exacta, prueba de signos)."""
    if n == 0:
        return 1.0
    extremo = min(k, n - k)
    return min(1.0, 2 * sum(comb(n, i) for i in range(extremo + 1)) / 2 ** n)


def cargar_kaggle(task: str) -> dict[str, dict[str, tuple[str, str | None]]]:
    """modelo -> {caso -> (estado, respuesta)} con la ejecución limpia más reciente; si no hay, la más reciente
    completada (los pares con un caso infra se excluyen después, como dice el prerregistro)."""
    datos = {}
    for modelo, ejecuciones in kr.leer_task(task).items():
        completas = [e for e in ejecuciones if e.completada and not e.otro_protocolo]
        if not completas:
            continue
        ej = kr.elegida(ejecuciones) or completas[-1]
        datos[modelo] = {i: (s, ej.respuestas.get(i)) for i, s in ej.casos.items()}
    return datos


def cargar_piloto(modo: str) -> dict[str, dict[str, tuple[str, str | None]]]:
    datos = defaultdict(dict)
    for fichero in sorted(SALIDA.glob(f"piloto-pairs-{modo}-*.jsonl")):
        for linea in fichero.open(encoding="utf-8"):
            r = json.loads(linea)
            if r["response"].startswith("ERROR"):
                estado = "infra"
            else:
                estado = kr.clasificar(r["response"], r["expected"], 8192, r.get("output_tokens"))
            datos[r["modelo"]][r["id"]] = (estado, r["response"])
    return dict(datos)


def pares_validos(casos: dict[str, tuple[str, str | None]]) -> list[tuple[str, str]]:
    """(id trampa, id control) de los pares con los dos casos respondidos."""
    validos = []
    for trampa in TRAMPAS:
        control = trampa.id[:-1] + "C"
        if trampa.id in casos and control in casos and "infra" not in (casos[trampa.id][0], casos[control][0]):
            validos.append((trampa.id, control))
    return validos


def informe(datos: dict[str, dict[str, tuple[str, str | None]]], titulo: str) -> str:
    lineas = [f"# Pares prerregistrados — {titulo}", "",
              "Trampa = la fecha cae donde la diferencia habitual no vale; control = el mismo enunciado fuera de ese "
              "periodo. Penalización = acierto en controles − acierto en trampas. IC al 95 %.", "",
              "| modelo | pares | trampas | controles | penalización | b / c | McNemar p | errores = ingenua |",
              "|---|---|---|---|---|---|---|---|"]
    penalizaciones, signos = {}, [0, 0]
    ingenuas, equivocadas = 0, 0
    por_estrato = defaultdict(lambda: [0, 0, 0])  # estrato -> [aciertos trampa, aciertos control, pares]
    for modelo, casos in sorted(datos.items()):
        pares = pares_validos(casos)
        if not pares:
            continue
        ok_t = sum(casos[t][0] == "ok" for t, _ in pares)
        ok_c = sum(casos[c][0] == "ok" for _, c in pares)
        b = sum(casos[c][0] == "ok" and casos[t][0] != "ok" for t, c in pares)  # control bien, trampa mal
        c_ = sum(casos[t][0] == "ok" and casos[c][0] != "ok" for t, c in pares)
        mal = [t for t, _ in pares if casos[t][0] == "wrong"]
        iguales = sum(parse_answer(casos[t][1]) == CASO[t].naive for t in mal)
        ingenuas += iguales
        equivocadas += len(mal)
        n = len(pares)
        pen = (ok_c - ok_t) / n
        penalizaciones[modelo] = {t: (casos[c][0] == "ok") - (casos[t][0] == "ok") for t, c in pares}
        signos[0 if pen > 0 else 1] += pen != 0
        for t, c in pares:
            caso = CASO[t]
            estrato = caso.category.rsplit("-", 1)[0].replace("pair-", "")
            por_estrato[estrato][0] += casos[t][0] == "ok"
            por_estrato[estrato][1] += casos[c][0] == "ok"
            por_estrato[estrato][2] += 1
        wt, wc = wilson(ok_t, n), wilson(ok_c, n)
        lineas.append(f"| {modelo} | {n} | {ok_t / n:.0%} [{wt[0]:.0%}–{wt[1]:.0%}] | {ok_c / n:.0%} "
                      f"[{wc[0]:.0%}–{wc[1]:.0%}] | {pen:+.0%} | {b} / {c_} | {binomial_dos_colas(b, b + c_):.3g} | "
                      f"{iguales}/{len(mal)} |")

    # Agregado: penalización media de la cohorte, bootstrap sobre los 50 pares (semilla fija).
    modelos = list(penalizaciones)
    media = sum(sum(p.values()) / len(p) for p in penalizaciones.values()) / max(len(modelos), 1)
    azar = random.Random(0)
    ids = [t.id for t in TRAMPAS]
    medias = []
    for _ in range(BOOTSTRAP):
        muestra = [azar.choice(ids) for _ in ids]
        por_modelo = []
        for m in modelos:
            valores = [penalizaciones[m][t] for t in muestra if t in penalizaciones[m]]
            if valores:
                por_modelo.append(sum(valores) / len(valores))
        medias.append(sum(por_modelo) / len(por_modelo) if por_modelo else 0.0)
    medias.sort()
    ic = (medias[int(0.025 * BOOTSTRAP)], medias[int(0.975 * BOOTSTRAP) - 1])
    h2 = wilson(ingenuas, equivocadas)
    lineas += ["", "## Hipótesis", "",
               f"- **H1** — penalización media de la cohorte: **{media:+.1%}** (IC bootstrap 95 % {ic[0]:+.1%} a "
               f"{ic[1]:+.1%}). Modelos con penalización positiva / negativa: {signos[0]} / {signos[1]} "
               f"(prueba de signos p = {binomial_dos_colas(signos[0], sum(signos)):.3g}). "
               f"**{'Se sostiene' if ic[0] > 0 else 'No se sostiene'}** (criterio: IC por encima de cero).",
               f"- **H2** — errores en trampas iguales a la respuesta ingenua: **{ingenuas}/{equivocadas}** "
               f"({ingenuas / max(equivocadas, 1):.0%}, IC Wilson {h2[0]:.0%}–{h2[1]:.0%}). "
               f"**{'Se sostiene' if h2[0] > 0.5 else 'No se sostiene'}** (criterio: límite inferior > 50 %). "
               "Las respuestas sin línea ANSWER no entran en H2 y se cuentan como fallo en H1.",
               "", "## Por estrato (descriptivo)", "", "| estrato | pares | trampas | controles |", "|---|---|---|---|"]
    for estrato, (t, c, n) in sorted(por_estrato.items()):
        lineas.append(f"| {estrato} | {n} | {t / n:.0%} | {c / n:.0%} |")
    return "\n".join(lineas) + "\n"


if __name__ == "__main__":
    origen, que = sys.argv[1], sys.argv[2]
    datos = cargar_kaggle(que) if origen == "kaggle" else cargar_piloto(que)
    texto = informe(datos, f"{origen} {que}")
    (SALIDA / f"pares-{origen}-{que}.md").write_text(texto, encoding="utf-8")
    print(texto)
