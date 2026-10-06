"""Gráfico del artículo: acierto en trampas frente a controles, por modelo (dumbbell), desde los datos de Kaggle.

    .venv/Scripts/python.exe benchmark/grafico_pares.py      # escribe benchmark/resultados/grafico-pares.html

El HTML es un SVG estático (DEV solo admite imágenes); el PNG se saca con una captura del navegador.
Colores: slots 1 y 2 de la paleta de referencia de la skill dataviz, validados (ΔE CVD 24,7).
"""

from html import escape

import analisis_pares as ap
import cifras_articulo as ca

AZUL, NARANJA = "#2a78d6", "#eb6834"  # control, trampa
SUPERFICIE, TINTA, TINTA_2, REJILLA = "#fcfcfb", "#0b0b0b", "#52514e", "#e4e3df"
NOMBRES = {  # slug -> nombre legible
    "claude-haiku-4-5@20251001": "Claude Haiku 4.5", "claude-sonnet-5@default": "Claude Sonnet 5",
    "claude-sonnet-4-5@20250929": "Claude Sonnet 4.5", "claude-opus-4-5@20251101": "Claude Opus 4.5",
    "claude-opus-4-6@default": "Claude Opus 4.6", "claude-opus-4-7@default": "Claude Opus 4.7",
    "claude-opus-4-8@default": "Claude Opus 4.8", "claude-opus-5@default": "Claude Opus 5",
    "gemini-2.5-flash": "Gemini 2.5 Flash", "gemini-2.5-pro": "Gemini 2.5 Pro",
    "gemini-3-flash-preview": "Gemini 3 Flash", "gemini-3.1-flash-lite-preview": "Gemini 3.1 Flash Lite",
    "gemini-3.1-pro-preview": "Gemini 3.1 Pro", "gemini-3.5-flash": "Gemini 3.5 Flash",
    "gemini-3.5-flash-lite": "Gemini 3.5 Flash Lite", "gemini-3.6-flash": "Gemini 3.6 Flash",
    "gemini-3.7-flash": "Gemini 3.7 Flash", "gemini-3.8-flash": "Gemini 3.8 Flash",
    "gemma-4-26b-a4b": "Gemma 4 26B", "gemma-4-31b": "Gemma 4 31B", "glm-5": "GLM-5",
    "gpt-5.4-2026-03-05": "GPT-5.4", "gpt-5.4-mini-2026-03-17": "GPT-5.4 mini",
    "gpt-5.4-nano-2026-03-17": "GPT-5.4 nano", "gpt-5.5-2026-04-23": "GPT-5.5", "gpt-5.6-luna": "GPT-5.6 Luna",
    "gpt-5.6-sol": "GPT-5.6 Sol", "gpt-5.6-terra": "GPT-5.6 Terra", "gpt-6-astra": "GPT-6 Astra",
    "gpt-oss-20b": "gpt-oss-20b", "grok-4.20-0309-non-reasoning": "Grok 4.20 (non-reasoning)",
    "grok-4.20-0309-reasoning": "Grok 4.20 Reasoning", "qwen3-coder-480b-a35b-instruct": "Qwen3 Coder 480B",
    "qwen3-next-80b-a3b-thinking": "Qwen3 Next Thinking", "qwen3-next-80b-a3b-instruct": "Qwen3 Next Instruct",
    "qwen3-235b-a22b-instruct-2507": "Qwen3 235B", "deepseek-r1-0528": "DeepSeek R1",
}


def filas(datos: dict) -> list[tuple[str, float, float]]:
    resultado = []
    for modelo, casos in datos.items():
        pares = ap.pares_validos(casos)
        if not pares:
            continue
        trampas = sum(casos[t][0] == "ok" for t, _ in pares) / len(pares)
        controles = sum(casos[c][0] == "ok" for _, c in pares) / len(pares)
        resultado.append((NOMBRES.get(modelo.split("/")[-1], modelo.split("/")[-1]), trampas, controles))
    return sorted(resultado, key=lambda f: (-(f[2] - f[1]), f[1]))  # mayor caída arriba


def svg(grupos: list[tuple[str, list]], pie: str) -> str:
    ancho, izq, der, fila, arriba = 1000, 230, 90, 22, 136
    x = lambda v: izq + v * (ancho - izq - der)
    alto = arriba + sum(len(g) * fila + 40 for _, g in grupos) + 40
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{ancho}" height="{alto}" viewBox="0 0 {ancho} {alto}" '
         f'font-family="Inter, Segoe UI, Helvetica, Arial, sans-serif">',
         f'<rect width="100%" height="100%" fill="{SUPERFICIE}"/>',
         f'<text x="24" y="36" font-size="22" font-weight="700" fill="{TINTA}">Same sentence, trap date vs. control date</text>',
         f'<text x="24" y="60" font-size="14" fill="{TINTA_2}">Share of correct answers on 50 trap/control pairs (direct mode, Kaggle). Controls move the date out of the EU/US</text>',
         f'<text x="24" y="78" font-size="14" fill="{TINTA_2}">gap (7 days earlier in autumn, 21 days later in spring) or keep a duration from crossing a clock change.</text>']
    # Leyenda: forma + color + texto (la identidad nunca va solo en el color).
    p += [f'<circle cx="30" cy="104" r="8" fill="{AZUL}"/><text x="42" y="109" font-size="13" fill="{TINTA}">Control</text>',
          f'<path d="M118 98 l6 6 l-6 6 l-6 -6 z" fill="{NARANJA}"/>'
          f'<text x="132" y="109" font-size="13" fill="{TINTA}">Trap (gap week or duration across a clock change)</text>',
          f'<text x="{ancho - 24}" y="109" font-size="13" text-anchor="end" fill="{TINTA_2}">Trap vs. control</text>']
    y = arriba
    for titulo, datos in grupos:
        p.append(f'<text x="24" y="{y + 4}" font-size="13" font-weight="700" fill="{TINTA_2}">{escape(titulo)}</text>')
        y += 20
        for v in (0, 0.25, 0.5, 0.75, 1):  # rejilla recesiva
            p.append(f'<line x1="{x(v):.1f}" y1="{y - 6}" x2="{x(v):.1f}" y2="{y + len(datos) * fila - 8}" '
                     f'stroke="{REJILLA}" stroke-width="1"/>')
        for nombre, t, c in datos:
            cy = y + fila / 2 - 4
            p.append(f'<text x="{izq - 14}" y="{cy + 4.5}" font-size="13" text-anchor="end" fill="{TINTA}">{escape(nombre)}</text>')
            p.append(f'<line x1="{x(t):.1f}" y1="{cy}" x2="{x(c):.1f}" y2="{cy}" stroke="#b9b7b0" stroke-width="2"/>')
            # Círculo mayor que el rombo: si coinciden (100 % y 100 %), el azul asoma alrededor del naranja.
            p.append(f'<circle cx="{x(c):.1f}" cy="{cy}" r="8" fill="{AZUL}" stroke="{SUPERFICIE}" stroke-width="2"/>')
            p.append(f'<path d="M{x(t):.1f} {cy - 6} l6 6 l-6 6 l-6 -6 z" fill="{NARANJA}" stroke="{SUPERFICIE}" stroke-width="2"/>')
            pen = round((c - t) * 100)
            texto = f"−{pen} pts" if pen > 0 else (f"+{-pen} pts" if pen < 0 else "same")
            p.append(f'<text x="{ancho - 24}" y="{cy + 4.5}" font-size="13" text-anchor="end" fill="{TINTA_2}">{texto}</text>')
            y += fila
        y += 20
    for v in (0, 0.25, 0.5, 0.75, 1):
        p.append(f'<text x="{x(v):.1f}" y="{y - 2}" font-size="12" text-anchor="middle" fill="{TINTA_2}">{int(v * 100)}%</text>')
    p.append(f'<text x="24" y="{alto - 12}" font-size="12" fill="{TINTA_2}">{escape(pie)}</text>')
    p.append("</svg>")
    return "\n".join(p)


def main() -> None:
    datos = ap.cargar_kaggle("deadline-math-pairs-direct")
    norm = {ca.kr_norm(m): m for m in datos}
    primarios = {norm[ca.kr_norm(m)]: datos[norm[ca.kr_norm(m)]] for m in ca.PRERREGISTRADOS if ca.kr_norm(m) in norm}
    ampliacion = {m: d for m, d in datos.items() if m not in primarios}
    f1, f2 = filas(primarios), filas(ampliacion)
    pie_todo = ("Pre-registered cohort: hypotheses and design fixed before the run. Extension: same set, logged as a "
                "deviation, reported separately. github.com/hvaler/deadline-math")
    pie_19 = ("Pre-registered cohort only: hypotheses, design and models fixed before the run. Extension to 18 more "
              "models: github.com/hvaler/deadline-math")
    versiones = {  # la del artículo (solo prerregistrados) y la completa (enlazada)
        "grafico-pares-prerregistrados.html": svg([(f"Pre-registered cohort ({len(f1)} models)", f1)], pie_19),
        "grafico-pares.html": svg([(f"Pre-registered cohort ({len(f1)} models)", f1),
                                   (f"Extension ({len(f2)} models)", f2)], pie_todo),
    }
    for nombre_fichero, contenido in versiones.items():
        destino = ap.SALIDA / nombre_fichero
        destino.write_text(f'<!doctype html><meta charset="utf-8"><body style="margin:0;background:{SUPERFICIE}">'
                           f'{contenido}</body>', encoding="utf-8")
        print(destino)
    print(len(f1), len(f2))


if __name__ == "__main__":
    main()
