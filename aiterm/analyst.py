"""Rules-based brief. This is not a model and not a trade recommendation."""

from __future__ import annotations

from aiterm.book import Book
from aiterm.market import Market


def brief(market: Market, book: Book) -> str:
    lines = ["paper brief — not financial advice, not a live order"]
    if not book.positions:
        lines.append("flat book")
    for symbol in sorted(book.positions):
        pos = book.positions[symbol]
        last = market.prices[symbol]
        pnl = (last - pos["avg"]) * pos["qty"]
        lines.append(
            f"{symbol} qty {pos['qty']:g} avg {pos['avg']:.2f} last {last:.2f} "
            f"pnl {pnl:+.2f} trend {market.trend(symbol)}"
        )
        if last < pos["avg"] * 0.95:
            lines.append(f"alert {symbol} is more than 5% under your average")
    lines.append(f"cash {book.cash:.2f} equity {book.equity(market.prices):.2f}")
    return "\n".join(lines)
