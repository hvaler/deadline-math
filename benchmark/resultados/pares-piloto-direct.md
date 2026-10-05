# Pares prerregistrados — piloto direct

Trampa = la fecha cae donde la diferencia habitual no vale; control = el mismo enunciado fuera de ese periodo. Penalización = acierto en controles − acierto en trampas. IC al 95 %.

| modelo | pares | trampas | controles | penalización | b / c | McNemar p | errores = ingenua |
|---|---|---|---|---|---|---|---|
| google/gemini-3.1-flash-lite-preview | 50 | 32% [21%–46%] | 100% [93%–100%] | +68% | 34 / 0 | 1.16e-10 | 34/34 |
| openai/gpt-5.4-nano-2026-03-17 | 50 | 6% [2%–16%] | 54% [40%–67%] | +48% | 24 / 0 | 1.19e-07 | 23/47 |

## Hipótesis

- **H1** — penalización media de la cohorte: **+58.0%** (IC bootstrap 95 % +47.0% a +68.0%). Modelos con penalización positiva / negativa: 2 / 0 (prueba de signos p = 0.5). **Se sostiene** (criterio: IC por encima de cero).
- **H2** — errores en trampas iguales a la respuesta ingenua: **57/81** (70%, IC Wilson 60%–79%). **Se sostiene** (criterio: límite inferior > 50 %). Las respuestas sin línea ANSWER no entran en H2 y se cuentan como fallo en H1.

## Por estrato (descriptivo)

| estrato | pares | trampas | controles |
|---|---|---|---|
| conversion-autumn | 36 | 28% | 64% |
| conversion-spring | 24 | 38% | 75% |
| duration-autumn | 24 | 0% | 83% |
| duration-spring | 16 | 0% | 100% |
