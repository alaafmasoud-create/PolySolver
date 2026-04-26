#include "poly_solver/equations.hpp"

#include <cstdlib>
#include <exception>
#include <iostream>
#include <string>

namespace {

double parse_double(const char* raw, const std::string& name) {
    try {
        std::size_t pos = 0;
        const std::string text(raw);
        const double value = std::stod(text, &pos);
        if (pos != text.size()) {
            throw std::invalid_argument("trailing characters");
        }
        return value;
    } catch (const std::exception&) {
        throw std::invalid_argument("Invalid numeric value for " + name + ": " + raw);
    }
}

void print_usage(const char* program_name) {
    std::cerr
        << "Usage:\n"
        << "  " << program_name << " quadratic <a> <b> <c>\n"
        << "  " << program_name << " cubic <a> <b> <c> <d>\n\n"
        << "Examples:\n"
        << "  " << program_name << " quadratic 1 -5 6\n"
        << "  " << program_name << " cubic 1 -6 11 -6\n";
}

}  // namespace

int main(int argc, char** argv) {
    try {
        if (argc < 2) {
            print_usage(argv[0]);
            return EXIT_FAILURE;
        }

        const std::string mode = argv[1];

        if (mode == "quadratic") {
            if (argc != 5) {
                print_usage(argv[0]);
                return EXIT_FAILURE;
            }
            const double a = parse_double(argv[2], "a");
            const double b = parse_double(argv[3], "b");
            const double c = parse_double(argv[4], "c");
            const auto result = poly_solver::solve_quadratic(a, b, c);
            std::cout << poly_solver::format_result(result);
            return EXIT_SUCCESS;
        }

        if (mode == "cubic") {
            if (argc != 6) {
                print_usage(argv[0]);
                return EXIT_FAILURE;
            }
            const double a = parse_double(argv[2], "a");
            const double b = parse_double(argv[3], "b");
            const double c = parse_double(argv[4], "c");
            const double d = parse_double(argv[5], "d");
            const auto result = poly_solver::solve_cubic(a, b, c, d);
            std::cout << poly_solver::format_result(result);
            return EXIT_SUCCESS;
        }

        std::cerr << "Unknown mode: " << mode << "\n";
        print_usage(argv[0]);
        return EXIT_FAILURE;
    } catch (const std::exception& error) {
        std::cerr << "Error: " << error.what() << "\n";
        return EXIT_FAILURE;
    }
}
