"""Tablas en inglés para el artículo y el repositorio, desde los mismos datos y las mismas funciones que el análisis
prerregistrado (analisis_pares.estadisticas): las cifras no pueden diferir de las del informe en español.

    .venv/Scripts/python.exe benchmark/tablas_en.py      # escribe benchmark/resultados/RESULTS.md
"""

from datetime import datetime, timezone

import analisis_pares as ap
import cifras_articulo as ca
import kaggle_resultados as kr
from grafico_pares import NOMBRES

ETIQUETA_ESTRATO = {"conversion-autumn": "Conversion, autumn gap (Oct 26–31)",
                    "conversion-spring": "Conversion, spring gap (Mar 9–14)",
                    "duration-autumn": "Duration across the autumn change",
                    "duration-spring": "Duration across the spring change"}
TASKS = {"deadline-math-direct": "Standard, direct", "deadline-math-reasoned": "Standard, reasoned",
         "deadline-math-hard-direct": "Hard, direct", "deadline-math-hard-reasoned": "Hard, reasoned"}


def nombre(slug: str) -> str:
    return NOMBRES.get(slug.split("/")[-1], slug.split("/")[-1])


def tabla_pares(datos: dict, titulo: str, nota: str) -> list[str]:
    e = ap.estadisticas(datos)
    lineas = [f"## {titulo}", "", nota, "",
              "| Model | Pairs | Traps correct (95% CI) | Controls correct (95% CI) | Penalty | b / c | McNemar p "
              "| Trap errors = naive |", "|---|---|---|---|---|---|---|---|"]
    for f in sorted(e["filas"], key=lambda f: (-f["pen"], f["ok_t"])):
        n, wt, wc = f["n"], f["wt"], f["wc"]
        lineas.append(f"| {nombre(f['modelo'])} | {n} | {f['ok_t'] / n:.0%} ({wt[0]:.0%}–{wt[1]:.0%}) | "
                      f"{f['ok_c'] / n:.0%} ({wc[0]:.0%}–{wc[1]:.0%}) | {f['pen'] * 100:+.0f} pts | {f['b']} / {f['c']} | "
                      f"{f['p']:.2g} | {f['iguales']}/{f['mal']} |")
    ic, h2, signos = e["ic"], e["wilson_h2"], e["signos"]
    lineas += ["",
               f"- **H1 {'holds' if e['h1'] else 'does not hold'}.** Mean penalty **{e['media'] * 100:+.1f} points** "
               f"(95% bootstrap CI {ic[0] * 100:+.1f} to {ic[1] * 100:+.1f}, 10,000 resamples of the 50 pairs, seed 0). "
               f"Models with a positive / negative penalty: {signos[0]} / {signos[1]} (sign test p = {e['p_signos']:.2g}). "
               "Criterion: CI above zero.",
               f"- **H2 {'holds' if e['h2'] else 'does not hold'}.** {e['ingenuas']} of {e['equivocadas']} wrong trap "
               f"answers ({e['ingenuas'] / max(e['equivocadas'], 1):.0%}, Wilson CI {h2[0]:.0%}–{h2[1]:.0%}) are exactly "
               "the naive answer. Criterion: lower bound above 50%. Answers without an `ANSWER` line are not in H2 and "
               "count as failures in H1.", "",
               "| Stratum (descriptive) | Pairs | Traps correct | Controls correct |", "|---|---|---|---|"]
    for estrato, (t, c, n) in e["estratos"].items():
        lineas.append(f"| {ETIQUETA_ESTRATO.get(estrato, estrato)} | {n} | {t / n:.0%} | {c / n:.0%} |")
    return lineas + [""]


def tabla_cohorte() -> list[str]:
    miembros, elegidas = ca.cohorte()
    lineas = [f"## The four original tasks — cohort of {len(miembros)} models", "",
              "Models with a clean run (every case answered) on all four tasks. Score = correct local time extracted. "
              "Latest clean run per model; one run per cell, temperature 0 (runs are not deterministic: see "
              "repeatability below).", "",
              "| Model | " + " | ".join(TASKS.values()) + " |", "|---|" + "---|" * len(TASKS)]
    filas = []
    for m in miembros:
        celdas = []
        for t in TASKS:
            ej = elegidas[t][m]
            celdas.append((sum(s == "ok" for s in ej.casos.values()), len(ej.casos)))
        filas.append((nombre(m), celdas))
    for n_, celdas in sorted(filas, key=lambda f: (-sum(a / b for a, b in f[1]), f[0])):
        lineas.append(f"| {n_} | " + " | ".join(f"{a}/{b}" for a, b in celdas) + " |")
    lineas += ["", "| Condition | Correct | One-line `ANSWER` only |", "|---|---|---|"]
    for t, etiqueta in TASKS.items():
        ok = sum(sum(s == "ok" for s in elegidas[t][m].casos.values()) for m in miembros)
        n = sum(len(elegidas[t][m].casos) for m in miembros)
        estricto = sum(sum(elegidas[t][m].strict.values()) for m in miembros)
        lineas.append(f"| {etiqueta} | {ok}/{n} ({ok / n:.1%}) | "
                      f"{f'{estricto}/{n}' if kr.PROTOCOLO[t].modo == 'direct' else 'not required'} |")
    return lineas + [""]


def repetibilidad() -> list[str]:
    iguales = total = 0
    cambios = []
    for t in kr.PROTOCOLO:
        for _, ejecuciones in kr.leer_task(t).items():
            limpias = [e for e in ejecuciones if e.limpia]
            if len(limpias) < 2:
                continue
            a, b = limpias[-2], limpias[-1]
            iguales += sum((a.casos[i] == "ok") == (b.casos[i] == "ok") for i in a.casos)
            total += len(a.casos)
            cambios.append(abs(sum(s == "ok" for s in a.casos.values()) - sum(s == "ok" for s in b.casos.values()))
                           / len(a.casos))
    if not cambios:
        return []
    return ["## Repeatability", "",
            f"{len(cambios)} pairs of clean runs of the same model on the same task (same prompt, temperature 0): "
            f"right/wrong agreement on **{iguales}/{total} cases ({iguales / total:.1%})**; a model's score changes by "
            f"**{sum(cambios) / len(cambios) * 100:.1f} points on average** between runs, and by up to "
            f"{max(cambios) * 100:.0f} points.", ""]


def main() -> None:
    datos = ap.cargar_kaggle("deadline-math-pairs-direct")
    norm = {ca.kr_norm(m): m for m in datos}
    primarios = {norm[ca.kr_norm(m)]: datos[norm[ca.kr_norm(m)]] for m in ca.PRERREGISTRADOS if ca.kr_norm(m) in norm}
    ampliacion = {m: d for m, d in datos.items() if m not in primarios}
    lineas = ["# Deadline Math — results", "",
              f"Generated {datetime.now(timezone.utc):%Y-%m-%d %H:%M} UTC by `benchmark/tablas_en.py` from the runs in "
              "`benchmark/resultados/kaggle/`. Pre-registration: [`docs/PREREGISTRATION.md`](../../docs/PREREGISTRATION.md).",
              "",
              "**Trap** = the date falls where the usual offset does not hold (EU/US gap week, or a duration crossing a "
              "clock change). **Control** = the same sentence, reader, clock time and weekday, with the date moved out "
              "of that period. **Penalty** = controls correct − traps correct. **b / c** = pairs with only the control "
              "right / only the trap right. **Naive answer** = the usual offset, or adding clock hours.", ""]
    lineas += tabla_pares(primarios, f"Pre-registered result — paired set, {len(primarios)} of "
                          f"{len(ca.PRERREGISTRADOS)} pre-registered models",
                          "Primary analysis, exactly as pre-registered (direct mode, one run per model).")
    if ampliacion:
        lineas += tabla_pares(ampliacion, f"Secondary extension — paired set, {len(ampliacion)} more models",
                              "Same set, prompt and analysis on more models once quota allowed. Logged as a deviation "
                              "before running it; reported separately and not part of the confirmatory claim.")
    lineas += tabla_cohorte()
    lineas += repetibilidad()
    destino = ap.SALIDA / "RESULTS.md"
    destino.write_text("\n".join(lineas), encoding="utf-8")
    print(destino)


if __name__ == "__main__":
    main()
