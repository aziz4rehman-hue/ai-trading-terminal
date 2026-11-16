"""Command session for the paper terminal."""

from __future__ import annotations

from aiterm.analyst import brief
from aiterm.book import Book
from aiterm.market import Market

HELP = """commands:
  help
  quotes
  quote SYMBOL
  buy SYMBOL QTY
  sell SYMBOL QTY
  tick [N]
  positions
  blotter
  brief
  cash
Fills are paper fills at the last quote. No broker is connected."""


class Terminal:
    def __init__(self, cash: float = 100_000.0, seed: int = 7) -> None:
        self.market = Market(seed)
        self.book = Book(cash)

    def execute(self, line: str) -> str:
        parts = line.strip().split()
        if not parts:
            return HELP
        cmd = parts[0].lower()
        try:
            if cmd == "help":
                return HELP
            if cmd == "quotes":
                return self._quotes()
            if cmd == "quote":
                return self._quote(parts)
            if cmd == "buy":
                return self._buy(parts)
            if cmd == "sell":
                return self._sell(parts)
            if cmd == "tick":
                return self._tick(parts)
            if cmd == "positions":
                return self._positions()
            if cmd == "blotter":
                return self._blotter()
            if cmd == "brief":
                return brief(self.market, self.book)
            if cmd == "cash":
                return f"cash {self.book.cash:.2f} equity {self.book.equity(self.market.prices):.2f}"
            return "error: unknown command. Try: help"
        except ValueError as exc:
            return f"error: {exc}"

    def demo(self) -> str:
        commands = ["quotes", "buy AAPL 10", "buy MSFT 5", "tick 3", "positions", "brief"]
        return self.run(commands)

    def run(self, commands: list[str]) -> str:
        blocks = []
        for command in commands:
            blocks.append(f"> {command}\n{self.execute(command)}")
        return "\n".join(blocks)

    def _symbol(self, token: str) -> str:
        symbol = token.upper()
        if symbol not in self.market.prices:
            known = ", ".join(self.market.symbols())
            raise ValueError(f"unknown symbol {symbol}. Known: {known}")
        return symbol

    def _quotes(self) -> str:
        lines = [f"{symbol:<6} {price:12.2f}" for symbol, price in self.market.prices.items()]
        return "\n".join(lines)

    def _quote(self, parts: list[str]) -> str:
        if len(parts) != 2:
            raise ValueError("usage: quote SYMBOL")
        symbol = self._symbol(parts[1])
        return f"{symbol} {self.market.prices[symbol]:.2f}"

    def _qty(self, token: str) -> float:
        try:
            qty = float(token)
        except ValueError as exc:
            raise ValueError("qty must be a number") from exc
        return qty

    def _buy(self, parts: list[str]) -> str:
        if len(parts) != 3:
            raise ValueError("usage: buy SYMBOL QTY")
        symbol = self._symbol(parts[1])
        qty = self._qty(parts[2])
        price = self.market.prices[symbol]
        fill = self.book.buy(symbol, qty, price)
        return f"bought {fill.qty:g} {symbol} @ {fill.price:.2f} cash {self.book.cash:.2f}"

    def _sell(self, parts: list[str]) -> str:
        if len(parts) != 3:
            raise ValueError("usage: sell SYMBOL QTY")
        symbol = self._symbol(parts[1])
        qty = self._qty(parts[2])
        price = self.market.prices[symbol]
        fill = self.book.sell(symbol, qty, price)
        return (
            f"sold {fill.qty:g} {symbol} @ {fill.price:.2f} "
            f"pnl {fill.pnl:+.2f} cash {self.book.cash:.2f}"
        )

    def _tick(self, parts: list[str]) -> str:
        steps = 1
        if len(parts) == 2:
            try:
                steps = int(parts[1])
            except ValueError as exc:
                raise ValueError("usage: tick [N]") from exc
        elif len(parts) > 2:
            raise ValueError("usage: tick [N]")
        if steps > 500:
            raise ValueError("tick N must be 500 or less")
        self.market.tick(steps)
        return f"advanced {steps} tick(s)"

    def _positions(self) -> str:
        if not self.book.positions:
            return "flat"
        lines = []
        for symbol in sorted(self.book.positions):
            pos = self.book.positions[symbol]
            last = self.market.prices[symbol]
            pnl = (last - pos["avg"]) * pos["qty"]
            lines.append(
                f"{symbol:<6} qty {pos['qty']:g} avg {pos['avg']:.2f} last {last:.2f} pnl {pnl:+.2f}"
            )
        return "\n".join(lines)

    def _blotter(self) -> str:
        if not self.book.fills:
            return "no fills"
        return "\n".join(
            f"{fill.side:<4} {fill.qty:g} {fill.symbol} @ {fill.price:.2f} pnl {fill.pnl:+.2f}"
            for fill in self.book.fills
        )
