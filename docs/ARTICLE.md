> Archival copy of the write-up as published on DEV on 2026-10-07. The canonical version is
> https://dev.to/hugo_valer_79d0d94e00804b/the-model-knew-the-rule-it-still-used-last-weeks-offset-584m

# The model knew the rule. It still used last week's offset.

*This is a submission for the [Kaggle Benchmarking Challenge](https://dev.to/challenges/kaggle-2026-09-23)*

*A Kaggle benchmark about the most boring bug I know: converting a deadline into your own time zone. In the opening example, the two dates are one week apart; the measured result comes from 50 pre-registered trap/control pairs (controls moved 7 or 21 days out of the clock-change gap, plus durations that do or do not cross a clock change).*

This contest closes on **October 11, 2026, at 11:59 PM PDT**. I live in Madrid, so for me it closes on **Monday, October 12, at 08:59**. That is the kind of conversion I no longer trust myself to do by hand, so I asked 46 models to do it for me, plus 130 variations of it.

The headline is not that models get time zones wrong. It is *how* they get them wrong: in a pre-registered test, of the 321 wrong answers on trap dates that contained a time, **293 (91%) were exactly the answer you get by applying the usual offset** (or by adding clock hours across a clock change). Some models even state the correct rule in their reasoning and then ignore it.

**In short:** across **50 trap/control pairs**, the trap version of a sentence (a date inside the weeks when Europe and the US change clocks on different dates, or a duration that crosses a clock change) costs the 19 pre-registered models **29.8 points** of accuracy on average compared with its control (95% CI +25.4 to +34.2); 13 of them get worse and none get better. The engineering recommendation that follows: let the model extract the date, time, and zone, and let a time-zone library do the arithmetic. (I did not compare prompting strategies, so I cannot say whether a better prompt would close the gap.)

## What I Benchmarked

**Task:** given a deadline as a contest page writes it ("Submissions close October 28, 2026 at 11:59 PM PT") and where the reader lives ("Madrid, Spain"), return the deadline in the reader's local time as `ANSWER: YYYY-MM-DD HH:MM`.

Why this itch: I build tooling for hackathons, and the first rule I wrote for it was *never compute deadline hours by hand; store the canonical UTC instant and its source*. This benchmark checks whether that rule is still needed when the one doing the arithmetic is an LLM.

The trap that makes it interesting: in 2026, Europe leaves summer time on **October 25** and the US on **November 1**. For one week the usual Madrid–Los Angeles difference is 8 hours, not 9. The same happens in spring (US on March 8, Europe on March 29). Anything that "knows" the usual difference is wrong during those weeks, and so is anything that adds clock hours across a change.

The benchmark has three case sets, all with **exact ground truth**: every answer is computed with Python's `zoneinfo` and checked against a hand-written answer when the file is imported (the confirmatory set is checked against a second, independent oracle written from the US and EU rules). No LLM judge anywhere.

| Set | Cases | What it covers | Status |
|---|---|---|---|
| Standard | 20 | day rollover, the autumn and spring gap weeks, `12 AM` and AoE wording, non-hour offsets | designed first |
| Hard | 11 | relative dates, durations across a clock change, a Unix timestamp, an ISO `Z` time, described dates, a traveling reader | **exploratory**: written after seeing the standard results |
| Pairs | 100 (50 pairs) | each trap has a control twin with the same text, reader, clock time and weekday, moved out of the gap | **pre-registered** before any run ([pre-registration](https://github.com/hvaler/deadline-math/blob/main/docs/PREREGISTRATION.md)) |

The standard and hard sets each run in two modes: **direct** (reply with one line only, like a quick lookup or an agent writing to a calendar) and **reasoned** (think briefly, then the answer line). The pre-registered pairs set runs in **direct** mode only.

One embarrassing detail belongs here. While building the hard set, *my own oracle* got two cases wrong: in Python, `aware_datetime + timedelta(hours=48)` with a `ZoneInfo` zone adds **wall-clock** hours and ignores the clock change. The cross-check between the hand-written answer and the computed one caught it. Keep that in mind for the findings: it is exactly the mistake the models make.

## Models Tested

Why these models: I did not pick favorites. I ran **every model Kaggle Community Benchmarks offered**: 41 on October 3, 2026, plus the 5 it added by October 6 (Claude Opus 5.5 and Sonnet 5.5, GPT-6 Luna, GPT-6 Sol and GPT-6.1 Sol), from Anthropic, Google, OpenAI, xAI, Qwen, DeepSeek and Zhipu, because the question is practical: if you drop one of these into an agent that books your deadlines, which ones can you trust? That range also matters for the finding: it spans small and flagship models from the same families, so "it is just the small ones" can be tested rather than assumed. Not all of them could be measured:

- **43 models** completed the four original tasks cleanly; they form the comparison cohort.
- 3 could not be included because of **infrastructure**, never because of their answers: Grok 4.5 and 4.6 returned "model not found" (404), and gpt-oss-120b was overloaded (429) so often that its last task finished only after the data freeze. They are *not completed*, not 0%; gpt-oss-120b's late runs are visible on the leaderboard.
- The public Kaggle leaderboard only shows each task's latest run, and it shows a run that failed on infrastructure as a 0. So its pairs column shows the replication run (finding 4), and Qwen3 Next Thinking, which completed every task only on earlier runs before its latest ones failed with 429 errors, is in the GitHub data but not on the leaderboard.

Every completed model ran each task at least once at temperature 0, and most ran it twice (see finding 6).

## Findings

### 1. In the plain cases, the top of the field is saturated

On the standard set in direct mode, 20 of 43 models score 20/20 (among them the Gemini 3.x Flash and Pro models, both Gemma 4 models, Claude Sonnet 5 and 5.5, Claude Opus 5.5, GPT-5.5, GPT-5.6 Sol, GPT-6 Sol, GPT-6.1 Sol, and GLM-5). A benchmark where everyone scores 100% tells you nothing, so the interesting signal lives in the middle of the field and in the harder sets.

Cohort of 43 models with all four tasks:

| Condition | Correct |
|---|---|
| Standard, direct | 726/860 (84.4%) |
| Standard, reasoned | 812/860 (94.4%) |
| Hard, direct | 339/473 (71.7%) |
| Hard, reasoned | 380/473 (80.3%) |

### 2. Letting a model think helps the middle of the field, not the top

Allowing a short reasoning step changes little for the strongest models, but a lot for mid-sized ones: on the standard set Claude Haiku 4.5 goes from 9/20 to 17/20, GPT-5.4 nano from 3/20 to 17/20, Qwen3 Next Instruct from 7/20 to 16/20, Qwen3 Coder 480B from 3/20 to 13/20. Given how much a single run varies (finding 6), read it as "the direct mode is where cheap models break", not as a precise effect size or a causal claim about reasoning.

That matters because the direct mode approximates a common automation pattern: an agent producing a calendar-ready time, with nobody reading its reasoning.

### 3. The failures are mechanical: exactly one hour

Across the four tasks and the 43-model cohort, 409 answers missed the ground truth. Of the 382 misses with an extractable but incorrect time, **235 (62%) were off by exactly one hour**. The pattern is strongest where the usual offset breaks: 51 of 52 such errors in the autumn gap week, 18 of 20 in the spring gap, and 56 of 71 on durations that cross a clock change.

The models are not guessing. They apply the *usual* offset:

> "Madrid is on Central European Time in late October, while PT on October 28, 2026 is Pacific Daylight Time (UTC−7). 11:59 PM PT on October 28, 2026 corresponds to 8:59 AM in Madrid on October 29, 2026." 
>
> — GPT-5.4 mini (correct answer: 07:59)

It names the right rule (CET, not CEST) and then uses the 9-hour difference anyway.

> "Since it lasts exactly 48 hours, which is two full days, it will end at the same time two days later." 
>
> — Gemini 2.5 Flash, on a hackathon starting Saturday Oct 24 at 18:00 in Madrid (correct answer: Monday 17:00)

That is my `zoneinfo` bug, written in English.

And on this very contest's deadline:

> "On October 11, 2026, Madrid will be on CET (UTC+1) since it will be after the end of daylight saving time in Europe (which ends on the last Sunday of October, October 25, 2026)." 
>
> — Qwen3 Coder 480B (correct answer: 08:59; it answered 07:59)

It recites the right date for the change and then decides that October 11 comes after October 25.

### 4. The confirmatory test: the same sentence, trap date vs. control date

The claim above came from cases I designed after seeing failures. That is how you fool yourself, so before generating anything new, I wrote down the two hypotheses, the design, and the pass/fail criteria ([pre-registration](https://github.com/hvaler/deadline-math/blob/main/docs/PREREGISTRATION.md); the task notebook with all 100 cases was public on Kaggle before the first run). After writing the pre-registration, I ran a local pilot on two cheap models to check that the cases and the parser worked (it is not part of the analysis), then one run per pre-registered model on Kaggle; one model that failed on infrastructure was retried until it completed. The hypotheses:

- **H1:** for the same sentence, accuracy drops when the date falls in a gap week (or a duration crosses a clock change) compared with its control twin. *Holds if the bootstrap 95% CI of the mean penalty is above zero.*
- **H2:** more than half of the wrong answers on traps equal the *naive* answer: the usual offset, or clock-hour addition. *Holds if the lower bound of the Wilson 95% CI is above 50%.*

The set has 50 pairs. Each trap has a control twin with the same wording, reader, clock time, and weekday; only the date moves out of the gap. For example:

| | Statement | Reader | Correct |
|---|---|---|---|
| Trap | Submissions close Monday, October 26, 2026 at 11:59 PM PT. | Madrid | Oct 27, **07:59** |
| Control | Submissions close Monday, October 19, 2026 at 11:59 PM PT. | Madrid | Oct 20, **08:59** |

Every answer is computed with `zoneinfo` and checked against a second oracle written by hand from the US and EU rules; the run would not start if they disagreed on a single case.

**Result, pre-registered cohort (all 19 models completed):**

- **H1 holds.** Mean penalty: **+29.8 percentage points** (95% bootstrap CI: +25.4 to +34.2). 13 models do worse on traps, none do better, and 6 show no difference (sign test p = 0.0002). The bootstrap resamples the 50 paired cases while keeping the 19-model cohort fixed, so the interval does not include the uncertainty of choosing other models or rerunning them.
- **H2 holds.** **293 of 321** wrong trap answers with an extractable time (**91%**, Wilson CI 88–94%) are *exactly* the naive answer. Answers without an `ANSWER` line are not in this count; they do count as failures in H1.

**It replicated.** Because temperature 0 is not deterministic (finding 6), I ran the same set once more on the same models, logged in advance as a secondary analysis. 18 of the 19 completed (Qwen3 Next Thinking failed every retry with 429 errors): mean penalty **+29.6 points** (CI +26.0 to +33.1), and **277 of 306** extractable trap errors (91%) were again exactly the naive answer.

First run, all 19 pre-registered models:

| Model | Traps | Controls | Trap errors that are the naive answer |
|---|---|---|---|
| Claude Haiku 4.5 | 4% | 92% | 46 / 48 |
| Grok 4.20 (non-reasoning) | 18% | 96% | 37 / 41 |
| GPT-5.4 nano | 6% | 58% | 29 / 47 |
| GPT-5.4 mini | 34% | 92% | 31 / 33 |
| Gemini 3.1 Flash Lite | 34% | 100% | 33 / 33 |
| Gemini 3.5 Flash Lite | 34% | 96% | 33 / 33 |
| Qwen3 Coder 480B | 0% | 34% | 21 / 22 |
| Gemini 2.5 Flash | 62% | 96% | 18 / 18 |
| Qwen3 Next Thinking | 64% | 98% | 15 / 15 |
| GPT-5.6 Luna | 70% | 100% | 14 / 15 |
| Grok 4.20 Reasoning | 84% | 100% | 8 / 8 |
| Gemma 4 31B | 90% | 100% | 5 / 5 |
| Claude Sonnet 5 | 96% | 100% | 2 / 2 |
| Gemma 4 26B | 98% | 98% | 1 / 1 |
| Gemini 3 Flash, 3.6 Flash, 3.7 Flash, 3.8 Flash, GLM-5 | 100% | 100% | — |

![Trap vs. control accuracy for the 19 pre-registered models](https://raw.githubusercontent.com/hvaler/deadline-math/main/docs/img/pairs-preregistered.png)

The same chart with the 24-model extension added: [pairs.png](https://github.com/hvaler/deadline-math/blob/main/docs/img/pairs.png).

Full per-model tables with Wilson intervals and exact McNemar p-values, pre-registered cohort, and extension kept separate: [RESULTS.md](https://github.com/hvaler/deadline-math/blob/main/benchmark/resultados/RESULTS.md).

**Secondary extension (logged as a deviation before running it, reported separately):** once quota allowed, I ran the same set on 24 more models, many of them the most expensive ones, and the five Kaggle added on October 6. The pattern holds (mean penalty +22.6 points, CI +19.7 to +25.4; **308 of 321** extractable trap errors are the naive answer), with a clear split. Shown below: the two Claude lines and the models with no penalty; all 24 rows are in RESULTS.md.

| Model | Traps | Controls |
|---|---|---|
| Claude Sonnet 4.5 | 6% | 100% |
| Claude Sonnet 4.6 | 20% | 96% |
| Claude Sonnet 5 (pre-registered) | 96% | 100% |
| Claude Sonnet 5.5 | 100% | 100% |
| Claude Opus 4.5 | 22% | 82% |
| Claude Opus 4.6 | 46% | 90% |
| Claude Opus 4.7 | 76% | 90% |
| Claude Opus 4.8 | 78% | 100% |
| Claude Opus 5 | 96% | 90% |
| Claude Opus 5.5 | 100% | 100% |
| Qwen3 235B | 0% | 88% |
| GPT-5.5, GPT-5.6 Sol/Terra, GPT-6 Astra, GPT-6 Sol, GPT-6.1 Sol, Gemini 3.1 Pro, Gemini 3.5 Flash | 100% | 98–100% |

So this is not "small models fail, big models pass". Some flagship models still carry the habit, and some smaller ones (Gemini 3.x Flash, Gemma 4 26B, GLM-5) do not. Within each Claude line, trap accuracy is higher in each later release I tested: Sonnet 6% → 20% → 96% → 100% (4.5 to 5.5) and Opus 22% → 46% → 76% → 78% → 96% → 100% (4.5 to 5.5). Each model ran once, so the gap between 4.7 and 4.8 is within run-to-run noise, and Opus 5 even scores slightly *lower* on the controls (90%, not significant, p = 0.45). The newest generation tested here (Claude Opus 5.5 and Sonnet 5.5, GPT-6 Sol, and GPT-6.1 Sol) makes no trap errors at all.

Read the Haiku row again: it gets the control right 92% of the time and the *same sentence on its trap date* right 4% of the time, and when it is wrong, it is wrong by exactly the hour you would predict.

### 5. The hard set separates the top models in specific places

On the exploratory hard set, the top models finally diverge, and again the wrong answers are not random. Given `2026-10-25T02:30:00Z`, ninety minutes after Europe left summer time (01:00 UTC), **all 12** models that failed in direct mode (and 11 of 12 in reasoned mode) answered the same thing: 04:30 instead of 03:30, as if Madrid were still on summer time. Given a Unix timestamp, the most common wrong answer (5 models in direct mode, 7 in reasoned) was the same one, exactly one day early. Durations crossing a change got 0 of 3 from 11 models in direct mode, including Claude Haiku 4.5, Sonnet 4.5 and Opus 4.5, GPT-5.4 mini and nano, both Flash Lite models, and Grok 4.20 without reasoning.

### 6. Temperature 0 is not a fixed answer

Because Kaggle's public leaderboard only shows the latest version of each task, I re-ran almost every model on the final versions, with the same prompts. That gave me a free reliability test: **106 pairs of runs** of the same model on the same task. They agree on whether each case is right or wrong only **92.1%** of the time; a model's score moves by 4.4 points on average between runs, and by up to 36 points on the 11-case hard set. Differences between close neighbors on a single-run leaderboard are noise, which is why the confirmatory claim rests on 50 pairs pooled across models, not on any one model's rank.

### What surprised me, and what I would measure next

What surprised me most is the Sonnet 4.5 row: a flagship model, perfect on the controls, failing 47 of 50 traps, and always in the same direction. And then how cleanly it disappears: the newest models in the same family make no trap errors at all. Next I would measure:

- **Repeated runs and other temperatures** to put real error bars on the per-model numbers.
- **Other languages and readers outside Europe and North America** (Brazil, Chile, Australia), whose clock changes fall on yet other dates.
- **Agents with a clock tool**: Does giving the model a time-zone tool remove the bias, or does it still answer from habit without calling it?

## What it changed in how I think about these models

- A model that **states** the right rule can still **apply** the habitual one. Reading the explanation is not verification.
- The failure is predictable, which makes it fixable: extract the date, time, and zone with the model, then compute with a time-zone library, and show the source next to the result. Never let free text be the source of truth for a deadline.
- The weeks around clock changes are a small, cheap regression test for any agent that touches calendars.

## Limits

- Runs at temperature 0 are not deterministic (finding 6): differences of a few cases between models are noise.
- The cohort is the set of models that completed; quota and availability decide who is missing.
- The hard set is exploratory. Only the pairs set is confirmatory, and only for the 19 pre-registered models; the replication and the 24-model extension are secondary.
- Confidence intervals on the pairs resample the 50 cases with the cohort fixed; they do not cover other models or reruns. "Exactly one hour" shares are over misses with an extractable time; misses without an answer line are counted as failures but not classified.
- The score measures whether a correct time can be extracted, not strict formatting; strict one-line compliance is reported separately (793/860 and 424/473 in direct mode).
- English prompts only; readers in a handful of cities.
- The model list is the one Kaggle offered by October 6, 2026; the five models added after October 3 were run in a reopening of the data freeze, logged in the pre-registration, and only appear in secondary analyses.

## My Benchmark

- **Kaggle benchmark:** [kaggle.com/benchmarks/hugovalerrojas/deadline-mat](https://www.kaggle.com/benchmarks/hugovalerrojas/deadline-mat)
- Tasks: [deadline-math-pairs-direct](https://www.kaggle.com/benchmarks/tasks/hugovalerrojas/deadline-math-pairs-direct) (pre-registered), [deadline-math-direct](https://www.kaggle.com/benchmarks/tasks/hugovalerrojas/deadline-math-direct), [deadline-math-reasoned](https://www.kaggle.com/benchmarks/tasks/hugovalerrojas/deadline-math-reasoned), [deadline-math-hard-direct](https://www.kaggle.com/benchmarks/tasks/hugovalerrojas/deadline-math-hard-direct), [deadline-math-hard-reasoned](https://www.kaggle.com/benchmarks/tasks/hugovalerrojas/deadline-math-hard-reasoned)
- Code, raw runs and analysis: https://github.com/hvaler/deadline-math
- Cost: **$0 to me.** Every call, including local pilots, went through Kaggle's Model Proxy within the free quota. The proxy reported a nominal $1.75 for the 608 local pilot calls; the leaderboard shows an estimated cost per model.

*Built with the Kaggle Benchmarks SDK. AI assistance (Claude) was used for the code, the analysis, and the drafting of this post; I chose the problem, made the design decisions, and reviewed every claim. Every number above comes from the published runs.*
