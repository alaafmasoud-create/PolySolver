#include "poly_solver/equations.hpp"

#include <algorithm>
#include <cmath>
#include <iomanip>
#include <limits>
#include <sstream>
#include <stdexcept>

namespace poly_solver {
namespace {
constexpr double PI = 3.141592653589793238462643383279502884;

void validate_finite(double value, const char* name) {
    if (!std::isfinite(value)) {
        throw std::invalid_argument(std::string(name) + " must be a finite number");
    }
}

std::complex<double> clean_complex(std::complex<double> z, double epsilon) {
    double real = std::abs(z.real()) < epsilon ? 0.0 : z.real();
    double imag = std::abs(z.imag()) < epsilon ? 0.0 : z.imag();
    return {real, imag};
}

}  // namespace

bool is_near_zero(double value, double epsilon) {
    return std::abs(value) < epsilon;
}

std::vector<std::complex<double>> sort_roots(std::vector<std::complex<double>> roots) {
    std::sort(roots.begin(), roots.end(), [](const auto& left, const auto& right) {
        constexpr double eps = 1e-10;
        if (std::abs(left.real() - right.real()) > eps) {
            return left.real() < right.real();
        }
        return left.imag() < right.imag();
    });
    return roots;
}

EquationResult solve_linear(double a, double b, double epsilon) {
    validate_finite(a, "a");
    validate_finite(b, "b");

    EquationResult result;
    result.equation_type = "linear";

    if (is_near_zero(a, epsilon)) {
        if (is_near_zero(b, epsilon)) {
            result.infinite_solutions = true;
        } else {
            result.no_solution = true;
        }
        return result;
    }

    result.roots.push_back(clean_complex({-b / a, 0.0}, epsilon));
    return result;
}

EquationResult solve_quadratic(double a, double b, double c, double epsilon) {
    validate_finite(a, "a");
    validate_finite(b, "b");
    validate_finite(c, "c");

    if (is_near_zero(a, epsilon)) {
        return solve_linear(b, c, epsilon);
    }

    EquationResult result;
    result.equation_type = "quadratic";

    const double discriminant = b * b - 4.0 * a * c;
    const std::complex<double> sqrt_discriminant = std::sqrt(std::complex<double>(discriminant, 0.0));

    // Numerically stable quadratic formula.
    if (discriminant >= 0.0) {
        const double sqrt_d = std::sqrt(std::max(0.0, discriminant));
        const double sign_b = b >= 0.0 ? 1.0 : -1.0;
        const double q = -0.5 * (b + sign_b * sqrt_d);

        if (is_near_zero(q, epsilon)) {
            const std::complex<double> root = clean_complex({-b / (2.0 * a), 0.0}, epsilon);
            result.roots = {root, root};
        } else {
            result.roots = {
                clean_complex({q / a, 0.0}, epsilon),
                clean_complex({c / q, 0.0}, epsilon)
            };
        }
    } else {
        result.roots = {
            clean_complex((-b + sqrt_discriminant) / (2.0 * a), epsilon),
            clean_complex((-b - sqrt_discriminant) / (2.0 * a), epsilon)
        };
    }

    result.roots = sort_roots(result.roots);
    return result;
}

EquationResult solve_cubic(double a, double b, double c, double d, double epsilon) {
    validate_finite(a, "a");
    validate_finite(b, "b");
    validate_finite(c, "c");
    validate_finite(d, "d");

    if (is_near_zero(a, epsilon)) {
        return solve_quadratic(b, c, d, epsilon);
    }

    EquationResult result;
    result.equation_type = "cubic";

    // Normalize: x^3 + A*x^2 + B*x + C = 0
    const double A = b / a;
    const double B = c / a;
    const double C = d / a;

    // Depressed cubic: y^3 + p*y + q = 0, x = y - A/3
    const double p = B - (A * A) / 3.0;
    const double q = (2.0 * A * A * A) / 27.0 - (A * B) / 3.0 + C;
    const double shift = A / 3.0;
    const double discriminant = (q * q) / 4.0 + (p * p * p) / 27.0;

    if (discriminant > epsilon) {
        // One real root and two complex conjugate roots.
        const double sqrt_disc = std::sqrt(discriminant);
        const double u = std::cbrt(-q / 2.0 + sqrt_disc);
        const double v = std::cbrt(-q / 2.0 - sqrt_disc);

        const double y1 = u + v;
        const double real_part = -(u + v) / 2.0;
        const double imag_part = (std::sqrt(3.0) / 2.0) * (u - v);

        result.roots = {
            clean_complex({y1 - shift, 0.0}, epsilon),
            clean_complex({real_part - shift, imag_part}, epsilon),
            clean_complex({real_part - shift, -imag_part}, epsilon)
        };
    } else if (std::abs(discriminant) <= epsilon) {
        // Multiple real roots.
        const double u = std::cbrt(-q / 2.0);
        result.roots = {
            clean_complex({2.0 * u - shift, 0.0}, epsilon),
            clean_complex({-u - shift, 0.0}, epsilon),
            clean_complex({-u - shift, 0.0}, epsilon)
        };
    } else {
        // Three distinct real roots. For this branch p is negative.
        const double acos_arg_raw = (3.0 * q / (2.0 * p)) * std::sqrt(-3.0 / p);
        const double acos_arg = std::max(-1.0, std::min(1.0, acos_arg_raw));
        const double phi = std::acos(acos_arg);
        const double radius = 2.0 * std::sqrt(-p / 3.0);

        result.roots = {
            clean_complex({radius * std::cos(phi / 3.0) - shift, 0.0}, epsilon),
            clean_complex({radius * std::cos((phi + 2.0 * PI) / 3.0) - shift, 0.0}, epsilon),
            clean_complex({radius * std::cos((phi + 4.0 * PI) / 3.0) - shift, 0.0}, epsilon)
        };
    }

    result.roots = sort_roots(result.roots);
    return result;
}

std::string format_complex(std::complex<double> value, double epsilon, int precision) {
    value = clean_complex(value, epsilon);

    std::ostringstream out;
    out << std::setprecision(precision);

    const double real = value.real();
    const double imag = value.imag();

    if (std::abs(imag) < epsilon) {
        out << real;
        return out.str();
    }

    if (std::abs(real) >= epsilon) {
        out << real;
        out << (imag >= 0.0 ? " + " : " - ");
    } else if (imag < 0.0) {
        out << "-";
    }

    const double abs_imag = std::abs(imag);
    if (std::abs(abs_imag - 1.0) < epsilon) {
        out << "i";
    } else {
        out << abs_imag << "i";
    }

    return out.str();
}

std::string format_result(const EquationResult& result) {
    std::ostringstream out;
    out << "Equation type: " << result.equation_type << '\n';

    if (result.infinite_solutions) {
        out << "Result: infinitely many solutions\n";
        return out.str();
    }
    if (result.no_solution) {
        out << "Result: no solution\n";
        return out.str();
    }

    out << "Roots:\n";
    for (std::size_t i = 0; i < result.roots.size(); ++i) {
        out << "  " << (i + 1) << ") " << format_complex(result.roots[i]) << '\n';
    }
    return out.str();
}

}  // namespace poly_solver
