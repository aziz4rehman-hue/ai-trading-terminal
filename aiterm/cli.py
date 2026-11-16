"""CLI. Repeating --eval keeps one paper book for the process."""

from __future__ import annotations

import argparse

from aiterm import __version__
from aiterm.terminal import Terminal


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="aiterm",
        description="Paper trading terminal. No live orders. Not financial advice.",
    )
    parser.add_argument("--version", action="version", version=f"aiterm {__version__}")
    parser.add_argument("--demo", action="store_true", help="Run a fixed paper session")
    parser.add_argument("--cash", type=float, default=100_000.0)
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument("--eval", action="append", default=[], help="Command to run. Repeatable.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    desk = Terminal(cash=args.cash, seed=args.seed)
    if args.demo:
        print(desk.demo())
        return 0
    if not args.eval:
        build_parser().print_help()
        return 0
    print(desk.run(args.eval))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
