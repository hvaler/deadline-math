"""Todas las cifras que cita entrega/articulo.md, calculadas desde los datos descargados. Ejecutar en la congelación
y copiar desde aquí, nunca a mano.

    .venv/Scripts/python.exe benchmark/cifras_articulo.py > benchmark/resultados/cifras-articulo.md
"""

from collections import Counter, defaultdict
from datetime import datetime

import analisis_pares as ap
import kaggle_resultados as kr
from deadline_math import parse_answer

FMT = "%Y-%m-%d %H:%M"
PRERREGISTRADOS = [linea.split()[1] for linea in (ap.SALIDA / "pendientes-pares.txt").read_text(encoding="utf-8").splitlines()
                   if linea.strip()]


def cohorte() -> tuple[list[str], dict[str, dict[str, kr.Ejecucion]]]:
    elegidas = {t: {m: kr.elegida(e) for m, e in kr.leer_task(t).items()} for t in kr.PROTOCOLO}
    modelos = sorted(set().union(*(set(d) for d in elegidas.values())))
    return [m for m in modelos if all(elegidas[t].get(m) for t in kr.PROTOCOLO)], elegidas


def main() -> None:
    miembros, elegidas = cohorte()
    print(f"# Cifras del artículo ({datetime.now():%Y-%m-%d %H:%M})\n")
    print(f"## Cohorte de las 4 tasks: {len(miembros)} modelos\n")
    for t in kr.PROTOCOLO:
        ok = sum(sum(s == "ok" for s in elegidas[t][m].casos.values()) for m in miembros)
        n = sum(len(elegidas[t][m].casos) for m in miembros)
        estricto = sum(sum(elegidas[t][m].strict.values()) for m in miembros)
        print(f"- {t}: {ok}/{n} ({ok / n:.1%}); una sola línea ANSWER {estricto}/{n}")

    completos = [m for m, e in elegidas["deadline-math-direct"].items() if e]
    perfectos = sorted(m for m in completos if all(s == "ok" for s in elegidas["deadline-math-direct"][m].casos.values()))
    print(f"\n## Estándar directo: {len(perfectos)} de {len(completos)} completados con 20/20\n\n{', '.join(perfectos)}")

    print("\n## Directo frente a razonado (estándar), por modelo de la cohorte\n")
    for m in miembros:
        d = sum(s == "ok" for s in elegidas["deadline-math-direct"][m].casos.values())
        r = sum(s == "ok" for s in elegidas["deadline-math-reasoned"][m].casos.values())
        if r - d >= 5:
            print(f"- {m}: {d}/20 -> {r}/20")

    print("\n## Tamaño del error en las respuestas equivocadas (cohorte, 4 tasks)\n")
    por_cat, total = defaultdict(Counter), Counter()
    for t in kr.PROTOCOLO:
        for m in miembros:
            ej = elegidas[t][m]
            for cid, estado in ej.casos.items():
                if estado != "wrong":
                    continue
                try:
                    horas = (datetime.strptime(parse_answer(ej.respuestas[cid]), FMT)
                             - datetime.strptime(kr.CASOS[cid].expected, FMT)).total_seconds() / 3600
                except ValueError:  # p. ej. «2026-12-31 24:00»: no es una hora válida, cuenta como otro error
                    horas = None
                clase = "exactamente 1 h" if horas is not None and abs(horas) == 1 else "otro"
                por_cat[kr.CASOS[cid].category][clase] += 1
                total[clase] += 1
    n = sum(total.values())
    print(f"- total: {total['exactamente 1 h']}/{n} ({total['exactamente 1 h'] / n:.0%}) exactamente una hora")
    for cat, c in sorted(por_cat.items()):
        print(f"- {cat}: {c['exactamente 1 h']}/{sum(c.values())}")

    print("\n## Nivel difícil: respuestas equivocadas repetidas\n")
    for t in ("deadline-math-hard-direct", "deadline-math-hard-reasoned"):
        for cid in ("h-fmt-1", "h-fmt-2"):
            c = Counter(parse_answer(elegidas[t][m].respuestas[cid]) for m in miembros
                        if elegidas[t][m].casos.get(cid) == "wrong")
            print(f"- {t} {cid} (correcta {kr.CASOS[cid].expected}): {dict(c.most_common(3))} de {sum(c.values())}")

    print("\n## Repetibilidad: dos ejecuciones limpias del mismo modelo y task (mismo prompt, temperatura 0)\n")
    iguales = total_casos = 0
    cambios = []
    for t in kr.PROTOCOLO:
        for m, ejecuciones in kr.leer_task(t).items():
            limpias = [e for e in ejecuciones if e.limpia]
            if len(limpias) < 2:
                continue
            a, b = limpias[-2], limpias[-1]
            iguales += sum((a.casos[i] == "ok") == (b.casos[i] == "ok") for i in a.casos)
            total_casos += len(a.casos)
            cambios.append(abs(sum(s == "ok" for s in a.casos.values()) - sum(s == "ok" for s in b.casos.values()))
                           / len(a.casos))
    if cambios:
        print(f"- {len(cambios)} pares de ejecuciones; acierto/fallo igual en {iguales}/{total_casos} casos "
              f"({iguales / total_casos:.1%})")
        print(f"- diferencia de acierto entre ejecuciones: media {sum(cambios) / len(cambios):.1%}, "
              f"máxima {max(cambios):.1%}")

    datos = ap.cargar_kaggle("deadline-math-pairs-direct")
    norm = {kr_norm(m): m for m in datos}
    primarios = {norm[kr_norm(m)]: datos[norm[kr_norm(m)]] for m in PRERREGISTRADOS if kr_norm(m) in norm}
    ampliacion = {m: d for m, d in datos.items() if m not in primarios}
    print(f"\n## Pares — prerregistrados ({len(primarios)} de {len(PRERREGISTRADOS)} completaron)\n")
    print(ap.informe(primarios, "prerregistrados"))
    if ampliacion:
        print(f"\n## Pares — ampliación, análisis secundario ({len(ampliacion)} modelos)\n")
        print(ap.informe(ampliacion, "ampliación"))


def kr_norm(slug: str) -> str:
    return slug.split("/")[-1].replace("@", "-").removesuffix("-it")


if __name__ == "__main__":
    main()
