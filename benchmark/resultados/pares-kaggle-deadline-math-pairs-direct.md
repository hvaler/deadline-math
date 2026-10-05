# Pares prerregistrados — kaggle deadline-math-pairs-direct

Trampa = la fecha cae donde la diferencia habitual no vale; control = el mismo enunciado fuera de ese periodo. Penalización = acierto en controles − acierto en trampas. IC al 95 %.

| modelo | pares | trampas | controles | penalización | b / c | McNemar p | errores = ingenua |
|---|---|---|---|---|---|---|---|
| anthropic/claude-haiku-4-5@20251001 | 50 | 4% [1%–13%] | 92% [81%–97%] | +88% | 46 / 2 | 8.36e-12 | 46/48 |
| anthropic/claude-sonnet-5@default | 50 | 96% [87%–99%] | 100% [93%–100%] | +4% | 2 / 0 | 0.5 | 2/2 |
| google/gemini-2.5-flash | 50 | 62% [48%–74%] | 96% [87%–99%] | +34% | 19 / 2 | 0.000221 | 18/18 |
| google/gemini-3-flash-preview | 50 | 100% [93%–100%] | 100% [93%–100%] | +0% | 0 / 0 | 1 | 0/0 |
| google/gemini-3.1-flash-lite-preview | 50 | 34% [22%–48%] | 100% [93%–100%] | +66% | 33 / 0 | 2.33e-10 | 33/33 |
| google/gemini-3.5-flash-lite | 50 | 34% [22%–48%] | 96% [87%–99%] | +62% | 33 / 2 | 3.67e-08 | 33/33 |
| google/gemini-3.6-flash | 50 | 100% [93%–100%] | 100% [93%–100%] | +0% | 0 / 0 | 1 | 0/0 |
| google/gemini-3.7-flash | 50 | 100% [93%–100%] | 100% [93%–100%] | +0% | 0 / 0 | 1 | 0/0 |
| google/gemini-3.8-flash | 50 | 100% [93%–100%] | 100% [93%–100%] | +0% | 0 / 0 | 1 | 0/0 |
| google/gemma-4-26b-a4b | 50 | 98% [90%–100%] | 98% [90%–100%] | +0% | 1 / 1 | 1 | 1/1 |
| google/gemma-4-31b | 50 | 90% [79%–96%] | 100% [93%–100%] | +10% | 5 / 0 | 0.0625 | 5/5 |
| openai/gpt-5.4-mini-2026-03-17 | 50 | 34% [22%–48%] | 92% [81%–97%] | +58% | 31 / 2 | 1.31e-07 | 31/33 |
| openai/gpt-5.4-nano-2026-03-17 | 50 | 6% [2%–16%] | 58% [44%–71%] | +52% | 29 / 3 | 2.56e-06 | 29/47 |
| openai/gpt-5.6-luna | 50 | 70% [56%–81%] | 100% [93%–100%] | +30% | 15 / 0 | 6.1e-05 | 14/15 |
| qwen/qwen3-coder-480b-a35b-instruct | 50 | 0% [0%–7%] | 34% [22%–48%] | +34% | 17 / 0 | 1.53e-05 | 21/22 |
| xai/grok-4.20-0309-non-reasoning | 50 | 18% [10%–31%] | 96% [87%–99%] | +78% | 40 / 1 | 3.82e-11 | 37/41 |
| xai/grok-4.20-0309-reasoning | 50 | 84% [71%–92%] | 100% [93%–100%] | +16% | 8 / 0 | 0.00781 | 8/8 |
| zai/glm-5 | 50 | 100% [93%–100%] | 100% [93%–100%] | +0% | 0 / 0 | 1 | 0/0 |

## Hipótesis

- **H1** — penalización media de la cohorte: **+29.6%** (IC bootstrap 95 % +25.4% a +33.7%). Modelos con penalización positiva / negativa: 12 / 0 (prueba de signos p = 0.000488). **Se sostiene** (criterio: IC por encima de cero).
- **H2** — errores en trampas iguales a la respuesta ingenua: **278/306** (91%, IC Wilson 87%–94%). **Se sostiene** (criterio: límite inferior > 50 %). Las respuestas sin línea ANSWER no entran en H2 y se cuentan como fallo en H1.

## Por estrato (descriptivo)

| estrato | pares | trampas | controles |
|---|---|---|---|
| conversion-autumn | 324 | 69% | 90% |
| conversion-spring | 216 | 72% | 89% |
| duration-autumn | 216 | 51% | 97% |
| duration-spring | 144 | 53% | 97% |
