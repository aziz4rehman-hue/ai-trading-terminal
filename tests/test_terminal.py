import unittest

from aiterm.market import Market
from aiterm.terminal import Terminal


class TerminalTests(unittest.TestCase):
    def test_buy_and_sell_round_trip_at_same_price(self):
        desk = Terminal(cash=10_000, seed=1)
        self.assertIn("bought 10 AAPL @ 190.00", desk.execute("buy AAPL 10"))
        self.assertAlmostEqual(desk.book.cash, 8_100)
        sold = desk.execute("sell AAPL 10")
        self.assertIn("pnl +0.00", sold)
        self.assertAlmostEqual(desk.book.cash, 10_000)
        self.assertEqual(desk.execute("positions"), "flat")

    def test_rejects_overspend_and_oversell(self):
        desk = Terminal(cash=1_000, seed=1)
        self.assertIn("insufficient cash", desk.execute("buy BTC 1"))
        self.assertIn("insufficient position", desk.execute("sell AAPL 1"))
        self.assertIn("unknown symbol", desk.execute("quote NOPE"))

    def test_average_cost(self):
        desk = Terminal(cash=100_000, seed=1)
        desk.execute("buy AAPL 10")
        desk.market.prices["AAPL"] = 200
        desk.execute("buy AAPL 10")
        pos = desk.book.positions["AAPL"]
        self.assertEqual(pos["qty"], 20)
        self.assertAlmostEqual(pos["avg"], 195)

    def test_ticks_are_deterministic_and_brief_is_labeled(self):
        first = Market(seed=7)
        second = Market(seed=7)
        first.tick(4)
        second.tick(4)
        self.assertEqual(first.prices, second.prices)
        desk = Terminal(seed=7)
        desk.execute("buy NVDA 2")
        desk.execute("tick 2")
        text = desk.execute("brief")
        self.assertIn("not financial advice", text)
        self.assertIn("NVDA", text)

    def test_unknown_command(self):
        self.assertIn("unknown command", Terminal().execute("launch"))


if __name__ == "__main__":
    unittest.main()
