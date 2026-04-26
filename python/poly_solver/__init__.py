"""Polynomial equation solver package."""

from .solver import EquationResult, format_complex, solve_cubic, solve_linear, solve_quadratic

__all__ = [
    "EquationResult",
    "format_complex",
    "solve_linear",
    "solve_quadratic",
    "solve_cubic",
]

__version__ = "1.0.0"
