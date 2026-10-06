# Deadline Math — results

Generated 2026-10-06 22:58 UTC by `benchmark/tablas_en.py` from the runs in `benchmark/resultados/kaggle/`. Pre-registration: [`docs/PREREGISTRATION.md`](../../docs/PREREGISTRATION.md).

**Trap** = the date falls where the usual offset does not hold (EU/US gap week, or a duration crossing a clock change). **Control** = the same sentence, reader, clock time and weekday, with the date moved out of that period. **Penalty** = controls correct − traps correct. **b / c** = pairs with only the control right / only the trap right. **Naive answer** = the usual offset, or adding clock hours.

## Pre-registered result — paired set, 19 of 19 pre-registered models

Primary analysis, exactly as pre-registered (direct mode, one run per model).

| Model | Pairs | Traps correct (95% CI) | Controls correct (95% CI) | Penalty | b / c | McNemar p | Trap errors = naive |
|---|---|---|---|---|---|---|---|
| Claude Haiku 4.5 | 50 | 4% (1%–13%) | 92% (81%–97%) | +88 pts | 46 / 2 | 8.4e-12 | 46/48 |
| Grok 4.20 (non-reasoning) | 50 | 18% (10%–31%) | 96% (87%–99%) | +78 pts | 40 / 1 | 3.8e-11 | 37/41 |
| Gemini 3.1 Flash Lite | 50 | 34% (22%–48%) | 100% (93%–100%) | +66 pts | 33 / 0 | 2.3e-10 | 33/33 |
| Gemini 3.5 Flash Lite | 50 | 34% (22%–48%) | 96% (87%–99%) | +62 pts | 33 / 2 | 3.7e-08 | 33/33 |
| GPT-5.4 mini | 50 | 34% (22%–48%) | 92% (81%–97%) | +58 pts | 31 / 2 | 1.3e-07 | 31/33 |
| GPT-5.4 nano | 50 | 6% (2%–16%) | 58% (44%–71%) | +52 pts | 29 / 3 | 2.6e-06 | 29/47 |
| Qwen3 Coder 480B | 50 | 0% (0%–7%) | 34% (22%–48%) | +34 pts | 17 / 0 | 1.5e-05 | 21/22 |
| Gemini 2.5 Flash | 50 | 62% (48%–74%) | 96% (87%–99%) | +34 pts | 19 / 2 | 0.00022 | 18/18 |
| Qwen3 Next Thinking | 50 | 64% (50%–76%) | 98% (90%–100%) | +34 pts | 18 / 1 | 7.6e-05 | 15/15 |
| GPT-5.6 Luna | 50 | 70% (56%–81%) | 100% (93%–100%) | +30 pts | 15 / 0 | 6.1e-05 | 14/15 |
| Grok 4.20 Reasoning | 50 | 84% (71%–92%) | 100% (93%–100%) | +16 pts | 8 / 0 | 0.0078 | 8/8 |
| Gemma 4 31B | 50 | 90% (79%–96%) | 100% (93%–100%) | +10 pts | 5 / 0 | 0.062 | 5/5 |
| Claude Sonnet 5 | 50 | 96% (87%–99%) | 100% (93%–100%) | +4 pts | 2 / 0 | 0.5 | 2/2 |
| Gemma 4 26B | 50 | 98% (90%–100%) | 98% (90%–100%) | +0 pts | 1 / 1 | 1 | 1/1 |
| Gemini 3 Flash | 50 | 100% (93%–100%) | 100% (93%–100%) | +0 pts | 0 / 0 | 1 | 0/0 |
| Gemini 3.6 Flash | 50 | 100% (93%–100%) | 100% (93%–100%) | +0 pts | 0 / 0 | 1 | 0/0 |
| Gemini 3.7 Flash | 50 | 100% (93%–100%) | 100% (93%–100%) | +0 pts | 0 / 0 | 1 | 0/0 |
| Gemini 3.8 Flash | 50 | 100% (93%–100%) | 100% (93%–100%) | +0 pts | 0 / 0 | 1 | 0/0 |
| GLM-5 | 50 | 100% (93%–100%) | 100% (93%–100%) | +0 pts | 0 / 0 | 1 | 0/0 |

- **H1 holds.** Mean penalty **+29.8 points** (95% bootstrap CI +25.4 to +34.2, 10,000 resamples of the 50 pairs, seed 0). Models with a positive / negative penalty: 13 / 0 (sign test p = 0.00024). Criterion: CI above zero.
- **H2 holds.** 293 of 321 wrong trap answers (91%, Wilson CI 88%–94%) are exactly the naive answer. Criterion: lower bound above 50%. Answers without an `ANSWER` line are not in H2 and count as failures in H1.

| Stratum (descriptive) | Pairs | Traps correct | Controls correct |
|---|---|---|---|
| Conversion, autumn gap (Oct 26–31) | 342 | 70% | 90% |
| Conversion, spring gap (Mar 9–14) | 228 | 74% | 89% |
| Duration across the autumn change | 228 | 50% | 97% |
| Duration across the spring change | 152 | 51% | 97% |

## Replication — second run of the paired set, 18 of 19 pre-registered models

Same models, task version and prompt, run once more at temperature 0. Secondary analysis, logged before running it; the pre-registered result above is the first run.

| Model | Pairs | Traps correct (95% CI) | Controls correct (95% CI) | Penalty | b / c | McNemar p | Trap errors = naive |
|---|---|---|---|---|---|---|---|
| Claude Haiku 4.5 | 50 | 4% (1%–13%) | 90% (79%–96%) | +86 pts | 45 / 2 | 1.6e-11 | 47/48 |
| Grok 4.20 (non-reasoning) | 50 | 18% (10%–31%) | 94% (84%–98%) | +76 pts | 38 / 0 | 7.3e-12 | 39/41 |
| Gemini 3.1 Flash Lite | 50 | 32% (21%–46%) | 98% (90%–100%) | +66 pts | 34 / 1 | 2.1e-09 | 34/34 |
| Gemini 3.5 Flash Lite | 50 | 32% (21%–46%) | 94% (84%–98%) | +62 pts | 34 / 3 | 1.2e-07 | 34/34 |
| GPT-5.4 mini | 50 | 36% (24%–50%) | 94% (84%–98%) | +58 pts | 29 / 0 | 3.7e-09 | 31/32 |
| GPT-5.4 nano | 50 | 4% (1%–13%) | 52% (39%–65%) | +48 pts | 25 / 1 | 8e-07 | 26/48 |
| Qwen3 Coder 480B | 50 | 0% (0%–7%) | 46% (33%–60%) | +46 pts | 23 / 0 | 2.4e-07 | 18/19 |
| GPT-5.6 Luna | 50 | 62% (48%–74%) | 100% (93%–100%) | +38 pts | 19 / 0 | 3.8e-06 | 18/19 |
| Gemini 2.5 Flash | 50 | 60% (46%–72%) | 90% (79%–96%) | +30 pts | 19 / 4 | 0.0026 | 19/20 |
| Grok 4.20 Reasoning | 50 | 80% (67%–89%) | 100% (93%–100%) | +20 pts | 10 / 0 | 0.002 | 10/10 |
| GLM-5 | 50 | 96% (87%–99%) | 98% (90%–100%) | +2 pts | 2 / 1 | 1 | 0/0 |
| Gemma 4 31B | 50 | 98% (90%–100%) | 100% (93%–100%) | +2 pts | 1 / 0 | 1 | 1/1 |
| Claude Sonnet 5 | 50 | 100% (93%–100%) | 100% (93%–100%) | +0 pts | 0 / 0 | 1 | 0/0 |
| Gemini 3 Flash | 50 | 100% (93%–100%) | 100% (93%–100%) | +0 pts | 0 / 0 | 1 | 0/0 |
| Gemini 3.6 Flash | 50 | 100% (93%–100%) | 100% (93%–100%) | +0 pts | 0 / 0 | 1 | 0/0 |
| Gemini 3.7 Flash | 50 | 100% (93%–100%) | 100% (93%–100%) | +0 pts | 0 / 0 | 1 | 0/0 |
| Gemini 3.8 Flash | 50 | 100% (93%–100%) | 100% (93%–100%) | +0 pts | 0 / 0 | 1 | 0/0 |
| Gemma 4 26B | 50 | 100% (93%–100%) | 98% (90%–100%) | -2 pts | 0 / 1 | 1 | 0/0 |

- **H1 holds.** Mean penalty **+29.6 points** (95% bootstrap CI +26.0 to +33.1, 10,000 resamples of the 50 pairs, seed 0). Models with a positive / negative penalty: 12 / 1 (sign test p = 0.0034). Criterion: CI above zero.
- **H2 holds.** 277 of 306 wrong trap answers (91%, Wilson CI 87%–93%) are exactly the naive answer. Criterion: lower bound above 50%. Answers without an `ANSWER` line are not in H2 and count as failures in H1.

| Stratum (descriptive) | Pairs | Traps correct | Controls correct |
|---|---|---|---|
| Conversion, autumn gap (Oct 26–31) | 324 | 67% | 90% |
| Conversion, spring gap (Mar 9–14) | 216 | 69% | 88% |
| Duration across the autumn change | 216 | 54% | 97% |
| Duration across the spring change | 144 | 53% | 94% |

## Secondary extension — paired set, 24 more models

Same set, prompt and analysis on more models once quota allowed. Logged as a deviation before running it; reported separately and not part of the confirmatory claim.

| Model | Pairs | Traps correct (95% CI) | Controls correct (95% CI) | Penalty | b / c | McNemar p | Trap errors = naive |
|---|---|---|---|---|---|---|---|
| Claude Sonnet 4.5 | 50 | 6% (2%–16%) | 100% (93%–100%) | +94 pts | 47 / 0 | 1.4e-14 | 47/47 |
| Qwen3 235B | 50 | 0% (0%–7%) | 88% (76%–94%) | +88 pts | 44 / 0 | 1.1e-13 | 47/50 |
| Qwen3 Next Instruct | 50 | 0% (0%–7%) | 78% (65%–87%) | +78 pts | 39 / 0 | 3.6e-12 | 44/50 |
| Claude Sonnet 4.6 | 50 | 20% (11%–33%) | 96% (87%–99%) | +76 pts | 39 / 1 | 7.5e-11 | 40/40 |
| Claude Opus 4.5 | 50 | 22% (13%–35%) | 82% (69%–90%) | +60 pts | 34 / 4 | 6e-07 | 39/39 |
| Claude Opus 4.6 | 50 | 46% (33%–60%) | 90% (79%–96%) | +44 pts | 24 / 2 | 1e-05 | 26/27 |
| gpt-oss-20b | 50 | 54% (40%–67%) | 94% (84%–98%) | +40 pts | 22 / 2 | 3.6e-05 | 22/23 |
| Claude Opus 4.8 | 50 | 78% (65%–87%) | 100% (93%–100%) | +22 pts | 11 / 0 | 0.00098 | 10/11 |
| Claude Opus 4.7 | 50 | 76% (63%–86%) | 90% (79%–96%) | +14 pts | 12 / 5 | 0.14 | 12/12 |
| GPT-5.4 | 50 | 76% (63%–86%) | 90% (79%–96%) | +14 pts | 11 / 4 | 0.12 | 11/12 |
| GPT-6 Luna | 50 | 86% (74%–93%) | 100% (93%–100%) | +14 pts | 7 / 0 | 0.016 | 7/7 |
| Gemini 2.5 Pro | 50 | 96% (87%–99%) | 100% (93%–100%) | +4 pts | 2 / 0 | 0.5 | 2/2 |
| DeepSeek R1 | 50 | 98% (90%–100%) | 100% (93%–100%) | +2 pts | 1 / 0 | 1 | 1/1 |
| Claude Opus 5.5 | 50 | 100% (93%–100%) | 100% (93%–100%) | +0 pts | 0 / 0 | 1 | 0/0 |
| Claude Sonnet 5.5 | 50 | 100% (93%–100%) | 100% (93%–100%) | +0 pts | 0 / 0 | 1 | 0/0 |
| Gemini 3.1 Pro | 50 | 100% (93%–100%) | 100% (93%–100%) | +0 pts | 0 / 0 | 1 | 0/0 |
| Gemini 3.5 Flash | 50 | 100% (93%–100%) | 100% (93%–100%) | +0 pts | 0 / 0 | 1 | 0/0 |
| GPT-5.5 | 50 | 100% (93%–100%) | 100% (93%–100%) | +0 pts | 0 / 0 | 1 | 0/0 |
| GPT-5.6 Sol | 50 | 100% (93%–100%) | 100% (93%–100%) | +0 pts | 0 / 0 | 1 | 0/0 |
| GPT-6 Astra | 50 | 100% (93%–100%) | 100% (93%–100%) | +0 pts | 0 / 0 | 1 | 0/0 |
| GPT-6 Sol | 50 | 100% (93%–100%) | 100% (93%–100%) | +0 pts | 0 / 0 | 1 | 0/0 |
| GPT-6.1 Sol | 50 | 100% (93%–100%) | 100% (93%–100%) | +0 pts | 0 / 0 | 1 | 0/0 |
| GPT-5.6 Terra | 50 | 100% (93%–100%) | 98% (90%–100%) | -2 pts | 0 / 1 | 1 | 0/0 |
| Claude Opus 5 | 50 | 96% (87%–99%) | 90% (79%–96%) | -6 pts | 2 / 5 | 0.45 | 0/0 |

- **H1 holds.** Mean penalty **+22.6 points** (95% bootstrap CI +19.7 to +25.4, 10,000 resamples of the 50 pairs, seed 0). Models with a positive / negative penalty: 13 / 2 (sign test p = 0.0074). Criterion: CI above zero.
- **H2 holds.** 308 of 321 wrong trap answers (96%, Wilson CI 93%–98%) are exactly the naive answer. Criterion: lower bound above 50%. Answers without an `ANSWER` line are not in H2 and count as failures in H1.

| Stratum (descriptive) | Pairs | Traps correct | Controls correct |
|---|---|---|---|
| Conversion, autumn gap (Oct 26–31) | 432 | 79% | 94% |
| Conversion, spring gap (Mar 9–14) | 288 | 73% | 94% |
| Duration across the autumn change | 288 | 67% | 99% |
| Duration across the spring change | 192 | 70% | 97% |

## The four original tasks — cohort of 43 models

Models with a clean run (every case answered) on all four tasks. Score = correct local time extracted. Latest clean run per model; one run per cell, temperature 0 (runs are not deterministic: see repeatability below).

| Model | Standard, direct | Standard, reasoned | Hard, direct | Hard, reasoned |
|---|---|---|---|---|
| Claude Sonnet 5.5 | 20/20 | 20/20 | 11/11 | 11/11 |
| GPT-5.5 | 20/20 | 20/20 | 11/11 | 11/11 |
| GPT-5.6 Sol | 20/20 | 20/20 | 11/11 | 11/11 |
| GPT-6 Astra | 20/20 | 20/20 | 11/11 | 11/11 |
| GPT-6 Sol | 20/20 | 20/20 | 11/11 | 11/11 |
| GPT-6.1 Sol | 20/20 | 20/20 | 11/11 | 11/11 |
| Gemini 3.1 Pro | 20/20 | 20/20 | 11/11 | 11/11 |
| Gemini 3.5 Flash | 20/20 | 20/20 | 11/11 | 11/11 |
| Gemini 3.6 Flash | 20/20 | 20/20 | 11/11 | 11/11 |
| Gemini 3.8 Flash | 20/20 | 20/20 | 11/11 | 11/11 |
| Gemma 4 31B | 20/20 | 20/20 | 11/11 | 11/11 |
| Grok 4.20 Reasoning | 20/20 | 20/20 | 11/11 | 11/11 |
| Claude Opus 5.5 | 20/20 | 20/20 | 10/11 | 11/11 |
| GLM-5 | 20/20 | 20/20 | 11/11 | 10/11 |
| Gemini 3 Flash | 20/20 | 20/20 | 11/11 | 10/11 |
| Gemini 3.7 Flash | 20/20 | 20/20 | 10/11 | 11/11 |
| Gemma 4 26B | 20/20 | 20/20 | 11/11 | 10/11 |
| GPT-5.6 Terra | 18/20 | 20/20 | 11/11 | 11/11 |
| GPT-6 Luna | 18/20 | 19/20 | 11/11 | 11/11 |
| Claude Sonnet 5 | 20/20 | 20/20 | 9/11 | 11/11 |
| DeepSeek R1 | 20/20 | 20/20 | 10/11 | 10/11 |
| Claude Opus 4.7 | 19/20 | 20/20 | 10/11 | 10/11 |
| Claude Opus 4.8 | 19/20 | 20/20 | 10/11 | 10/11 |
| Claude Opus 5 | 17/20 | 20/20 | 10/11 | 11/11 |
| Gemini 2.5 Pro | 18/20 | 20/20 | 10/11 | 10/11 |
| GPT-5.6 Luna | 19/20 | 20/20 | 9/11 | 9/11 |
| Claude Opus 4.6 | 15/20 | 19/20 | 10/11 | 10/11 |
| Qwen3 Next Thinking | 20/20 | 19/20 | 9/11 | 8/11 |
| gpt-oss-20b | 18/20 | 18/20 | 8/11 | 8/11 |
| Gemini 2.5 Flash | 17/20 | 20/20 | 8/11 | 7/11 |
| Claude Sonnet 4.6 | 16/20 | 20/20 | 6/11 | 8/11 |
| GPT-5.4 | 19/20 | 18/20 | 7/11 | 6/11 |
| Claude Sonnet 4.5 | 15/20 | 20/20 | 3/11 | 9/11 |
| Claude Opus 4.5 | 13/20 | 19/20 | 3/11 | 9/11 |
| Gemini 3.5 Flash Lite | 16/20 | 18/20 | 2/11 | 6/11 |
| Gemini 3.1 Flash Lite | 17/20 | 16/20 | 2/11 | 3/11 |
| GPT-5.4 mini | 12/20 | 16/20 | 2/11 | 4/11 |
| Claude Haiku 4.5 | 9/20 | 17/20 | 1/11 | 6/11 |
| Qwen3 Next Instruct | 7/20 | 16/20 | 1/11 | 6/11 |
| Grok 4.20 (non-reasoning) | 11/20 | 14/20 | 1/11 | 2/11 |
| Qwen3 235B | 7/20 | 13/20 | 1/11 | 4/11 |
| GPT-5.4 nano | 3/20 | 17/20 | 0/11 | 3/11 |
| Qwen3 Coder 480B | 3/20 | 13/20 | 0/11 | 4/11 |

| Condition | Correct | One-line `ANSWER` only |
|---|---|---|
| Standard, direct | 726/860 (84.4%) | 793/860 |
| Standard, reasoned | 812/860 (94.4%) | not required |
| Hard, direct | 339/473 (71.7%) | 424/473 |
| Hard, reasoned | 380/473 (80.3%) | not required |

## Repeatability

106 pairs of clean runs of the same model on the same task (same prompt, temperature 0): right/wrong agreement on **1480/1607 cases (92.1%)**; a model's score changes by **4.4 points on average** between runs, and by up to 36 points.
