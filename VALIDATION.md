# Validation Report

The project was validated before packaging.

## Python

Command:

```bash
PYTHONPATH=python python -m unittest discover -s tests/python
```

Result:

```text
Ran 12 tests
OK
```

CLI smoke test:

```bash
PYTHONPATH=python python -m poly_solver.cli cubic 1 -6 11 -6
```

Output:

```text
Equation type: cubic
Roots:
  1) 1
  2) 2
  3) 3
```

## C++

Commands:

```bash
cmake -S . -B build
cmake --build build
ctest --test-dir build --output-on-failure
```

Result:

```text
100% tests passed, 0 tests failed out of 1
```

CLI smoke test:

```bash
./build/eqsolver cubic 1 -6 11 -6
```

Output:

```text
Equation type: cubic
Roots:
  1) 1
  2) 2
  3) 3
```
