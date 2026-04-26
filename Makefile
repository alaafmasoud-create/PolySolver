PYTHON ?= python3
BUILD_DIR ?= build

.PHONY: help test test-python configure build test-cpp clean run-python run-cpp

help:
	@echo "Available commands:"
	@echo "  make test-python  - Run Python unit tests"
	@echo "  make configure    - Configure CMake build"
	@echo "  make build        - Build C++ executable"
	@echo "  make test-cpp     - Run C++ tests"
	@echo "  make test         - Run Python and C++ tests"
	@echo "  make clean        - Remove build artifacts"

run-python:
	$(PYTHON) -m poly_solver.cli cubic 1 -6 11 -6

configure:
	cmake -S . -B $(BUILD_DIR)

build: configure
	cmake --build $(BUILD_DIR)

run-cpp: build
	./$(BUILD_DIR)/eqsolver cubic 1 -6 11 -6

test-python:
	$(PYTHON) -m unittest discover -s tests/python

test-cpp: build
	ctest --test-dir $(BUILD_DIR) --output-on-failure

test: test-python test-cpp

clean:
	rm -rf $(BUILD_DIR) *.egg-info python/*.egg-info
