"""Solvers for linear, quadratic, and cubic equations.

The functions in this module solve equations with real coefficients and may
return real or complex roots. Degenerate equations are handled automatically:

- quadratic with a = 0 becomes linear
- cubic with a = 0 becomes quadratic
"""

from __future__ import annotations

from dataclasses import dataclass
import cmath
import math
from typing import Iterable, List

DEFAULT_EPSILON = 1e-12


@dataclass(frozen=True)
class EquationResult:
    """Container for a solved equation."""

    equation_type: str
    roots: List[complex]
    infinite_solutions: bool = False
    no_solution: bool = False


def _validate_finite(value: float, name: str) -> None:
    if not math.isfinite(value):
        raise ValueError(f"{name} must be a finite number")


def _is_near_zero(value: float, epsilon: float = DEFAULT_EPSILON) -> bool:
    return abs(value) < epsilon


def _clean_complex(value: complex, epsilon: float = DEFAULT_EPSILON) -> complex:
    real = 0.0 if abs(value.real) < epsilon else value.real
    imag = 0.0 if abs(value.imag) < epsilon else value.imag
    return complex(real, imag)


def _real_cuberoot(value: float) -> float:
    """Return the real cube root, preserving the sign for negative values."""
    if value >= 0:
        return value ** (1.0 / 3.0)
    return -((-value) ** (1.0 / 3.0))


def sort_roots(roots: Iterable[complex]) -> List[complex]:
    """Sort roots by real part, then imaginary part, for stable output."""
    return sorted(roots, key=lambda z: (round(z.real, 12), round(z.imag, 12)))


def solve_linear(a: float, b: float, epsilon: float = DEFAULT_EPSILON) -> EquationResult:
    """Solve a*x + b = 0."""
    _validate_finite(a, "a")
    _validate_finite(b, "b")

    if _is_near_zero(a, epsilon):
        if _is_near_zero(b, epsilon):
            return EquationResult("linear", [], infinite_solutions=True)
        return EquationResult("linear", [], no_solution=True)

    return EquationResult("linear", [_clean_complex(complex(-b / a, 0.0), epsilon)])


def solve_quadratic(a: float, b: float, c: float, epsilon: float = DEFAULT_EPSILON) -> EquationResult:
    """Solve a*x^2 + b*x + c = 0.

    Uses a numerically stable version of the quadratic formula when the
    discriminant is non-negative, and the symmetric complex formula when the
    roots are complex.
    """
    _validate_finite(a, "a")
    _validate_finite(b, "b")
    _validate_finite(c, "c")

    if _is_near_zero(a, epsilon):
        return solve_linear(b, c, epsilon)

    discriminant = b * b - 4.0 * a * c

    if discriminant >= 0.0:
        sqrt_d = math.sqrt(max(0.0, discriminant))
        sign_b = 1.0 if b >= 0 else -1.0
        q = -0.5 * (b + sign_b * sqrt_d)

        if _is_near_zero(q, epsilon):
            root = _clean_complex(complex(-b / (2.0 * a), 0.0), epsilon)
            roots = [root, root]
        else:
            roots = [
                _clean_complex(complex(q / a, 0.0), epsilon),
                _clean_complex(complex(c / q, 0.0), epsilon),
            ]
    else:
        sqrt_d_complex = cmath.sqrt(complex(discriminant, 0.0))
        roots = [
            _clean_complex((-b + sqrt_d_complex) / (2.0 * a), epsilon),
            _clean_complex((-b - sqrt_d_complex) / (2.0 * a), epsilon),
        ]

    return EquationResult("quadratic", sort_roots(roots))


def solve_cubic(
    a: float,
    b: float,
    c: float,
    d: float,
    epsilon: float = DEFAULT_EPSILON,
) -> EquationResult:
    """Solve a*x^3 + b*x^2 + c*x + d = 0.

    The implementation uses the depressed cubic transformation and Cardano's
    method with separate real branches for numerical stability.
    """
    _validate_finite(a, "a")
    _validate_finite(b, "b")
    _validate_finite(c, "c")
    _validate_finite(d, "d")

    if _is_near_zero(a, epsilon):
        return solve_quadratic(b, c, d, epsilon)

    # Normalize: x^3 + A*x^2 + B*x + C = 0
    A = b / a
    B = c / a
    C = d / a

    # Depressed cubic: y^3 + p*y + q = 0, x = y - A/3
    p = B - (A * A) / 3.0
    q = (2.0 * A * A * A) / 27.0 - (A * B) / 3.0 + C
    shift = A / 3.0
    discriminant = (q * q) / 4.0 + (p * p * p) / 27.0

    if discriminant > epsilon:
        # One real root and two complex conjugate roots.
        sqrt_disc = math.sqrt(discriminant)
        u = _real_cuberoot(-q / 2.0 + sqrt_disc)
        v = _real_cuberoot(-q / 2.0 - sqrt_disc)

        y1 = u + v
        real_part = -(u + v) / 2.0
        imag_part = (math.sqrt(3.0) / 2.0) * (u - v)

        roots = [
            complex(y1 - shift, 0.0),
            complex(real_part - shift, imag_part),
            complex(real_part - shift, -imag_part),
        ]
    elif abs(discriminant) <= epsilon:
        # Multiple real roots.
        u = _real_cuberoot(-q / 2.0)
        roots = [
            complex(2.0 * u - shift, 0.0),
            complex(-u - shift, 0.0),
            complex(-u - shift, 0.0),
        ]
    else:
        # Three distinct real roots. In this branch p is negative.
        acos_arg_raw = (3.0 * q / (2.0 * p)) * math.sqrt(-3.0 / p)
        acos_arg = max(-1.0, min(1.0, acos_arg_raw))
        phi = math.acos(acos_arg)
        radius = 2.0 * math.sqrt(-p / 3.0)

        roots = [
            complex(radius * math.cos(phi / 3.0) - shift, 0.0),
            complex(radius * math.cos((phi + 2.0 * math.pi) / 3.0) - shift, 0.0),
            complex(radius * math.cos((phi + 4.0 * math.pi) / 3.0) - shift, 0.0),
        ]

    return EquationResult("cubic", sort_roots(_clean_complex(root, epsilon) for root in roots))


def format_complex(value: complex, epsilon: float = DEFAULT_EPSILON, precision: int = 12) -> str:
    """Format a complex number for human-readable CLI output."""
    value = _clean_complex(value, epsilon)
    real = value.real
    imag = value.imag

    def fmt(number: float) -> str:
        text = f"{number:.{precision}g}"
        return "0" if text == "-0" else text

    if abs(imag) < epsilon:
        return fmt(real)

    abs_imag = abs(imag)
    imag_text = "i" if abs(abs_imag - 1.0) < epsilon else f"{fmt(abs_imag)}i"

    if abs(real) < epsilon:
        return imag_text if imag > 0 else f"-{imag_text}"

    sign = "+" if imag >= 0 else "-"
    return f"{fmt(real)} {sign} {imag_text}"


def format_result(result: EquationResult) -> str:
    """Return a multi-line string describing an EquationResult."""
    lines = [f"Equation type: {result.equation_type}"]

    if result.infinite_solutions:
        lines.append("Result: infinitely many solutions")
        return "\n".join(lines)

    if result.no_solution:
        lines.append("Result: no solution")
        return "\n".join(lines)

    lines.append("Roots:")
    for index, root in enumerate(result.roots, start=1):
        lines.append(f"  {index}) {format_complex(root)}")
    return "\n".join(lines)
