import unittest

from multiplym import *
from aux import readMatrix


"""
    Test case 1:
 
        1, 2        -1, 3       7, 7
        3, 4    x    4, 2   =   13,17
"""
CASE_1 = {
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

def get_sequential_and_concurrent(dimension):
    n = str(dimension)
    A = readMatrix(inputFilename("A",n)) 
    B = readMatrix(inputFilename("B",n)) 
    
    c1 = sequential_multiplication(A, B, dimension)
    c2 = concurrent_multiplication(A, B, dimension)

    # printMatrix(c1)
    # printMatrix(c2)

    return (c1, c2)

class MatrixMultiplicationTest(unittest.TestCase):
    
    def test_multiply_case_1_sequential(self):
        r = sequential_multiplication(CASE_1["A"], CASE_1["B"], 2)
        self.assertEqual(CASE_1["C"], r)

    def test_multiply_case_1_concurrent(self):
        r = concurrent_multiplication(CASE_1["A"], CASE_1["B"], 2)
        self.assertEqual(CASE_1["C"], r)

    def test_should_get_same_result_4x4(self):
        c1, c2 = get_sequential_and_concurrent(4)
        self.assertEqual(c1, c2)

    def test_should_get_same_result_8x8(self):
        c1, c2 = get_sequential_and_concurrent(8)
        self.assertEqual(c1, c2)

    def test_should_get_same_result_16x16(self):
        c1, c2 = get_sequential_and_concurrent(16)
        self.assertEqual(c1, c2)

    def test_should_get_same_result_32x32(self):
        c1, c2 = get_sequential_and_concurrent(32)
        self.assertEqual(c1, c2)

    def test_should_get_same_result_64x64(self):
        c1, c2 = get_sequential_and_concurrent(64)
        self.assertEqual(c1, c2)

    def test_should_get_same_result_128x128(self):
        c1, c2 = get_sequential_and_concurrent(128)
        self.assertEqual(c1, c2)

    def test_should_get_same_result_256x256(self):
        c1, c2 = get_sequential_and_concurrent(256)
        self.assertEqual(c1, c2)

    # def test_should_get_same_result_512x512(self):
    #     c1, c2 = get_sequential_and_concurrent(512)
    #     self.assertEqual(c1, c2)

    # def test_should_get_same_result_1024x1024(self):
    #     c1, c2 = get_sequential_and_concurrent(1024)
    #     self.assertEqual(c1, c2)

    # def test_should_get_same_result_2048x2048(self):
    #     c1, c2 = get_sequential_and_concurrent(2048)
    #     self.assertEqual(c1, c2)

if __name__ == '__main__':
    unittest.main()