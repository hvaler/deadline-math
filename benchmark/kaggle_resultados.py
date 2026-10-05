"""Resultados de las ejecuciones descargadas de Kaggle (`kaggle b t download`), con versiones fijadas.

Qué cuenta y qué no:

- Solo las versiones de PROTOCOLO. Se excluye `deadline-math-direct` v2: allí los reintentos repetían el prompt
  dentro de la misma conversación y un error de la API puntuaba como fallo.
- Cada caso se clasifica a partir de la respuesta guardada en la trayectoria (`*.atif.json`), no de la nota
  agregada: `ok`, `wrong` (hora extraída pero equivocada), `no_answer` (respondió sin línea ANSWER), `truncated`
  (sin línea ANSWER y al borde de max_tokens) o `infra` (el modelo no llegó a responder: 403/404/429/503).
- Se comprueba que el prompt enviado en cada caso es idéntico al que genera hoy `deadline_math.py`; si no, la
  ejecución se descarta como «otro protocolo».
- `strict`: en los modos directos, si la respuesta es exactamente una línea `ANSWER: YYYY-MM-DD HH:MM`. El acierto
  principal mide si se puede extraer una hora correcta, no el cumplimiento literal del formato.

    .venv/Scripts/python.exe benchmark/kaggle_resultados.py deadline-math-direct     # tabla de una task
    .venv/Scripts/python.exe benchmark/kaggle_resultados.py --informe                # cohorte + manifiesto
"""

import hashlib
import json
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from deadline_math import ALL_CASES, CASE_SETS, PROMPTS, parse_answer

RAIZ = Path(__file__).parent / "resultados" / "kaggle"
SALIDA = Path(__file__).parent / "resultados"
CASOS = {c.id: c for c in ALL_CASES}
STRICT_RE = re.compile(r"ANSWER: \d{4}-\d{2}-\d{2} \d{2}:\d{2}")

@dataclass(frozen=True)
class Protocolo:
    juego: str
    modo: str
    desde: int  # primera versión aceptada: misma conversación por caso, reintentos en chat nuevo, error a la vista
    limite_desde: int  # primera versión con max_tokens
    max_tokens: int

    def acepta(self, version: int) -> bool:
        return version >= self.desde

    def limite(self, version: int) -> int | None:
        return self.max_tokens if version >= self.limite_desde else None


# Las versiones nuevas (las que se suban para repetir ejecuciones) entran solas: llevan max_tokens.
PROTOCOLO = {
    "deadline-math-direct": Protocolo("standard", "direct", desde=3, limite_desde=4, max_tokens=8192),
    "deadline-math-reasoned": Protocolo("standard", "reasoned", desde=3, limite_desde=4, max_tokens=8192),
    "deadline-math-hard-direct": Protocolo("hard", "direct", desde=1, limite_desde=2, max_tokens=16384),
    "deadline-math-hard-reasoned": Protocolo("hard", "reasoned", desde=1, limite_desde=2, max_tokens=16384),
}
# Conjunto confirmatorio prerregistrado (docs/04-PREREGISTRO.md): va aparte de la cohorte de las 4 tasks.
PROTOCOLO_PARES = {
    "deadline-math-pairs-direct": Protocolo("pairs", "direct", desde=1, limite_desde=1, max_tokens=8192),
    "deadline-math-pairs-reasoned": Protocolo("pairs", "reasoned", desde=1, limite_desde=1, max_tokens=8192),
}
TRUNCATION_SHARE = 0.95  # mismo umbral que la task


@dataclass
class Ejecucion:
    task: str
    modelo: str
    version: int
    completada: bool
    error: str = ""
    casos: dict[str, str] = field(default_factory=dict)  # id -> ok / wrong / no_answer / truncated / infra
    strict: dict[str, bool] = field(default_factory=dict)  # id -> formato estricto (solo con respuesta)
    respuestas: dict[str, str] = field(default_factory=dict)
    otro_protocolo: list[str] = field(default_factory=list)  # casos cuyo prompt no coincide con el actual
    discrepancias: list[str] = field(default_factory=list)  # casos donde la aserción de Kaggle dice otra cosa

    @property
    def limpia(self) -> bool:
        """Completa, con todos los casos respondidos y con el protocolo actual."""
        juego = {**PROTOCOLO, **PROTOCOLO_PARES}[self.task].juego
        return (self.completada and not self.otro_protocolo
                and len(self.casos) == len(CASE_SETS[juego])
                and "infra" not in self.casos.values())


def _ultima_respuesta(sub: dict) -> tuple[str | None, str | None]:
    """(prompt enviado, última respuesta del modelo) de una trayectoria de caso."""
    prompt = next((p.get("message") for p in sub["steps"] if p.get("source") == "user"), None)
    respuestas = [p.get("message") for p in sub["steps"] if p.get("source") == "agent"]
    return prompt, (respuestas[-1] if respuestas else None)


def clasificar(respuesta: str | None, esperado: str, max_tokens: int | None, output_tokens: int | None) -> str:
    if respuesta is None:
        return "infra"
    answer = parse_answer(respuesta)
    if answer is None:
        cerca = max_tokens and output_tokens and output_tokens >= TRUNCATION_SHARE * max_tokens
        return "truncated" if cerca or "(truncated at max_tokens" in respuesta else "no_answer"
    return "ok" if answer == esperado else "wrong"


def leer_ejecucion(task: str, version: int, run_json: Path) -> Ejecucion:
    proto = {**PROTOCOLO, **PROTOCOLO_PARES}[task]
    juego, modo = proto.juego, proto.modo
    datos = json.loads(run_json.read_text(encoding="utf-8"))
    modelo = datos["modelVersion"]["slug"]
    completada = datos.get("state") == "BENCHMARK_TASK_RUN_STATE_COMPLETED"
    ej = Ejecucion(task, modelo, version, completada, error=(datos.get("errorMessage") or "")[-300:])
    if not completada:
        return ej
    caso_de = {a["expectation"]: m.group(1) for a in datos["assertions"]
               if (m := re.match(r"^\[[^\]]+\] (\S+):", a["expectation"]))}
    aserciones = {caso_de[a["expectation"]]: a["status"].endswith("PASSED")
                  for a in datos["assertions"] if a["expectation"] in caso_de}
    truncadas = {caso for texto, caso in caso_de.items() if "(truncated at max_tokens" in texto}
    atif = next(run_json.parent.glob("*.atif.json"), None)
    trayectorias: dict[str, list[dict]] = defaultdict(list)
    if atif is not None:
        for sub in json.loads(atif.read_text(encoding="utf-8")).get("subagent_trajectories") or []:
            trayectorias[sub["agent"]["name"].split("-try")[0]].append(sub)
    for case in CASE_SETS[juego]:
        prompt, respuesta = None, None
        for sub in trayectorias.get(case.id, []):  # el último intento con respuesta es el que puntuó
            p, r = _ultima_respuesta(sub)
            prompt = prompt or p
            respuesta = r if r is not None else respuesta
        esperado_prompt = PROMPTS[modo].format(reader=case.reader, statement=case.statement, target=case.target)
        if prompt is not None and prompt != esperado_prompt:
            ej.otro_protocolo.append(case.id)
        estado = clasificar(respuesta, case.expected, proto.limite(version), None)
        if case.id in truncadas and estado != "ok":
            estado = "truncated"
        ej.casos[case.id] = estado
        if estado != "infra" and case.id in aserciones and aserciones[case.id] != (estado == "ok"):
            ej.discrepancias.append(case.id)
        if respuesta is not None:
            ej.respuestas[case.id] = respuesta
            ej.strict[case.id] = bool(STRICT_RE.fullmatch(respuesta.strip()))
    return ej


def leer_task(task: str) -> dict[str, list[Ejecucion]]:
    """modelo -> ejecuciones de las versiones aceptadas, de la más antigua a la más reciente."""
    por_modelo: dict[str, list[Ejecucion]] = defaultdict(list)
    carpetas = [c for c in (RAIZ / task).iterdir() if c.name.isdigit()] if (RAIZ / task).exists() else []
    for carpeta in sorted(carpetas, key=lambda c: int(c.name)):
        version = int(carpeta.name)
        if not {**PROTOCOLO, **PROTOCOLO_PARES}[task].acepta(version):
            continue
        for run in sorted(carpeta.glob("*/*/*.run.json")):
            ej = leer_ejecucion(task, version, run)
            por_modelo[ej.modelo].append(ej)
    return por_modelo


def elegida(ejecuciones: list[Ejecucion]) -> Ejecucion | None:
    """La ejecución limpia más reciente; si no hay ninguna, None (el modelo queda «no completado»)."""
    limpias = [e for e in ejecuciones if e.limpia]
    return limpias[-1] if limpias else None


def leer(task: str) -> tuple[dict[str, dict[str, bool | None]], dict[str, str]]:
    """Compatibilidad con pendientes_kaggle.py: modelo -> {caso -> acierto, None si infra}, y las no completadas."""
    resultado, fallidas = {}, {}
    for modelo, ejecuciones in leer_task(task).items():
        ej = elegida(ejecuciones)
        if ej is None:
            ultima = ejecuciones[-1]
            fallidas[modelo] = ultima.error or ("protocolo distinto" if ultima.otro_protocolo else "casos sin respuesta")
            continue
        resultado[modelo] = {i: (None if s == "infra" else s == "ok") for i, s in ej.casos.items()}
    return resultado, fallidas


def _causa(ejecuciones: list[Ejecucion]) -> str:
    """Motivo breve por el que un modelo no tiene ejecución limpia."""
    texto = " ".join(e.error for e in ejecuciones)
    for codigo, nombre in (("403", "cuota (403)"), ("404", "modelo no encontrado (404)"),
                           ("429", "saturado (429)"), ("503", "no disponible (503)")):
        if f"Error code: {codigo}" in texto:
            return nombre
    if any(e.otro_protocolo for e in ejecuciones):
        return "prompt distinto del actual"
    if any("infra" in e.casos.values() for e in ejecuciones):
        return "casos sin respuesta"
    return "error"


def tabla_task(task: str) -> None:
    juego = {**PROTOCOLO, **PROTOCOLO_PARES}[task].juego
    categorias = list(dict.fromkeys(c.category for c in CASE_SETS[juego]))
    por_modelo = leer_task(task)
    filas, no_completados = [], []
    for modelo, ejecuciones in por_modelo.items():
        ej = elegida(ejecuciones)
        if ej is None:
            no_completados.append((modelo, _causa(ejecuciones)))
            continue
        cuenta = Counter(ej.casos.values())
        celdas = []
        for cat in categorias:
            ids = [c.id for c in CASE_SETS[juego] if c.category == cat]
            celdas.append(f"{sum(ej.casos[i] == 'ok' for i in ids)}/{len(ids)}")
        strict = f"{sum(ej.strict.values())}/{len(ej.strict)}"
        filas.append((cuenta["ok"] / len(ej.casos), modelo, ej.version, celdas, cuenta, strict))
    print(f"| modelo | v | {' | '.join(categorias)} | acierto | wrong | no_answer | truncated | strict |")
    print("|---" * (len(categorias) + 7) + "|")
    for acierto, modelo, version, celdas, cuenta, strict in sorted(filas, reverse=True):
        print(f"| {modelo} | {version} | {' | '.join(celdas)} | {acierto:.0%} | {cuenta['wrong']} | "
              f"{cuenta['no_answer']} | {cuenta['truncated']} | {strict} |")
    discrepancias = [f"{m} v{e.version}: {e.discrepancias}" for m, es in por_modelo.items() for e in es
                     if e.discrepancias]
    if discrepancias:
        print("\nAVISO: la clasificación no coincide con la aserción de Kaggle en:", *discrepancias, sep="\n  ")
    if no_completados:
        print("\nNo completados (infraestructura, no puntúan):")
        for modelo, causa in sorted(no_completados):
            print(f"  {modelo}: {causa}")


def informe() -> None:
    """Cohorte con las 4 tasks limpias: tabla Markdown y manifiesto JSON en benchmark/resultados/."""
    elegidas = {task: {m: elegida(e) for m, e in leer_task(task).items()} for task in PROTOCOLO}
    modelos = sorted(set().union(*(set(d) for d in elegidas.values())))
    cohorte = [m for m in modelos if all(elegidas[t].get(m) for t in PROTOCOLO)]
    abrevia = {"deadline-math-direct": "std direct", "deadline-math-reasoned": "std reasoned",
               "deadline-math-hard-direct": "hard direct", "deadline-math-hard-reasoned": "hard reasoned"}

    lineas = [f"# Deadline Math — cohorte de {len(cohorte)} modelos con las 4 tasks completas",
              "", f"Generado {datetime.now(timezone.utc):%Y-%m-%d %H:%M} UTC por `kaggle_resultados.py --informe`. "
              "Una ejecución por modelo y condición; acierto = hora local extraída correcta.", "",
              "| modelo | " + " | ".join(abrevia[t] for t in PROTOCOLO) + " |", "|---" * 5 + "|"]
    totales = {t: Counter() for t in PROTOCOLO}
    for m in cohorte:
        celdas = []
        for t in PROTOCOLO:
            ej = elegidas[t][m]
            ok = sum(s == "ok" for s in ej.casos.values())
            totales[t]["ok"] += ok
            totales[t]["n"] += len(ej.casos)
            totales[t].update(s for s in ej.casos.values() if s != "ok")
            totales[t]["strict"] += sum(ej.strict.values())
            celdas.append(f"{ok}/{len(ej.casos)} (v{ej.version})")
        lineas.append(f"| {m} | " + " | ".join(celdas) + " |")
    lineas += ["", "| condición | aciertos | wrong | no_answer | truncated | una sola línea ANSWER |",
               "|---|---|---|---|---|---|"]
    for t in PROTOCOLO:
        c = totales[t]
        # El formato estricto solo se pide en los modos directos; en los razonados se espera texto antes.
        estricto = f"{c['strict']}/{c['n']}" if PROTOCOLO[t].modo == "direct" else "no se pide"
        lineas.append(f"| {abrevia[t]} | {c['ok']}/{c['n']} ({c['ok'] / max(c['n'], 1):.1%}) | {c['wrong']} | "
                      f"{c['no_answer']} | {c['truncated']} | {estricto} |")
    fuera = []
    for m in modelos:
        if m in cohorte:
            continue
        faltan = [f"{abrevia[t]}: {_causa(leer_task(t).get(m, []))}" for t in PROTOCOLO if not elegidas[t].get(m)]
        fuera.append(f"- {m} — " + "; ".join(faltan))
    lineas += ["", f"## Fuera de la cohorte ({len(fuera)}): no completados, no puntúan como 0 %", "", *fuera]
    (SALIDA / "tabla-cohorte.md").write_text("\n".join(lineas) + "\n", encoding="utf-8")

    manifiesto = {
        "generado_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "protocolo": {t: {"set": p.juego, "mode": p.modo, "accepted_from_version": p.desde,
                          "max_tokens": p.max_tokens, "max_tokens_from_version": p.limite_desde}
                      for t, p in PROTOCOLO.items()},
        "codigo_sha256": {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                          for p in sorted((Path(__file__).parent / "kaggle").glob("*.py"))},
        "casos": {"standard": len(CASE_SETS["standard"]), "hard": len(CASE_SETS["hard"])},
        "cohorte": cohorte,
        "ejecuciones": {t: {m: ej.version for m, ej in elegidas[t].items() if ej} for t in PROTOCOLO},
    }
    (SALIDA / "manifiesto.json").write_text(json.dumps(manifiesto, indent=2, ensure_ascii=False) + "\n",
                                            encoding="utf-8")
    print("\n".join(lineas))


if __name__ == "__main__":
    informe() if sys.argv[1] == "--informe" else tabla_task(sys.argv[1])
