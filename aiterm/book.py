"""Cash and long-only positions. Fills happen at the price the caller passes."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Fill:
    side: str
    symbol: str
    qty: float
    price: float
    pnl: float


class Book:
    def __init__(self, cash: float = 100_000.0) -> None:
        if cash <= 0:
            raise ValueError("cash must be positive")
        self.cash = float(cash)
        self.positions: dict[str, dict[str, float]] = {}
        self.fills: list[Fill] = []

    def equity(self, prices: dict[str, float]) -> float:
        total = self.cash
        for symbol, pos in self.positions.items():
            total += pos["qty"] * prices[symbol]
        return total

    def buy(self, symbol: str, qty: float, price: float) -> Fill:
        if qty <= 0:
            raise ValueError("qty must be positive")
        if price <= 0:
            raise ValueError("price must be positive")
        cost = qty * price
        if cost > self.cash + 1e-9:
            raise ValueError("insufficient cash")
        pos = self.positions.get(symbol)
        if pos is None:
            self.positions[symbol] = {"qty": qty, "avg": price}
        else:
            new_qty = pos["qty"] + qty
            pos["avg"] = (pos["avg"] * pos["qty"] + price * qty) / new_qty
            pos["qty"] = new_qty
        self.cash -= cost
        fill = Fill("buy", symbol, qty, price, 0.0)
        self.fills.append(fill)
        return fill

    def sell(self, symbol: str, qty: float, price: float) -> Fill:
        if qty <= 0:
            raise ValueError("qty must be positive")
        if price <= 0:
            raise ValueError("price must be positive")
        pos = self.positions.get(symbol)
        if pos is None or pos["qty"] + 1e-9 < qty:
            raise ValueError("insufficient position")
        pnl = (price - pos["avg"]) * qty
        pos["qty"] -= qty
        if pos["qty"] <= 1e-9:
            del self.positions[symbol]
        else:
            # average cost stays on the remainder
            pass
        self.cash += qty * price
        fill = Fill("sell", symbol, qty, price, pnl)
        self.fills.append(fill)
        return fill
