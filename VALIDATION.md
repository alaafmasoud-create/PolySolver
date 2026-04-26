# Validation Report

Date: 2026-04-26

## Python solver

Command:

```bash
PYTHONPATH=python python -m unittest discover -s tests/python
```

Result:

```text
OK
```

## C++ solver

Commands:

```bash
cmake -S . -B build
cmake --build build
ctest --test-dir build --output-on-failure
```

Result:

```text
100% tests passed
```

## CLI examples checked

```bash
python -m poly_solver.cli quadratic 1 -5 6
python -m poly_solver.cli cubic 1 -6 11 -6
```

Expected roots:

```text
quadratic: 2, 3
cubic: 1, 2, 3
```

## Web App / second platform layer

Added and statically checked:

```text
app.py
requirements.txt
Dockerfile
render.yaml
.streamlit/config.toml
docs/DEPLOY_SECOND_PLATFORM_AR.md
```

The app uses the same tested Python solver module:

```text
python/poly_solver/solver.py
```

To run the web app:

```bash
python -m pip install -r requirements.txt
streamlit run app.py
```
