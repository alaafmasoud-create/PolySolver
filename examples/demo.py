"""Small usage demo for the Python solver."""

from poly_solver import solve_cubic, solve_quadratic
from poly_solver.solver import format_result

examples = [
    ("Quadratic: x^2 - 5x + 6 = 0", solve_quadratic(1, -5, 6)),
    ("Quadratic: x^2 + 1 = 0", solve_quadratic(1, 0, 1)),
    ("Cubic: x^3 - 6x^2 + 11x - 6 = 0", solve_cubic(1, -6, 11, -6)),
    ("Cubic: x^3 - 1 = 0", solve_cubic(1, 0, 0, -1)),
]

for title, result in examples:
    print(title)
    print(format_result(result))
    print("-" * 60)
