# Cifras del artículo (2026-10-07 00:57)

## Cohorte de las 4 tasks: 43 modelos

- deadline-math-direct: 726/860 (84.4%); una sola línea ANSWER 793/860
- deadline-math-reasoned: 812/860 (94.4%); una sola línea ANSWER 13/860
- deadline-math-hard-direct: 339/473 (71.7%); una sola línea ANSWER 424/473
- deadline-math-hard-reasoned: 380/473 (80.3%); una sola línea ANSWER 11/473

## Estándar directo: 20 de 43 completados con 20/20

anthropic/claude-opus-5-5@default, anthropic/claude-sonnet-5-5@default, anthropic/claude-sonnet-5@default, deepseek-ai/deepseek-r1-0528, google/gemini-3-flash-preview, google/gemini-3.1-pro-preview, google/gemini-3.5-flash, google/gemini-3.6-flash, google/gemini-3.7-flash, google/gemini-3.8-flash, google/gemma-4-26b-a4b, google/gemma-4-31b, openai/gpt-5.5-2026-04-23, openai/gpt-5.6-sol, openai/gpt-6-astra, openai/gpt-6-sol, openai/gpt-6.1-sol, qwen/qwen3-next-80b-a3b-thinking, xai/grok-4.20-0309-reasoning, zai/glm-5

## Directo frente a razonado (estándar), por modelo de la cohorte

- anthropic/claude-haiku-4-5@20251001: 9/20 -> 17/20
- anthropic/claude-opus-4-5@20251101: 13/20 -> 19/20
- anthropic/claude-sonnet-4-5@20250929: 15/20 -> 20/20
- openai/gpt-5.4-nano-2026-03-17: 3/20 -> 17/20
- qwen/qwen3-235b-a22b-instruct-2507: 7/20 -> 13/20
- qwen/qwen3-coder-480b-a35b-instruct: 3/20 -> 13/20
- qwen/qwen3-next-80b-a3b-instruct: 7/20 -> 16/20

## Tamaño del error en las respuestas equivocadas (cohorte, 4 tasks)

- total: 235/382 (62%) exactamente una hora
- base: 5/10
- day-rollover: 5/21
- described-date: 19/42
- dst-gap-autumn: 51/52
- dst-gap-spring: 18/20
- duration: 56/71
- machine-format: 24/66
- offsets: 31/45
- relative-date: 18/25
- traveling: 4/14
- wording: 4/16

## Nivel difícil: respuestas equivocadas repetidas

- deadline-math-hard-direct h-fmt-1 (correcta 2026-10-12 15:59): {'2026-10-11 15:59': 5, '2026-10-23 10:39': 1, '2026-10-12 12:59': 1} de 20
- deadline-math-hard-direct h-fmt-2 (correcta 2026-10-25 03:30): {'2026-10-25 04:30': 12} de 12
- deadline-math-hard-reasoned h-fmt-1 (correcta 2026-10-12 15:59): {'2026-10-11 15:59': 7, '2026-06-16 12:59': 1, '2026-10-12 08:59': 1} de 22
- deadline-math-hard-reasoned h-fmt-2 (correcta 2026-10-25 03:30): {'2026-10-25 04:30': 11, '2026-10-25 02:30': 1} de 12

## Repetibilidad: dos ejecuciones limpias del mismo modelo y task (mismo prompt, temperatura 0)

- 106 pares de ejecuciones; acierto/fallo igual en 1480/1607 casos (92.1%)
- diferencia de acierto entre ejecuciones: media 4.4%, máxima 36.4%

## Pares — prerregistrados (19 de 19 completaron)

# Pares prerregistrados — prerregistrados

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
| qwen/qwen3-next-80b-a3b-thinking | 50 | 64% [50%–76%] | 98% [90%–100%] | +34% | 18 / 1 | 7.63e-05 | 15/15 |
| xai/grok-4.20-0309-non-reasoning | 50 | 18% [10%–31%] | 96% [87%–99%] | +78% | 40 / 1 | 3.82e-11 | 37/41 |
| xai/grok-4.20-0309-reasoning | 50 | 84% [71%–92%] | 100% [93%–100%] | +16% | 8 / 0 | 0.00781 | 8/8 |
| zai/glm-5 | 50 | 100% [93%–100%] | 100% [93%–100%] | +0% | 0 / 0 | 1 | 0/0 |

## Hipótesis

- **H1** — penalización media de la cohorte: **+29.8%** (IC bootstrap 95 % +25.4% a +34.2%). Modelos con penalización positiva / negativa: 13 / 0 (prueba de signos p = 0.000244). **Se sostiene** (criterio: IC por encima de cero).
- **H2** — errores en trampas iguales a la respuesta ingenua: **293/321** (91%, IC Wilson 88%–94%). **Se sostiene** (criterio: límite inferior > 50 %). Las respuestas sin línea ANSWER no entran en H2 y se cuentan como fallo en H1.

## Por estrato (descriptivo)

| estrato | pares | trampas | controles |
|---|---|---|---|
| conversion-autumn | 342 | 70% | 90% |
| conversion-spring | 228 | 74% | 89% |
| duration-autumn | 228 | 50% | 97% |
| duration-spring | 152 | 51% | 97% |


## Pares — réplica de los prerregistrados (18 de 19 con segunda ejecución)

# Pares prerregistrados — réplica

Trampa = la fecha cae donde la diferencia habitual no vale; control = el mismo enunciado fuera de ese periodo. Penalización = acierto en controles − acierto en trampas. IC al 95 %.

| modelo | pares | trampas | controles | penalización | b / c | McNemar p | errores = ingenua |
|---|---|---|---|---|---|---|---|
| anthropic/claude-haiku-4-5@20251001 | 50 | 4% [1%–13%] | 90% [79%–96%] | +86% | 45 / 2 | 1.6e-11 | 47/48 |
| anthropic/claude-sonnet-5@default | 50 | 100% [93%–100%] | 100% [93%–100%] | +0% | 0 / 0 | 1 | 0/0 |
| google/gemini-2.5-flash | 50 | 60% [46%–72%] | 90% [79%–96%] | +30% | 19 / 4 | 0.0026 | 19/20 |
| google/gemini-3-flash-preview | 50 | 100% [93%–100%] | 100% [93%–100%] | +0% | 0 / 0 | 1 | 0/0 |
| google/gemini-3.1-flash-lite-preview | 50 | 32% [21%–46%] | 98% [90%–100%] | +66% | 34 / 1 | 2.1e-09 | 34/34 |
| google/gemini-3.5-flash-lite | 50 | 32% [21%–46%] | 94% [84%–98%] | +62% | 34 / 3 | 1.23e-07 | 34/34 |
| google/gemini-3.6-flash | 50 | 100% [93%–100%] | 100% [93%–100%] | +0% | 0 / 0 | 1 | 0/0 |
| google/gemini-3.7-flash | 50 | 100% [93%–100%] | 100% [93%–100%] | +0% | 0 / 0 | 1 | 0/0 |
| google/gemini-3.8-flash | 50 | 100% [93%–100%] | 100% [93%–100%] | +0% | 0 / 0 | 1 | 0/0 |
| google/gemma-4-26b-a4b | 50 | 100% [93%–100%] | 98% [90%–100%] | -2% | 0 / 1 | 1 | 0/0 |
| google/gemma-4-31b | 50 | 98% [90%–100%] | 100% [93%–100%] | +2% | 1 / 0 | 1 | 1/1 |
| openai/gpt-5.4-mini-2026-03-17 | 50 | 36% [24%–50%] | 94% [84%–98%] | +58% | 29 / 0 | 3.73e-09 | 31/32 |
| openai/gpt-5.4-nano-2026-03-17 | 50 | 4% [1%–13%] | 52% [39%–65%] | +48% | 25 / 1 | 8.05e-07 | 26/48 |
| openai/gpt-5.6-luna | 50 | 62% [48%–74%] | 100% [93%–100%] | +38% | 19 / 0 | 3.81e-06 | 18/19 |
| qwen/qwen3-coder-480b-a35b-instruct | 50 | 0% [0%–7%] | 46% [33%–60%] | +46% | 23 / 0 | 2.38e-07 | 18/19 |
| xai/grok-4.20-0309-non-reasoning | 50 | 18% [10%–31%] | 94% [84%–98%] | +76% | 38 / 0 | 7.28e-12 | 39/41 |
| xai/grok-4.20-0309-reasoning | 50 | 80% [67%–89%] | 100% [93%–100%] | +20% | 10 / 0 | 0.00195 | 10/10 |
| zai/glm-5 | 50 | 96% [87%–99%] | 98% [90%–100%] | +2% | 2 / 1 | 1 | 0/0 |

## Hipótesis

- **H1** — penalización media de la cohorte: **+29.6%** (IC bootstrap 95 % +26.0% a +33.1%). Modelos con penalización positiva / negativa: 12 / 1 (prueba de signos p = 0.00342). **Se sostiene** (criterio: IC por encima de cero).
- **H2** — errores en trampas iguales a la respuesta ingenua: **277/306** (91%, IC Wilson 87%–93%). **Se sostiene** (criterio: límite inferior > 50 %). Las respuestas sin línea ANSWER no entran en H2 y se cuentan como fallo en H1.

## Por estrato (descriptivo)

| estrato | pares | trampas | controles |
|---|---|---|---|
| conversion-autumn | 324 | 67% | 90% |
| conversion-spring | 216 | 69% | 88% |
| duration-autumn | 216 | 54% | 97% |
| duration-spring | 144 | 53% | 94% |


## Pares — ampliación, análisis secundario (24 modelos)

# Pares prerregistrados — ampliación

Trampa = la fecha cae donde la diferencia habitual no vale; control = el mismo enunciado fuera de ese periodo. Penalización = acierto en controles − acierto en trampas. IC al 95 %.

| modelo | pares | trampas | controles | penalización | b / c | McNemar p | errores = ingenua |
|---|---|---|---|---|---|---|---|
| anthropic/claude-opus-4-5@20251101 | 50 | 22% [13%–35%] | 82% [69%–90%] | +60% | 34 / 4 | 6.04e-07 | 39/39 |
| anthropic/claude-opus-4-6@default | 50 | 46% [33%–60%] | 90% [79%–96%] | +44% | 24 / 2 | 1.05e-05 | 26/27 |
| anthropic/claude-opus-4-7@default | 50 | 76% [63%–86%] | 90% [79%–96%] | +14% | 12 / 5 | 0.143 | 12/12 |
| anthropic/claude-opus-4-8@default | 50 | 78% [65%–87%] | 100% [93%–100%] | +22% | 11 / 0 | 0.000977 | 10/11 |
| anthropic/claude-opus-5-5@default | 50 | 100% [93%–100%] | 100% [93%–100%] | +0% | 0 / 0 | 1 | 0/0 |
| anthropic/claude-opus-5@default | 50 | 96% [87%–99%] | 90% [79%–96%] | -6% | 2 / 5 | 0.453 | 0/0 |
| anthropic/claude-sonnet-4-5@20250929 | 50 | 6% [2%–16%] | 100% [93%–100%] | +94% | 47 / 0 | 1.42e-14 | 47/47 |
| anthropic/claude-sonnet-4-6@default | 50 | 20% [11%–33%] | 96% [87%–99%] | +76% | 39 / 1 | 7.46e-11 | 40/40 |
| anthropic/claude-sonnet-5-5@default | 50 | 100% [93%–100%] | 100% [93%–100%] | +0% | 0 / 0 | 1 | 0/0 |
| deepseek-ai/deepseek-r1-0528 | 50 | 98% [90%–100%] | 100% [93%–100%] | +2% | 1 / 0 | 1 | 1/1 |
| google/gemini-2.5-pro | 50 | 96% [87%–99%] | 100% [93%–100%] | +4% | 2 / 0 | 0.5 | 2/2 |
| google/gemini-3.1-pro-preview | 50 | 100% [93%–100%] | 100% [93%–100%] | +0% | 0 / 0 | 1 | 0/0 |
| google/gemini-3.5-flash | 50 | 100% [93%–100%] | 100% [93%–100%] | +0% | 0 / 0 | 1 | 0/0 |
| openai/gpt-5.4-2026-03-05 | 50 | 76% [63%–86%] | 90% [79%–96%] | +14% | 11 / 4 | 0.118 | 11/12 |
| openai/gpt-5.5-2026-04-23 | 50 | 100% [93%–100%] | 100% [93%–100%] | +0% | 0 / 0 | 1 | 0/0 |
| openai/gpt-5.6-sol | 50 | 100% [93%–100%] | 100% [93%–100%] | +0% | 0 / 0 | 1 | 0/0 |
| openai/gpt-5.6-terra | 50 | 100% [93%–100%] | 98% [90%–100%] | -2% | 0 / 1 | 1 | 0/0 |
| openai/gpt-6-astra | 50 | 100% [93%–100%] | 100% [93%–100%] | +0% | 0 / 0 | 1 | 0/0 |
| openai/gpt-6-luna | 50 | 86% [74%–93%] | 100% [93%–100%] | +14% | 7 / 0 | 0.0156 | 7/7 |
| openai/gpt-6-sol | 50 | 100% [93%–100%] | 100% [93%–100%] | +0% | 0 / 0 | 1 | 0/0 |
| openai/gpt-6.1-sol | 50 | 100% [93%–100%] | 100% [93%–100%] | +0% | 0 / 0 | 1 | 0/0 |
| openai/gpt-oss-20b | 50 | 54% [40%–67%] | 94% [84%–98%] | +40% | 22 / 2 | 3.59e-05 | 22/23 |
| qwen/qwen3-235b-a22b-instruct-2507 | 50 | 0% [0%–7%] | 88% [76%–94%] | +88% | 44 / 0 | 1.14e-13 | 47/50 |
| qwen/qwen3-next-80b-a3b-instruct | 50 | 0% [0%–7%] | 78% [65%–87%] | +78% | 39 / 0 | 3.64e-12 | 44/50 |

## Hipótesis

- **H1** — penalización media de la cohorte: **+22.6%** (IC bootstrap 95 % +19.7% a +25.4%). Modelos con penalización positiva / negativa: 13 / 2 (prueba de signos p = 0.00739). **Se sostiene** (criterio: IC por encima de cero).
- **H2** — errores en trampas iguales a la respuesta ingenua: **308/321** (96%, IC Wilson 93%–98%). **Se sostiene** (criterio: límite inferior > 50 %). Las respuestas sin línea ANSWER no entran en H2 y se cuentan como fallo en H1.

## Por estrato (descriptivo)

| estrato | pares | trampas | controles |
|---|---|---|---|
| conversion-autumn | 432 | 79% | 94% |
| conversion-spring | 288 | 73% | 94% |
| duration-autumn | 288 | 67% | 99% |
| duration-spring | 192 | 70% | 97% |

