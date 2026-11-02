# Error-rate bench of the Strategy Arena judge: report

Finished on 3 November 2026. The plan is in `PLAN.md`, written and committed before these seeds ran. Raw rows: `results.jsonl`, SHA-256 `e15fe36a9c494d814f4627dbd3a661c972d21e4ebde941bcf1b94692d3bf7aea`.

## Result

| Measure | Result | 95% Clopper-Pearson interval |
|---|---:|---:|
| False positives: NULL runs with at least one unforced `survives` | **0 of 300** | 0% to 1.22% |
| Detection: EDGE runs with at least one unforced `survives` | **82 of 100** | 73.05% to 88.97% |

On these synthetic markets, the judge confirmed nothing on 300 random walks and confirmed a strategy on 82 of 100 markets with a planted signal. **It missed the signal on 18 of the 100.** This says nothing about real markets.

## Execution

- All 300 NULL seeds and all 100 EDGE seeds ran once, with no crash, no resume, and no seed dropped or replaced.
- The 400 series were rebuilt with `generators.py`: 400 of 400 hashes match `csvSha256`.
- All 863 promotion rows have `matchesProof: true`.
- Runtime: about 9.7 hours on the CPU, 3 threads.
- The log line printed by the test says `n=30` for EDGE. That label is wrong: `results.jsonl` holds 100 EDGE seeds and 100 `move` rows.

## Secondary measures

Occupied cells, per data kind. A cell can stop before opening the sealed period.

| First outcome | NULL cells | EDGE cells |
|---|---:|---:|
| Stopped: `negative_train_score` | 508 | 6 |
| Stopped: `underpowered` | 82 | 70 |
| Opened: `mirage` | 29 | 42 |
| Opened: `inconclusive` | 0 | 29 |
| Opened: `survives` | 0 | 97 |
| **Total** | **619** | **244** |

Verdicts of the stopped cells once forced open, counted separately and never in the primary measures:

| Forced verdict | NULL | EDGE |
|---|---:|---:|
| `mirage` | 572 | 45 |
| `insufficient_activity` | 18 | 26 |
| `inconclusive` | 0 | 4 |
| `survives` | 0 | 1 |

- On NULL, even forced open, no stopped cell reached `survives`.
- On EDGE, one stopped cell would have reached `survives` once forced open (seed 2080, cell `t1_e0`, `cross_t12`, stopped by `negative_train_score`). That seed already counts as a detection through another cell, so this stop did not change the primary result.
- The 97 unforced `survives` came from two structures: `close_above_ema/timeout_short` (76) and `cross_t12` (21). `rsi_below/timeout_short` produced none.

## How to read it

- **0 of 300 is a bound, not a zero.** It rules out a false-positive rate above about 1.2% on this bench, at this confidence.
- **The EDGE signal is strong and regular:** hidden regimes of about 25 days with a drift of 0.6% a day. A real signal can be much weaker. 82% is not a detection rate for real strategies.
- **Detection depends on the structures.** Three fixed structures and one timeframe do not cover every use.

## Limits

- We wrote the judge, the bench, the plan and this report. No third party has rerun it yet.
- The EDGE setting and `cross_t12` were tuned during an earlier exploration on seeds 1 to 30. These seeds are new, but the setting is not independent of us.
- Lab 0.1.0-255 is not on the public download page on the date of this report. The series and the raw rows can be checked now; rerunning the verdicts needs that version.
- A verdict on past data is research, not advice.
