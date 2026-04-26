#include "poly_solver/equations.hpp"

#include <cassert>
#include <cmath>
#include <complex>
#include <iostream>
#include <vector>

namespace {

bool near(double a, double b, double eps = 1e-8) {
    return std::abs(a - b) < eps;
}

void assert_roots_close(
    std::vector<std::complex<double>> actual,
    std::vector<std::complex<double>> expected
) {
    actual = poly_solver::sort_roots(actual);
    expected = poly_solver::sort_roots(expected);
    assert(actual.size() == expected.size());
    for (std::size_t i = 0; i < actual.size(); ++i) {
        assert(near(actual[i].real(), expected[i].real()));
        assert(near(actual[i].imag(), expected[i].imag()));
    }
}

}  // namespace

int main() {
    using poly_solver::solve_cubic;
    using poly_solver::solve_linear;
    using poly_solver::solve_quadratic;

    {
        const auto result = solve_linear(2, -8);
        assert(!result.no_solution);
        assert(!result.infinite_solutions);
        assert_roots_close(result.roots, {{4, 0}});
    }

    {
        const auto result = solve_linear(0, 5);
        assert(result.no_solution);
        assert(result.roots.empty());
    }

    {
        const auto result = solve_linear(0, 0);
        assert(result.infinite_solutions);
        assert(result.roots.empty());
    }

    {
        const auto result = solve_quadratic(1, -5, 6);
        assert_roots_close(result.roots, {{2, 0}, {3, 0}});
    }

    {
        const auto result = solve_quadratic(1, -2, 1);
        assert_roots_close(result.roots, {{1, 0}, {1, 0}});
    }

    {
        const auto result = solve_quadratic(1, 0, 1);
        assert_roots_close(result.roots, {{0, -1}, {0, 1}});
    }

    {
        const auto result = solve_quadratic(0, 2, -8);
        assert(result.equation_type == "linear");
        assert_roots_close(result.roots, {{4, 0}});
    }

    {
        const auto result = solve_cubic(1, -6, 11, -6);
        assert_roots_close(result.roots, {{1, 0}, {2, 0}, {3, 0}});
    }

    {
        const auto result = solve_cubic(1, -3, 3, -1);
        assert_roots_close(result.roots, {{1, 0}, {1, 0}, {1, 0}});
    }

    {
        const auto result = solve_cubic(1, 0, 0, -1);
        const double s3 = std::sqrt(3.0) / 2.0;
        assert_roots_close(result.roots, {{1, 0}, {-0.5, s3}, {-0.5, -s3}});
    }

    {
        const auto result = solve_cubic(0, 1, -5, 6);
        assert(result.equation_type == "quadratic");
        assert_roots_close(result.roots, {{2, 0}, {3, 0}});
    }

    std::cout << "All C++ equation solver tests passed.\n";
    return 0;
}
