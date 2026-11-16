# ai-trading-terminal

Paper trading desk in the terminal. Quotes, buys, sells, and a short analyst brief. Nothing is routed to a broker.

**Not financial advice. No live orders.**

```bash
git clone https://github.com/aziz4rehman-hue/ai-trading-terminal.git
cd ai-trading-terminal
python -m aiterm --demo
```

```
> quotes
AAPL         190.00
MSFT         420.00
NVDA         140.00
BTC        67000.00
> buy AAPL 10
bought 10 AAPL @ 190.00 cash 98100.00
> buy MSFT 5
bought 5 MSFT @ 420.00 cash 96000.00
> tick 3
advanced 3 tick(s)
> positions
AAPL   qty 10 avg 190.00 last 189.76 pnl -2.40
MSFT   qty 5 avg 420.00 last 421.84 pnl +9.20
> brief
paper brief — not financial advice, not a live order
AAPL qty 10 avg 190.00 last 189.76 pnl -2.40 trend down
MSFT qty 5 avg 420.00 last 421.84 pnl +9.20 trend up
cash 96000.00 equity 100006.80
```

The tape is a seeded random walk, so the same seed always reprints the same path. Fills use the last quote. You cannot spend cash you do not have, and you cannot sell a share you do not hold.

## Your own commands

`--eval` repeats on one book:

```bash
python -m aiterm --cash 25000 --seed 7 \
  --eval "buy AAPL 5" \
  --eval "tick 2" \
  --eval "brief"
```

| Command | What it does |
|---|---|
| `quotes` / `quote SYMBOL` | Last prices |
| `buy SYMBOL QTY` / `sell SYMBOL QTY` | Paper fill at the last quote |
| `tick [N]` | Advance the tape, up to 500 steps |
| `positions` / `blotter` / `cash` | Book |
| `brief` | Trend and a 5% underwater alert |

Symbols in the demo tape: `AAPL`, `MSFT`, `NVDA`, `BTC`.

From Python:

```python
from aiterm.terminal import Terminal

desk = Terminal(cash=10_000, seed=7)
print(desk.execute("buy AAPL 2"))
print(desk.execute("brief"))
```

## Tests

```bash
python -m unittest discover -s tests -v
```

Python 3.10+. No third-party packages.

## License

MIT. Built by [Aziz Rehman](https://github.com/aziz4rehman-hue).
