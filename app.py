"""Streamlit web app for the Polynomial Equation Solver.

Run locally:
    streamlit run app.py

Deploy on Streamlit Community Cloud:
    App file: app.py
"""

from __future__ import annotations

from dataclasses import asdict
import sys
from pathlib import Path

import streamlit as st

# Make the local package importable when the app is executed directly from the
# repository root without installing the package first.
PROJECT_ROOT = Path(__file__).resolve().parent
PYTHON_SRC = PROJECT_ROOT / "python"
if str(PYTHON_SRC) not in sys.path:
    sys.path.insert(0, str(PYTHON_SRC))

from poly_solver.solver import (  # noqa: E402
    EquationResult,
    format_complex,
    solve_cubic,
    solve_quadratic,
)


def _format_equation(kind: str, coefficients: tuple[float, ...]) -> str:
    """Return a readable equation string."""
    if kind == "quadratic":
        a, b, c = coefficients
        return f"({a:g})x² + ({b:g})x + ({c:g}) = 0"

    a, b, c, d = coefficients
    return f"({a:g})x³ + ({b:g})x² + ({c:g})x + ({d:g}) = 0"


def _render_result(result: EquationResult) -> None:
    """Render a solver result in Streamlit."""
    st.subheader("Result")

    if result.infinite_solutions:
        st.success("Infinitely many solutions.")
        return

    if result.no_solution:
        st.warning("No solution.")
        return

    rows = [
        {"#": index, "Root": format_complex(root), "Real": root.real, "Imaginary": root.imag}
        for index, root in enumerate(result.roots, start=1)
    ]
    st.table(rows)

    with st.expander("Raw result object"):
        raw = asdict(result)
        raw["roots"] = [format_complex(root) for root in result.roots]
        st.json(raw)


def _sample_y(kind: str, coefficients: tuple[float, ...], x: float) -> float:
    """Evaluate the polynomial at x for simple plotting."""
    if kind == "quadratic":
        a, b, c = coefficients
        return a * x * x + b * x + c

    a, b, c, d = coefficients
    return a * x * x * x + b * x * x + c * x + d


def _render_preview_chart(kind: str, coefficients: tuple[float, ...]) -> None:
    """Render a lightweight preview chart without extra dependencies."""
    st.subheader("Polynomial preview")
    x_min, x_max = st.slider("X range", -20.0, 20.0, (-10.0, 10.0), 0.5)
    if x_min >= x_max:
        st.info("Choose a valid range where the minimum is smaller than the maximum.")
        return

    points = 121
    step = (x_max - x_min) / (points - 1)
    data = {
        "x": [x_min + i * step for i in range(points)],
        "y": [_sample_y(kind, coefficients, x_min + i * step) for i in range(points)],
    }
    st.line_chart(data, x="x", y="y")


def main() -> None:
    st.set_page_config(
        page_title="Polynomial Equation Solver",
        page_icon="🧮",
        layout="centered",
    )

    st.title("Polynomial Equation Solver")
    st.caption("Solve quadratic and cubic equations with real or complex roots.")

    equation_type = st.radio(
        "Equation type",
        ["quadratic", "cubic"],
        captions=["a·x² + b·x + c = 0", "a·x³ + b·x² + c·x + d = 0"],
        horizontal=False,
    )

    st.divider()

    if equation_type == "quadratic":
        col1, col2, col3 = st.columns(3)
        with col1:
            a = st.number_input("a", value=1.0, format="%.10g")
        with col2:
            b = st.number_input("b", value=-5.0, format="%.10g")
        with col3:
            c = st.number_input("c", value=6.0, format="%.10g")

        coefficients = (float(a), float(b), float(c))
        solver = lambda: solve_quadratic(*coefficients)
    else:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            a = st.number_input("a", value=1.0, format="%.10g")
        with col2:
            b = st.number_input("b", value=-6.0, format="%.10g")
        with col3:
            c = st.number_input("c", value=11.0, format="%.10g")
        with col4:
            d = st.number_input("d", value=-6.0, format="%.10g")

        coefficients = (float(a), float(b), float(c), float(d))
        solver = lambda: solve_cubic(*coefficients)

    st.code(_format_equation(equation_type, coefficients), language="text")

    if st.button("Solve equation", type="primary"):
        try:
            _render_result(solver())
        except ValueError as exc:
            st.error(str(exc))

    _render_preview_chart(equation_type, coefficients)

    st.divider()
    st.caption("Done with Python, Streamlit, and a matching C++17 solver library.")
    st.markdown("<div style='text-align: center; padding-top: 0.5rem; font-size: 0.65rem;'>Built by Alan Masoud</div>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()
