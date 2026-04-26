import math
import unittest

from poly_solver import solve_cubic, solve_linear, solve_quadratic


def assert_roots_close(test_case, actual, expected, places=9):
    actual_sorted = sorted(actual, key=lambda z: (round(z.real, 9), round(z.imag, 9)))
    expected_sorted = sorted(expected, key=lambda z: (round(z.real, 9), round(z.imag, 9)))
    test_case.assertEqual(len(actual_sorted), len(expected_sorted))
    for got, want in zip(actual_sorted, expected_sorted):
        test_case.assertAlmostEqual(got.real, want.real, places=places)
        test_case.assertAlmostEqual(got.imag, want.imag, places=places)


class TestEquationSolver(unittest.TestCase):
    def test_linear_single_root(self):
        result = solve_linear(2, -8)
        self.assertFalse(result.no_solution)
        self.assertFalse(result.infinite_solutions)
        assert_roots_close(self, result.roots, [4])

    def test_linear_no_solution(self):
        result = solve_linear(0, 5)
        self.assertTrue(result.no_solution)
        self.assertFalse(result.infinite_solutions)
        self.assertEqual(result.roots, [])

    def test_linear_infinite_solutions(self):
        result = solve_linear(0, 0)
        self.assertTrue(result.infinite_solutions)
        self.assertFalse(result.no_solution)
        self.assertEqual(result.roots, [])

    def test_quadratic_two_real_roots(self):
        result = solve_quadratic(1, -5, 6)
        assert_roots_close(self, result.roots, [2, 3])

    def test_quadratic_double_root(self):
        result = solve_quadratic(1, -2, 1)
        assert_roots_close(self, result.roots, [1, 1])

    def test_quadratic_complex_roots(self):
        result = solve_quadratic(1, 0, 1)
        assert_roots_close(self, result.roots, [-1j, 1j])

    def test_quadratic_degenerates_to_linear(self):
        result = solve_quadratic(0, 2, -8)
        self.assertEqual(result.equation_type, "linear")
        assert_roots_close(self, result.roots, [4])

    def test_cubic_three_real_roots(self):
        result = solve_cubic(1, -6, 11, -6)
        assert_roots_close(self, result.roots, [1, 2, 3])

    def test_cubic_triple_root(self):
        result = solve_cubic(1, -3, 3, -1)
        assert_roots_close(self, result.roots, [1, 1, 1])

    def test_cubic_one_real_two_complex_roots(self):
        result = solve_cubic(1, 0, 0, -1)
        expected = [1, complex(-0.5, math.sqrt(3) / 2), complex(-0.5, -math.sqrt(3) / 2)]
        assert_roots_close(self, result.roots, expected)

    def test_cubic_degenerates_to_quadratic(self):
        result = solve_cubic(0, 1, -5, 6)
        self.assertEqual(result.equation_type, "quadratic")
        assert_roots_close(self, result.roots, [2, 3])

    def test_rejects_nan(self):
        with self.assertRaises(ValueError):
            solve_quadratic(float("nan"), 1, 1)


if __name__ == "__main__":
    unittest.main()
