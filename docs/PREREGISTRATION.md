# Pre-registration — paired confirmatory set (Deadline Math)

> **Translation note.** English translation made on 2026-10-05. The authoritative text is the Spanish original,
> [`preregistro-original-es.md`](preregistro-original-es.md), kept exactly as written. Public evidence that the
> design was fixed before the run: the task notebook `deadline-math-pairs-direct` v1, with all 100 cases and the
> generator, was published on Kaggle at ~07:07 UTC on 2026-10-04; the confirmatory runs were scheduled at 07:09 UTC.

**Written on 2026-10-04 at 06:53 UTC (08:53 Madrid), before generating the cases and before running any of them.**
It will not be edited after the first run. Any later change goes in a dated "Deviations" section at the end, with
its reason.

## Why

The 31 existing cases are **exploratory**: the hard set was designed after seeing where models failed. What we saw
there (2026-10-03, 19-model cohort, 321 wrong answers) was that 60% of the errors were **exactly one hour**: 38 of
39 in the autumn gap week; on durations crossing a clock change, 47 of 63 were +1 h. This set exists to **confirm or
refute** that with a design fixed in advance, not to look for new failures.

## Hypotheses

- **H1 (clock-change penalty).** For the same sentence, models are less accurate when the date falls in a period
  where the usual offset does not hold (gap week, or a duration that crosses a clock change) than when the same date
  is moved out of that period.
- **H2 (the failure is mechanical).** Among wrong answers to trap cases, **more than half are exactly the "naive
  answer"**: the one obtained by applying the offset of the control dates (conversions) or by adding clock hours
  (durations).

## Design

- **Matched pairs.** Each trap case has a control twin with the same text, the same reader, the same clock time and
  the same weekday; only the date changes, moved out of the problematic period:
  - autumn conversions: trap between Oct 26 and 31, 2026; control 7 days earlier (Oct 19–24, both sides on summer
    time);
  - spring conversions: trap between Mar 9 and 14, 2026; control 21 days later (Mar 30–Apr 4, both on summer time);
  - durations (24, 48 and 72 h): the trap crosses a clock change in the event's zone; the control starts 7 days
    earlier and crosses none.
- **Varying factors**: zone pair (US Pacific and Eastern versus Madrid, London, Berlin and Paris — *see deviations:
  Paris was not used*), direction (US→Europe and Europe→US), time of day (including times that change the date),
  season (autumn and spring) and duration.
- **Zones by generic name** ("PT", "ET", "London time"), never by abbreviations that fix the offset (PDT, CEST): the
  model has to know which rule applies that day.
- **Correct answer** computed with `zoneinfo` and checked against a **second, independent oracle** written by hand
  from the US and EU clock-change rules. If they disagree on a single case, nothing runs.
- **The generator checks every pair**: on the trap, the offset (or the offset at the end of the duration) differs
  from the control's; on the control, the naive answer equals the correct one.
- **Prompt**: the current direct-mode prompt (`PROMPTS["direct"]`). Reasoned mode only if quota is left over, as a
  secondary analysis.
- **Models**: the 19-model cohort of `benchmark/resultados/tabla-cohorte.md` (2026-10-03). If any cannot run for
  infrastructure reasons, it is reported as "not completed".
- **One run per model**, temperature 0 (the SDK default).

## Measures and analysis

- Per model: accuracy on traps and on controls, with 95% Wilson intervals; **penalty** = control accuracy − trap
  accuracy; exact McNemar test on discordant pairs.
- Aggregate: mean penalty of the cohort with a bootstrap interval over pairs; number of models with positive,
  negative and zero penalty (sign test).
- H2: share of trap errors equal to the naive answer, with a Wilson interval. **H2 holds if the lower bound exceeds
  50%.**
- **H1 holds** if the aggregate penalty is positive with an interval that excludes zero.
- Reported separately by season, type (conversion or duration) and direction. These are descriptions, not new tests.
- **Exclusions**: cases with no answer because of infrastructure (403/404/429/503) remove the whole pair. Answers
  without an `ANSWER` line count as failures and are reported separately. No other exclusions.
- **The result is published whatever it is**, including if H1 or H2 does not hold.

## Schedule

Generation and local pilot, Oct 4. Kaggle run, Oct 5–6 if quota allows. **Data freeze: Wednesday Oct 7.** Article,
Oct 8–10. Publication, Sunday Oct 11.

## Deviations

- **2026-10-04 07:58 UTC — Extension to more models (secondary analysis).** Written before running it. After the
  confirmatory run, the cohort of the 4 tasks grew from 19 to 33 models when quota was restored. The pairs set is also
  run on the 14 new models (among them Claude Opus 4.x, GPT-5.5, GPT-5.6 Sol/Terra and Gemini 3.1 Pro), with the same
  prompt, task version and analysis. **The primary result remains the 19 pre-registered models**; the extension is
  reported separately and without changing the H1 and H2 criteria. Reason: without it we cannot tell whether the
  most expensive models fall into the same trap. Qwen3 Next 80B Thinking, which did not complete because of a 429, is
  also retried.
- **2026-10-05 08:09 UTC — Discrepancies found while translating** (they change no result):
  - The design lists the European zones as "Madrid, London, Berlin and Paris", but the generator (fixed and
    published before running) uses Madrid, London and Berlin: **Paris appears in no case**.
  - The schedule planned the Kaggle run for Oct 5–6; the confirmatory run happened on Oct 4, as soon as quota was
    restored.

## Execution log (does not change the plan)

- 2026-10-04 ~07:00 UTC — **Local pilot to validate the design** (not part of the confirmatory analysis): Gemini 3.1
  Flash Lite and GPT-5.4 nano, direct mode, 100 cases each. Flash Lite: traps 32%, controls 100%, 34/34 errors equal
  to the naive answer. Nano: traps 6%, controls 54%, 23/47. No infrastructure or format problem that required
  changing the design. Report: `benchmark/resultados/pares-piloto-direct.md`.
- **Data freeze moved to Wednesday Oct 7** (was Tuesday Oct 6) to make room for the pairs set.
- 2026-10-04 ~07:15–07:45 UTC — **Confirmatory run** on Kaggle (`deadline-math-pairs-direct` v1), 19-model cohort. 18
  complete; Qwen3 Next 80B Thinking ends with an infrastructure error (429 on `pc-aut-11-C`) and is "not completed".
  Result (`benchmark/resultados/pares-kaggle-deadline-math-pairs-direct.md`):
  - **H1 holds**: mean penalty +29.6% (95% bootstrap CI +25.4% to +33.7%); 12 models with positive penalty, 0
    negative, 6 with no difference (sign test p = 0.0005).
  - **H2 holds**: 278 of 306 trap errors (91%, Wilson CI 87–94%) are exactly the naive answer.
  - Process note: the first download was incomplete (9 of 18); the analysis was repeated on the complete download.
    The figures above are from the complete download.
- 2026-10-04 ~19:45 UTC — **Extension (secondary)**: 8 of 14 models complete before quota runs out again (403); Qwen3
  Next Thinking fails again (503). H1 and H2 also hold in the extension: penalty +25.5% (CI +20.5% to +30.5%), 118/121
  naive errors (98%). Notable: Claude Sonnet 4.5 (traps 6%, controls 100%, 47/47 naive) and no penalty for GPT-5.5,
  GPT-5.6 Sol and GPT-5.6 Terra. Pending for Oct 5: Opus 4.5 and 4.8, GPT-6 Astra, Gemini 2.5 Pro, 3.1 Pro and 3.5
  Flash, Qwen3 Next Thinking.
- 2026-10-05 ~07:50 UTC — **Extension (secondary), completed**: 14 models. H1: penalty +20.7% (CI +16.6% to +24.7%), 8
  positive / 1 negative. H2: 169/173 naive errors (98%). Claude Opus 4.5 22% / 82%, Sonnet 4.5 6% / 100%, Opus 4.8
  78% / 100%; GPT-5.5, GPT-5.6 Sol/Terra, GPT-6 Astra, Gemini 3.1 Pro and 3.5 Flash with no penalty. The 4 models of the
  public benchmark that did not have it yet (Qwen3 Next Instruct, DeepSeek R1, Qwen3 235B, Claude Opus 5) are added to
  the extension, with the same criteria.
- 2026-10-06 ~07:03 UTC — **Final retry.** Qwen3 Next 80B Thinking completes the pairs: **the pre-registered result
  now covers 19 of 19 models.** Recomputed with the same analysis:
  - **H1 holds**: mean penalty +29.8% (95% bootstrap CI +25.4% to +34.2%); 13 models with a positive penalty, 0
    negative (sign test p = 0.00024).
  - **H2 holds**: 293 of 321 trap errors (91%, Wilson CI 88–94%) are the naive answer.
  - The 18-model figures logged on Oct 4 (+29.6%; 278/306) are superseded by these; the verdict does not change.
  Extension (secondary), now 18 models (adding Qwen3 Next Instruct, DeepSeek R1, Qwen3 235B and Claude Opus 5):
  penalty +25.1% (CI +21.7% to +28.3%), 11 positive / 2 negative; 261/274 naive errors (95%). Claude Opus 5 comes out
  at −6 points (traps 96%, controls 90%; McNemar p = 0.45, not significant).
- **2026-10-06 — Data freeze.** No further runs.
- **2026-10-06 18:32 UTC — Data freeze reopened (deviation, written before running).** Kaggle added 5 models after Oct 3 (Claude Opus 5.5, Claude Sonnet 5.5, GPT-6 Luna, GPT-6 Sol, GPT-6.1 Sol). All 5 tasks run on them with the same task versions. The pre-registered result (19 models) does not change; their pairs join the secondary extension. Also retried: gpt-oss-120b, Grok 4.5/4.6 (404 again, excluded), and cells whose latest run had failed on infrastructure (the public leaderboard shows those as 0).
- **2026-10-06 19:14 UTC — Replication (secondary, written before running).** The pairs set is run once more on the 19 pre-registered models (same task version, prompt, temperature 0). The primary result stays the first clean run of each model; the replication is analysed separately with the same H1/H2 criteria and reported whatever it shows.
- 2026-10-07 ~01:00 UTC — **Results.**
  - **Replication: H1 and H2 replicate.** 18 of 19 models (Qwen3 Next Thinking failed every retry with 429): penalty +29.6% (CI +26.0% to +33.1%); 277/306 naive errors (91%).
  - Extension (secondary), now 24 models: penalty +22.6% (CI +19.7% to +25.4%); 308/321 (96%). Claude Opus 5.5, Sonnet 5.5, GPT-6 Sol and GPT-6.1 Sol: 100% on traps and controls; GPT-6 Luna 86% / 100%.
  - 4-task cohort: 43 models. Excluded: gpt-oss-120b (two runs hung) and Grok 4.5/4.6 (404).
- **2026-10-07 — New data freeze.** No further runs.
  - 2026-10-07 01:10 UTC: gpt-oss-120b finished the standard direct task after the data freeze (download at 01:00); it is not in the cohort, but it is visible on the leaderboard.
