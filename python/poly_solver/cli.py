"""Command-line interface for the polynomial equation solver."""

from __future__ import annotations

import argparse
import sys

from .solver import format_result, solve_cubic, solve_quadratic


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="poly-solver",
        description="Solve quadratic and cubic equations with real coefficients.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    quadratic = subparsers.add_parser(
        "quadratic",
        help="Solve a*x^2 + b*x + c = 0",
    )
    quadratic.add_argument("a", type=float)
    quadratic.add_argument("b", type=float)
    quadratic.add_argument("c", type=float)

    cubic = subparsers.add_parser(
        "cubic",
        help="Solve a*x^3 + b*x^2 + c*x + d = 0",
    )
    cubic.add_argument("a", type=float)
    cubic.add_argument("b", type=float)
    cubic.add_argument("c", type=float)
    cubic.add_argument("d", type=float)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    try:
        if args.command == "quadratic":
            result = solve_quadratic(args.a, args.b, args.c)
        elif args.command == "cubic":
            result = solve_cubic(args.a, args.b, args.c, args.d)
        else:
            parser.error(f"Unknown command: {args.command}")
            return 2
    except ValueError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    print(format_result(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
