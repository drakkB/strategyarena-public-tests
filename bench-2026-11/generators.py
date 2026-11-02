#!/usr/bin/env python3
"""Rebuilds the synthetic markets of the bench. No market data: only arithmetic from a seed.
Usage: python3 generators.py NULL 1001 > series.csv   (kind NULL or EDGE, seed; 14000 daily bars)
The SHA-256 of the output is the csvSha256 field of results.jsonl."""
import math, sys
from datetime import datetime, timezone
M = (1 << 64) - 1
DAY = 86_400_000
T0 = 1_420_070_400_000  # 2015-01-01


class Rng:
    def __init__(self, seed, salt):
        self.s = ((seed * 0x9E3779B97F4A7C15) & M) ^ salt

    def lcg(self):
        self.s = (self.s * 6364136223846793005 + 1442695040888963407) & M
        return (self.s >> 11) / float(1 << 53)

    def normal(self):
        a, b = max(self.lcg(), 1e-12), self.lcg()
        return math.sqrt(-2.0 * math.log(a)) * math.cos(2.0 * math.pi * b)


def stamp(ms):
    return datetime.fromtimestamp(ms / 1000, timezone.utc).strftime(STAMP)


STAMP = "%Y-%m-%dT%H:%M:%SZ"


def null_csv(n, seed):
    """Random walk without drift: there is nothing to find. Series seed = 7000 + bench seed."""
    r = Rng(7000 + seed, 0x254C)
    close, out = 100.0, ["timestamp,open,high,low,close,volume"]
    for i in range(n):
        o = close
        close = o * math.exp(0.02 * r.normal())
        hi = max(o, close) * (1.0 + 0.004 * r.lcg())
        lo = min(o, close) * (1.0 - 0.004 * r.lcg())
        out.append(f"{stamp(T0 + i * DAY)},{o:.6f},{hi:.6f},{lo:.6f},{close:.6f},{1000.0 + 500.0 * r.lcg():.1f}")
    return "\n".join(out) + "\n"


def edge_csv(n, seed, drift=0.006):
    """Hidden regimes of about 25 days, up or down by `drift` a day. Series seed = 8000 + bench seed."""
    r = Rng(8000 + seed, 0x254D)
    close, up, out = 100.0, True, ["timestamp,open,high,low,close,volume"]
    for i in range(n):
        if r.lcg() < 0.04:
            up = not up
        o = close
        close = o * math.exp((drift if up else -drift) + 0.012 * r.normal())
        out.append(f"{stamp(T0 + i * DAY)},{o:.6f},{max(o, close) * 1.001:.6f},{min(o, close) * 0.999:.6f},{close:.6f},1000.0")
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    kind, seed = sys.argv[1], int(sys.argv[2])
    sys.stdout.write((null_csv if kind == "NULL" else edge_csv)(14000, seed))
