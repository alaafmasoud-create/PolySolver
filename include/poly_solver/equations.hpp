#pragma once

#include <complex>
#include <string>
#include <vector>

namespace poly_solver {

constexpr double DEFAULT_EPSILON = 1e-12;

struct EquationResult {
    std::string equation_type;
    std::vector<std::complex<double>> roots;
    bool infinite_solutions = false;
    bool no_solution = false;
};

bool is_near_zero(double value, double epsilon = DEFAULT_EPSILON);
std::vector<std::complex<double>> sort_roots(std::vector<std::complex<double>> roots);
EquationResult solve_linear(double a, double b, double epsilon = DEFAULT_EPSILON);
EquationResult solve_quadratic(double a, double b, double c, double epsilon = DEFAULT_EPSILON);
EquationResult solve_cubic(double a, double b, double c, double d, double epsilon = DEFAULT_EPSILON);
std::string format_complex(std::complex<double> value, double epsilon = DEFAULT_EPSILON, int precision = 12);
std::string format_result(const EquationResult& result);

}  // namespace poly_solver
