"""
Suite de tests unitaires pour MATRIXCALC.
Vérifie la précision et le comportement des algorithmes manuels.
"""

import unittest
from core.matrix_operations import matrix_add, matrix_subtract, matrix_multiply, transpose
from core.determinant import determinant
from core.inverse import inverse
from core.gaussian import row_echelon, rref
from core.solver import solve_system
from utils.formatter import format_number

class TestMatrixCalc(unittest.TestCase):

    def test_addition(self):
        A = [[1, 2], [3, 4]]
        B = [[5, 6], [7, 8]]
        C, _ = matrix_add(A, B)
        self.assertEqual(C, [[6, 8], [10, 12]])

    def test_addition_mismatch(self):
        A = [[1, 2]]
        B = [[1], [2]]
        with self.assertRaises(ValueError):
            matrix_add(A, B)

    def test_subtraction(self):
        A = [[5, 6], [7, 8]]
        B = [[1, 2], [3, 4]]
        C, _ = matrix_subtract(A, B)
        self.assertEqual(C, [[4, 4], [4, 4]])

    def test_multiplication(self):
        A = [[1, 2, 3], [4, 5, 6]]
        B = [[7, 8], [9, 1], [2, 3]]
        C, _ = matrix_multiply(A, B)
        # C[0][0] = 1*7 + 2*9 + 3*2 = 7 + 18 + 6 = 31
        # C[0][1] = 1*8 + 2*1 + 3*3 = 8 + 2 + 9 = 19
        # C[1][0] = 4*7 + 5*9 + 6*2 = 28 + 45 + 12 = 85
        # C[1][1] = 4*8 + 5*1 + 6*3 = 32 + 5 + 18 = 55
        self.assertEqual(C, [[31, 19], [85, 55]])

    def test_transpose(self):
        A = [[1, 2, 3], [4, 5, 6]]
        A_T, _ = transpose(A)
        self.assertEqual(A_T, [[1, 4], [2, 5], [3, 6]])

    def test_determinant_2x2(self):
        A = [[4, 6], [3, 8]]
        det, _ = determinant(A)
        self.assertAlmostEqual(det, 14.0)

    def test_determinant_3x3(self):
        A = [[6, 1, 1], [4, -2, 5], [2, 8, 7]]
        det, _ = determinant(A)
        # Det = 6*(-14-40) - 1*(28-10) + 1*(32 - (-4)) = 6*(-54) - 18 + 36 = -324 - 18 + 36 = -306
        self.assertAlmostEqual(det, -306.0)

    def test_inverse(self):
        A = [[4, 7], [2, 6]]
        inv, _, is_inv = inverse(A)
        self.assertTrue(is_inv)
        # Det(A) = 24 - 14 = 10 -> inv = [[0.6, -0.7], [-0.2, 0.4]]
        self.assertAlmostEqual(inv[0][0], 0.6)
        self.assertAlmostEqual(inv[0][1], -0.7)
        self.assertAlmostEqual(inv[1][0], -0.2)
        self.assertAlmostEqual(inv[1][1], 0.4)

    def test_non_invertible(self):
        A = [[1, 2], [2, 4]]
        inv, _, is_inv = inverse(A)
        self.assertFalse(is_inv)
        self.assertIsNone(inv)

    def test_solve_system_unique(self):
        # x + 2y = 5
        # 3x + 4y = 11
        # => x = 1, y = 2
        A = [[1, 2], [3, 4]]
        B = [5, 11]
        sol_type, vec, _, _, _ = solve_system(A, B)
        self.assertEqual(sol_type, "UNIQUE")
        self.assertAlmostEqual(vec[0], 1.0)
        self.assertAlmostEqual(vec[1], 2.0)

    def test_solve_system_no_solution(self):
        # x + y = 2
        # x + y = 5
        A = [[1, 1], [1, 1]]
        B = [2, 5]
        sol_type, vec, _, _, _ = solve_system(A, B)
        self.assertEqual(sol_type, "NONE")
        self.assertIsNone(vec)

    def test_solve_system_infinite(self):
        # x + y = 2
        # 2x + 2y = 4
        A = [[1, 1], [2, 2]]
        B = [2, 4]
        sol_type, vec, _, _, _ = solve_system(A, B)
        self.assertEqual(sol_type, "INFINITE")
        self.assertIsNone(vec)

    def test_format_number(self):
        self.assertEqual(format_number(2.0), "2")
        self.assertEqual(format_number(-3.0), "-3")
        self.assertEqual(format_number(4.5), "4.5")
        self.assertEqual(format_number(2.0000000000000004), "2")

if __name__ == "__main__":
    unittest.main()
