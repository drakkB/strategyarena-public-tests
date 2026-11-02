# AI quant researcher leaderboard, round 2: plan

Written on 2 November 2026. The Git history of this repository dates it. The result is published whatever it says, including if no model stands out.

## Question

Round 1 tested frozen strategies on a past period (October 2023 to September 2026). The research tool hid that period, but the models may know it from their training. What happens to the same strategies on candles that did not exist when they were frozen?

## What is frozen

`strategies.json`: the 23 primary entries of round 1, with the exact script and its SHA-256. File SHA-256: `528e9a057931595d26898b96eed66c4d49143172724cfbce006b90609c2f3fc6`. One entry abstained and is listed as such. No new AI run and no tokens: nothing is added or edited after this file. Some models wrote identical scripts; each entry stays as it is. No frozen rule uses a chart figure (head and shoulders, double top and the like): they are moving-average, breakout and momentum rules.

## Tape

- Market: BTCUSDT 4h, spot, from Binance public data. Candles are not redistributed here. Their SHA-256 is published with each reading.
- First scored candle: **2026-11-05 00:00 UTC**. All scripts are public before it.
- The tape given to the engine starts on **2026-09-01 00:00 UTC**, so that the slowest rule (300 bars) has warmed up before the first scored candle. Nothing before the first scored candle counts in a score. A rule already in position at that moment stays in position, as it would have in live.
- Fees: 10 bps per side, as in round 1.

## Engine

Strategy Arena Lab 0.1.0-255, freeze `20261102-255-n2`, commit `072267a040d0d947ee4c94ee0f29c1ddd948f9d5`, with `replay.patch` (SHA-256 `86b74cdbbda84c1de4113071b3e297b21240b037514723238ea91f1dc34018f0`, test harness only), tool `run_sandbox_backtest`, `executionSemantics: tv_exact_v1` set explicitly so that a later change of default cannot alter this round. The same engine runs every entry at every reading.

## Equity

Scores come from the engine itself, with no separate reconstruction. For each UTC day, the entry is rerun on the tape cut at that day's last 4h close, and `equity_final` is read. Return and maximum drawdown are computed on this daily series from the last close before the first scored candle. Before this plan, cuts at two dates on the round 1 tape gave the same opening trades as the full run, for all 22 scripts. Buy-and-hold is computed on the same daily closes from the same starting point, with the same fees.

## Readings

| Date | What is published |
|---|---|
| 2027-05-05 | Indicative table, no ranking |
| 2027-11-05 | First ranking |
| 2028-11-05 | Final ranking |

Each reading covers the first candle up to the last candle closed before that date.

## Ranking, mechanical

Return divided by maximum drawdown on the daily series above, after fees. An entry needs at least 10 trades closed after the first scored candle to be ranked; otherwise it is shown as "too few trades". Models with several entries get the average of their entries. Buy-and-hold is shown beside them. An entry that does not run scores nothing and is shown as such. Ties: lower maximum drawdown.

## Limits

- One market and one or two years: chance cannot be separated from skill. The ranking describes what happened and shows no model to be better.
- All the frozen rules are slow trend rules on the same market, so their results will be strongly correlated.
- The scripts were written with knowledge of markets up to 2026.
- The referee, Claude, is also a contestant, which is why the score is mechanical.
- None of these strategies trades real money.

## Round 1 used other semantics

Replaying these entries with this engine does not reproduce round 1, because round 1 ran under `legacy_v1` and the engine defaults to `tv_exact_v1` since Lab 241. With `executionSemantics: legacy_v1`, Lab 255 reproduces all 21 scored entries (return, drawdown, trades): `replay-legacy.jsonl`. Under `tv_exact_v1`, `replay-check.json` shows differences of up to about 108 points of return. `legacy_v1` differs from TradingView: its EMA is recomputed over a window, indicators equal the price during warm-up from bar 55, and stops and targets are read on closes. `tv_exact_v1` was compared with real TradingView logs on 6 of these scripts over 4,000 candles: 234 of 234 trades matched in date and price. That does not cover every script.

Round 1 is not rescored. Round 1 and round 2 figures must not be compared directly.

## Corrections to this plan

2 November 2026, before the first scored candle: the first version said the cause of the round 1 differences was not established, and that indicators warmed up on the scored tape "as in round 1", which was wrong. It also left the execution semantics to the default. The tape start, the equity method, the explicit semantics and this section were added. The frozen strategies and the first scored candle did not change.

Research and education only, not financial advice.
