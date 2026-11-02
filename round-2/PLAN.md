# AI quant researcher leaderboard, round 2: plan

Written on 2 November 2026. The Git history of this repository dates it. The result is published whatever it says, including if no model stands out.

## Question

Round 1 tested frozen strategies on a past period (October 2023 to September 2026). The research tool hid that period, but the models may know it from their training. What happens to the same strategies on candles that did not exist when they were frozen?

## What is frozen

`strategies.json`: the 23 primary entries of round 1, with the exact script and its SHA-256. File SHA-256: `528e9a057931595d26898b96eed66c4d49143172724cfbce006b90609c2f3fc6`. One entry abstained and is listed as such. No new AI run and no tokens: nothing is added or edited after this file. Some models wrote identical scripts; each entry stays as it is. No frozen rule uses a chart figure (head and shoulders, double top and the like): they are moving-average, breakout and momentum rules.

## Tape

- Market: BTCUSDT 4h, spot, from Binance public data. Candles are not redistributed here. Their SHA-256 is published with each reading.
- First candle: **2026-11-05 00:00 UTC**. All scripts are public before it.
- Indicators warm up on this tape, as in round 1, so slow rules stay flat for their first weeks.
- Fees: 10 bps per side, as in round 1.

## Engine

Strategy Arena Lab 0.1.0-255, freeze `20261102-255-n2`, commit `072267a040d0d947ee4c94ee0f29c1ddd948f9d5`, with `replay.patch` (SHA-256 `4c5db3b61592da87159e4fe0d24142a4a368e1b94d5cc6119fa46d8ae2446066`, test harness only), tool `run_sandbox_backtest`. The same engine runs every entry and buy-and-hold at every reading.

## Readings

| Date | What is published |
|---|---|
| 2027-05-05 | Indicative table, no ranking |
| 2027-11-05 | First ranking |
| 2028-11-05 | Final ranking |

Each reading covers the first candle up to the last candle closed before that date.

## Ranking, mechanical

Return divided by maximum drawdown, after fees. An entry needs at least 10 closed trades to be ranked; otherwise it is shown as "too few trades". Models with several entries get the average of their entries. Buy-and-hold is shown beside them. An entry that does not run scores nothing and is shown as such. Ties: lower maximum drawdown.

## Limits

- One market and one or two years: chance cannot be separated from skill. The ranking describes what happened and shows no model to be better.
- All the frozen rules are slow trend rules on the same market, so their results will be strongly correlated.
- The scripts were written with knowledge of markets up to 2026.
- The referee, Claude, is also a contestant, which is why the score is mechanical.
- None of these strategies trades real money.

## Check of the engine against round 1

`replay-check.json` replays the entries on the round 1 sealed tape with this engine. **Round 1 figures are not all reproduced:** 10 of 21 entries are within 1 point of return, the others differ, up to about 108 points, often with a different trade count, and one entry that exceeded the work budget in round 1 now runs. Round 1 ran on earlier Lab versions; the cause has not been established on the date of this plan. Round 1 and round 2 figures must therefore not be compared directly. Round 2 entries are only compared with each other, on one engine.

Research and education only, not financial advice.
