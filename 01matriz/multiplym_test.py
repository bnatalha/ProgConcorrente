import unittest

from multiplym import *

CASE_A = {
    "A" : {
        0: {0: 1,
            1: 2},
        1: {0: 3,
            1: 4},
    },
    "B" : {
        0: {0: -1,
            1: 3},
        1: {0: 4,
            1: 2},
    },
    "C" : {
        0: {0: 7,
            1: 7},
        1: {0: 13,
            1: 17},
    },
}


class MatrixMultiplicationTest(unittest.TestCase):
    """
    Test case A:
 
        1, 2        -1, 3       7, 7
        3, 4    x    4, 2   =   13,17

    """
    def test_multiply_case_A_sequential(self):
        r = multiplySeq(MATRIX_A, MATRIX_B, 2)

        self.assertEqual(MATRIX_RESULT, r)

    def test_multiply_case_A_concurrent(self):
        r = multiplyCon(MATRIX_A, MATRIX_B, 2)

        self.assertEqual(MATRIX_RESULT, r)

if __name__ == '__main__':
    unittest.main()