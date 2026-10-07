# Deadline Math

[![tests](https://github.com/hvaler/deadline-math/actions/workflows/tests.yml/badge.svg)](https://github.com/hvaler/deadline-math/actions/workflows/tests.yml)
[![Kaggle benchmark](https://img.shields.io/badge/Kaggle-benchmark-20BEFF?logo=kaggle&logoColor=white)](https://www.kaggle.com/benchmarks/hugovalerrojas/deadline-mat)
[![Write-up on DEV](https://img.shields.io/badge/DEV-write--up-0A0A0A?logo=devdotto&logoColor=white)](https://dev.to/hugo_valer_79d0d94e00804b/the-model-knew-the-rule-it-still-used-last-weeks-offset-584m)
[![Pre-registered](https://img.shields.io/badge/pre--registered-yes-2ea44f)](docs/PREREGISTRATION.md)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

**Can a language model convert a published deadline into the reader's local time?**
"Submissions close October 28, 2026 at 11:59 PM PT" — what time is that in Madrid?

A benchmark built on [Kaggle Community Benchmarks](https://www.kaggle.com/benchmarks) for the
[DEV × Kaggle Benchmarking Challenge](https://dev.to/challenges/kaggle-2026-09-23). *Leer en español:
[README.es.md](README.es.md).*

![The model knew the rule. It still used last week's offset.](docs/img/cover.png)

## Key findings

In 2026, Europe leaves summer time on October 25 and the US on November 1; in spring, the US moves first (March 8)
and Europe follows (March 29). During those weeks the usual offset between the two sides is wrong by one hour.

- **The failure is mechanical, not random.** In a pre-registered test of 50 trap/control pairs (the same sentence
  with the date inside or outside those weeks), **91% of the wrong answers with a time (293/321) are exactly the
  naive answer**: the usual offset, or clock hours added across a clock change.
- **The trap costs 29.8 points of accuracy** on average for the 19 pre-registered models (95% CI +25.4 to +34.2);
  13 get worse and none gets better. **It replicated** on a second run (+29.6 points, 91%).
- **It is a matter of model generation, not size.** Claude Sonnet 4.5 gets 100% of controls and 6% of traps; within
  each Claude line the habit fades release by release, and the newest models tested (Claude Opus 5.5 and Sonnet 5.5,
  GPT-6 Sol, GPT-6.1 Sol) make no trap errors.
- **Temperature 0 is not deterministic:** two runs of the same model agree on 92% of cases.

![Trap vs. control accuracy for the 19 pre-registered models](docs/img/pairs-preregistered.png)

Full results, with Wilson intervals and exact McNemar tests, pre-registered cohort and secondary analyses kept
separate: **[benchmark/resultados/RESULTS.md](benchmark/resultados/RESULTS.md)**.

## Design

| Set | Cases | Modes | Status |
|---|---|---|---|
| Pairs | 100 (50 trap/control pairs) | direct | **pre-registered** ([PREREGISTRATION.md](docs/PREREGISTRATION.md)) |
| Standard | 20 | direct, reasoned | designed first |
| Hard | 11 | direct, reasoned | exploratory |

- **Exact ground truth, no LLM judge.** Every answer is computed with Python's `zoneinfo` and must match a
  hand-written answer when the module is imported; the 100 paired cases are also checked against an independent,
  hand-written implementation of the 2026 US and EU daylight-saving rules (see the tests).
- **Scoring:** a case is correct when the last `ANSWER: YYYY-MM-DD HH:MM` line of the reply matches the ground truth.
  Strict one-line format compliance is reported separately.
- **Models:** every model offered by Kaggle Community Benchmarks (46 by October 6, 2026); 43 completed all four
  original tasks. Infrastructure failures (HTTP 403/404/429/503) are reported as *not completed*, never as 0%.
- **Protocol:** the accepted task versions are pinned in `benchmark/kaggle_resultados.py`; every downloaded run is
  checked to have used exactly the prompts in the current code.

## Repository layout

```
benchmark/
  deadline_math.py        cases, prompts, oracle and the Kaggle task (single source of truth)
  construir_kaggle.py     writes the six self-contained task files in benchmark/kaggle/
  kaggle_resultados.py    per-task tables from the downloaded runs, with pinned task versions
  analisis_pares.py       pre-registered analysis: Wilson, exact McNemar, bootstrap, sign test
  tablas_en.py            builds RESULTS.md
  cifras_articulo.py      every number quoted in the write-up, computed from the data
  grafico_pares.py        the trap/control chart
  piloto.py               local pilot runner through the Kaggle model proxy
  tests/                  25 tests (oracles, parser, classification, version and replica selection)
  resultados/
    RESULTS.md            final results (English)
    kaggle/               raw runs downloaded from Kaggle, including full model trajectories
    piloto-*.jsonl        local pilot runs
docs/
  PREREGISTRATION.md      pre-registration (English translation), deviations and execution log
  preregistro-original-es.md   the authoritative Spanish original
  img/                    figures
```

Docstrings and comments outside `deadline_math.py` are in Spanish, the author's working language.

## Reproduce

Python 3.12.

```bash
python -m venv .venv
source .venv/bin/activate            # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m unittest discover -s benchmark/tests -v   # oracles, parser and analysis
python benchmark/tablas_en.py                       # rebuilds RESULTS.md from benchmark/resultados/kaggle/
python benchmark/cifras_articulo.py                 # every figure in the write-up
```

Running the tasks yourself needs a Kaggle account with phone and identity verification, `kaggle benchmarks init`,
and then `kaggle b t push <task> -f benchmark/kaggle/<task>.py` and `kaggle b t run <task> -m <model>`.

## Cite

```bibtex
@misc{valer2026deadlinemath,
  title        = {Deadline Math: LLMs and time-zone conversion of published deadlines},
  author       = {Valer Rojas, Hugo Carlos},
  year         = {2026},
  howpublished = {Kaggle Community Benchmarks},
  url          = {https://www.kaggle.com/benchmarks/hugovalerrojas/deadline-mat}
}
```

GitHub's "Cite this repository" button reads [CITATION.cff](CITATION.cff).

## License and disclosure

Code under the [MIT License](LICENSE). Model outputs in `benchmark/resultados/` are published as evidence for the
analysis. AI assistance (Claude) was used for the code, the analysis and the write-up; the author chose the problem,
made the design decisions and reviewed every claim.
