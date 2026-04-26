# Polynomial Equation Solver — Quadratic & Cubic

A GitHub-ready project for solving **quadratic** and **cubic** equations using both **Python** and **C++**.

The project includes:

- Python package with CLI command
- C++17 library and CLI executable
- Unit tests for Python and C++
- CMake build system
- GitHub Actions CI workflow
- Mathematical notes and examples
- No runtime external dependencies

> Equations supported:
>
> - Quadratic: `a*x^2 + b*x + c = 0`
> - Cubic: `a*x^3 + b*x^2 + c*x + d = 0`
>
> Degenerate cases are handled automatically. For example, if `a = 0` in a quadratic equation, the solver treats it as a linear equation.

---

## Quick Start — Python

From the project root:

```bash
python -m poly_solver.cli quadratic 1 -5 6
python -m poly_solver.cli cubic 1 -6 11 -6
```

Expected output:

```text
Equation type: quadratic
Roots:
  1) 2
  2) 3
```

```text
Equation type: cubic
Roots:
  1) 1
  2) 2
  3) 3
```

### Install as a local package

```bash
python -m pip install -e .
poly-solver quadratic 1 0 1
poly-solver cubic 1 0 0 -1
```

---

## Quick Start — C++

### Build with CMake

```bash
cmake -S . -B build
cmake --build build
```

### Run

Linux/macOS:

```bash
./build/eqsolver quadratic 1 -5 6
./build/eqsolver cubic 1 -6 11 -6
```

Windows PowerShell:

```powershell
.\build\Debug\eqsolver.exe quadratic 1 -5 6
.\build\Debug\eqsolver.exe cubic 1 -6 11 -6
```

---

## Run Tests

### Python tests

```bash
python -m unittest discover -s tests/python
```

### C++ tests

```bash
cmake -S . -B build
cmake --build build
ctest --test-dir build --output-on-failure
```

---

## Project Structure

```text
poly-equation-solver/
├── .github/workflows/ci.yml
├── CMakeLists.txt
├── LICENSE
├── Makefile
├── README.md
├── docs/
│   └── MATH_NOTES.md
├── examples/
│   └── demo.py
├── include/
│   └── poly_solver/
│       └── equations.hpp
├── python/
│   └── poly_solver/
│       ├── __init__.py
│       ├── cli.py
│       └── solver.py
├── src/
│   ├── equations.cpp
│   └── main.cpp
├── tests/
│   ├── cpp/test_equations.cpp
│   └── python/test_solver.py
├── pyproject.toml
└── requirements-dev.txt
```

---



## License

MIT License. See [`LICENSE`](LICENSE).

Authior
Built By Alan Masoud
