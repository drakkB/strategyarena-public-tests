# Error-rate bench of the Strategy Arena judge: plan

Written on 2 November 2026, before the seeds below were run. The Git history of this repository dates it. The result is published whatever it says.

## Question

On markets where the truth is known, how often does the judge confirm a strategy when there is nothing to find, and how often does it confirm one when a real signal was planted?

## Data

Synthetic only, no market data. `generators.py` rebuilds every series from its seed and its SHA-256 is logged for each run.

| Kind | What it is | Bench seeds | Runs |
|---|---|---|---:|
| NULL | Random walk without drift | 1001 to 1300 | 300 |
| EDGE | Hidden regimes of about 25 days, drift 0.6% a day | 2001 to 2100 | 100 |

14,000 daily bars, sealed end of 4,200 bars. Three fixed structures: `cross_t12` (EMA cross with a 12-bar exit), `close_above_ema/timeout_short`, `rsi_below/timeout_short`. Budget: 256 trials per structure, CPU backend. `move` then `promote` on every occupied cell.

## Measures, fixed now

**Primary**
1. False positives: share of NULL runs with at least one unforced `survives`.
2. Detection: share of EDGE runs with at least one unforced `survives`.

Both are given with a 95% Clopper-Pearson interval.

**Secondary**
- Cells stopped before opening the sealed period, by reason.
- Verdicts of the stops once forced open (`forcedVerdict`), counted separately.
- Share of `mirage` and `inconclusive` openings.

There is no pass mark. 0 out of 300 would bound the false-positive rate at about 1.2% on this bench, not on real markets.

## Rules

- No seed is dropped, replaced or rerun to change a result.
- If a run crashes, the bench resumes at that seed and the report says so.
- Settings do not change after this file. Another setting means another bench, with its own plan and new seeds.

## Code

- Strategy Arena Lab 0.1.0-255, freeze `20261102-255-n2`, commit `072267a040d0d947ee4c94ee0f29c1ddd948f9d5`.
- Test `plateau_255_bench_argon` with `harness.patch` applied (SHA-256 `3ff5347fc2fd6b162b027807e55685d54c7f4bc8393d0db14d6c5c3a770b6756`): seed ranges and the series hash, nothing in the judge.
- Test binary SHA-256 `7097445bf4f8109f3b51c13098a7fb7e1b5a81e71a3ac315a993c617b539df87`, Linux debug build with `--features cuda`, run with 3 threads.
- Environment: `P255_BENCH_ARMS=on`, `P255_BENCH_FORCE_ARMS=on`, `P255_BENCH_BARS=14000`, `P255_BENCH_TRIALS=256`, `P255_BENCH_SEED_START_NULL=1001`, `P255_BENCH_N_NULL=300`, `P255_BENCH_SEED_START_EDGE=2001`, `P255_BENCH_N_EDGE=100`.

## What was already known

An earlier run on seeds 1 to 30 gave 0 of 30 on NULL and 22 of 30 on EDGE (1 November 2026). The EDGE setting and the `cross_t12` structure were tuned during that exploration, which is why those seeds are not reused. Before this plan, seed 1 of both kinds was replayed to check the build: 5 of 5 rows matched the earlier output.

## Limits

- We wrote the judge, the bench and this plan.
- A synthetic bench says nothing about real markets. A planted regime can be easier or harder than a real signal.
- Three structures and one timeframe do not cover every use.
- Lab 0.1.0-255 is not on the public download page on the date of this plan. The series and the raw rows can be checked by anyone now; rerunning the verdicts needs that version of the Lab.

## Output

`results.jsonl` (raw rows) and `REPORT.md` in this folder. Machine-readable, no performance claim about any real market.
