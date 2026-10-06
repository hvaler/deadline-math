# Pares prerregistrados — kaggle deadline-math-pairs-direct

Trampa = la fecha cae donde la diferencia habitual no vale; control = el mismo enunciado fuera de ese periodo. Penalización = acierto en controles − acierto en trampas. IC al 95 %.

| modelo | pares | trampas | controles | penalización | b / c | McNemar p | errores = ingenua |
|---|---|---|---|---|---|---|---|
| anthropic/claude-haiku-4-5@20251001 | 50 | 4% [1%–13%] | 92% [81%–97%] | +88% | 46 / 2 | 8.36e-12 | 46/48 |
| anthropic/claude-opus-4-5@20251101 | 50 | 22% [13%–35%] | 82% [69%–90%] | +60% | 34 / 4 | 6.04e-07 | 39/39 |
| anthropic/claude-opus-4-6@default | 50 | 46% [33%–60%] | 90% [79%–96%] | +44% | 24 / 2 | 1.05e-05 | 26/27 |
| anthropic/claude-opus-4-7@default | 50 | 76% [63%–86%] | 90% [79%–96%] | +14% | 12 / 5 | 0.143 | 12/12 |
| anthropic/claude-opus-4-8@default | 50 | 78% [65%–87%] | 100% [93%–100%] | +22% | 11 / 0 | 0.000977 | 10/11 |
| anthropic/claude-opus-5@default | 50 | 96% [87%–99%] | 90% [79%–96%] | -6% | 2 / 5 | 0.453 | 0/0 |
| anthropic/claude-sonnet-4-5@20250929 | 50 | 6% [2%–16%] | 100% [93%–100%] | +94% | 47 / 0 | 1.42e-14 | 47/47 |
| anthropic/claude-sonnet-5@default | 50 | 96% [87%–99%] | 100% [93%–100%] | +4% | 2 / 0 | 0.5 | 2/2 |
| deepseek-ai/deepseek-r1-0528 | 50 | 98% [90%–100%] | 100% [93%–100%] | +2% | 1 / 0 | 1 | 1/1 |
| google/gemini-2.5-flash | 50 | 62% [48%–74%] | 96% [87%–99%] | +34% | 19 / 2 | 0.000221 | 18/18 |
| google/gemini-2.5-pro | 50 | 96% [87%–99%] | 100% [93%–100%] | +4% | 2 / 0 | 0.5 | 2/2 |
| google/gemini-3-flash-preview | 50 | 100% [93%–100%] | 100% [93%–100%] | +0% | 0 / 0 | 1 | 0/0 |
| google/gemini-3.1-flash-lite-preview | 50 | 34% [22%–48%] | 100% [93%–100%] | +66% | 33 / 0 | 2.33e-10 | 33/33 |
| google/gemini-3.1-pro-preview | 50 | 100% [93%–100%] | 100% [93%–100%] | +0% | 0 / 0 | 1 | 0/0 |
| google/gemini-3.5-flash | 50 | 100% [93%–100%] | 100% [93%–100%] | +0% | 0 / 0 | 1 | 0/0 |
| google/gemini-3.5-flash-lite | 50 | 34% [22%–48%] | 96% [87%–99%] | +62% | 33 / 2 | 3.67e-08 | 33/33 |
| google/gemini-3.6-flash | 50 | 100% [93%–100%] | 100% [93%–100%] | +0% | 0 / 0 | 1 | 0/0 |
| google/gemini-3.7-flash | 50 | 100% [93%–100%] | 100% [93%–100%] | +0% | 0 / 0 | 1 | 0/0 |
| google/gemini-3.8-flash | 50 | 100% [93%–100%] | 100% [93%–100%] | +0% | 0 / 0 | 1 | 0/0 |
| google/gemma-4-26b-a4b | 50 | 98% [90%–100%] | 98% [90%–100%] | +0% | 1 / 1 | 1 | 1/1 |
| google/gemma-4-31b | 50 | 90% [79%–96%] | 100% [93%–100%] | +10% | 5 / 0 | 0.0625 | 5/5 |
| openai/gpt-5.4-2026-03-05 | 50 | 76% [63%–86%] | 90% [79%–96%] | +14% | 11 / 4 | 0.118 | 11/12 |
| openai/gpt-5.4-mini-2026-03-17 | 50 | 34% [22%–48%] | 92% [81%–97%] | +58% | 31 / 2 | 1.31e-07 | 31/33 |
| openai/gpt-5.4-nano-2026-03-17 | 50 | 6% [2%–16%] | 58% [44%–71%] | +52% | 29 / 3 | 2.56e-06 | 29/47 |
| openai/gpt-5.5-2026-04-23 | 50 | 100% [93%–100%] | 100% [93%–100%] | +0% | 0 / 0 | 1 | 0/0 |
| openai/gpt-5.6-luna | 50 | 70% [56%–81%] | 100% [93%–100%] | +30% | 15 / 0 | 6.1e-05 | 14/15 |
| openai/gpt-5.6-sol | 50 | 100% [93%–100%] | 100% [93%–100%] | +0% | 0 / 0 | 1 | 0/0 |
| openai/gpt-5.6-terra | 50 | 100% [93%–100%] | 98% [90%–100%] | -2% | 0 / 1 | 1 | 0/0 |
| openai/gpt-6-astra | 50 | 100% [93%–100%] | 100% [93%–100%] | +0% | 0 / 0 | 1 | 0/0 |
| openai/gpt-oss-20b | 50 | 54% [40%–67%] | 94% [84%–98%] | +40% | 22 / 2 | 3.59e-05 | 22/23 |
| qwen/qwen3-235b-a22b-instruct-2507 | 50 | 0% [0%–7%] | 88% [76%–94%] | +88% | 44 / 0 | 1.14e-13 | 47/50 |
| qwen/qwen3-coder-480b-a35b-instruct | 50 | 0% [0%–7%] | 34% [22%–48%] | +34% | 17 / 0 | 1.53e-05 | 21/22 |
| qwen/qwen3-next-80b-a3b-instruct | 50 | 0% [0%–7%] | 78% [65%–87%] | +78% | 39 / 0 | 3.64e-12 | 44/50 |
| qwen/qwen3-next-80b-a3b-thinking | 50 | 64% [50%–76%] | 98% [90%–100%] | +34% | 18 / 1 | 7.63e-05 | 15/15 |
| xai/grok-4.20-0309-non-reasoning | 50 | 18% [10%–31%] | 96% [87%–99%] | +78% | 40 / 1 | 3.82e-11 | 37/41 |
| xai/grok-4.20-0309-reasoning | 50 | 84% [71%–92%] | 100% [93%–100%] | +16% | 8 / 0 | 0.00781 | 8/8 |
| zai/glm-5 | 50 | 100% [93%–100%] | 100% [93%–100%] | +0% | 0 / 0 | 1 | 0/0 |

## Hipótesis

- **H1** — penalización media de la cohorte: **+27.5%** (IC bootstrap 95 % +24.1% a +31.1%). Modelos con penalización positiva / negativa: 24 / 2 (prueba de signos p = 1.05e-05). **Se sostiene** (criterio: IC por encima de cero).
- **H2** — errores en trampas iguales a la respuesta ingenua: **554/595** (93%, IC Wilson 91%–95%). **Se sostiene** (criterio: límite inferior > 50 %). Las respuestas sin línea ANSWER no entran en H2 y se cuentan como fallo en H1.

## Por estrato (descriptivo)

| estrato | pares | trampas | controles |
|---|---|---|---|
| conversion-autumn | 666 | 73% | 91% |
| conversion-spring | 444 | 71% | 91% |
| duration-autumn | 444 | 56% | 98% |
| duration-spring | 296 | 58% | 97% |
