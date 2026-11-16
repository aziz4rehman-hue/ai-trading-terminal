"""Seeded quote tape. The path is deterministic for a given seed."""

from __future__ import annotations

import random


START_PRICES = {
    "AAPL": 190.0,
    "MSFT": 420.0,
    "NVDA": 140.0,
    "BTC": 67000.0,
}


class Market:
    def __init__(self, seed: int = 7) -> None:
        self.rng = random.Random(seed)
        self.prices = dict(START_PRICES)
        self.history: dict[str, list[float]] = {symbol: [price] for symbol, price in self.prices.items()}

    def symbols(self) -> list[str]:
        return list(self.prices)

    def tick(self, steps: int = 1) -> None:
        if steps < 1:
            raise ValueError("steps must be positive")
        for _ in range(steps):
            for symbol in self.prices:
                shock = self.rng.gauss(0, 0.008)
                nxt = round(max(1.0, self.prices[symbol] * (1 + shock)), 2)
                self.prices[symbol] = nxt
                self.history[symbol].append(nxt)

    def trend(self, symbol: str, window: int = 5) -> str:
        hist = self.history[symbol][-window:]
        if len(hist) < 2 or hist[-1] == hist[0]:
            return "flat"
        return "up" if hist[-1] > hist[0] else "down"
