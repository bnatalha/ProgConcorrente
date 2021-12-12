from threading import Thread
from time import sleep

# TODO: usar mapa ou lista?

""" 
    1, 2
    3, 4
"""
matrix_A = {
    0: {0: 1,
        1: 2},
    1: {0: 3,
        1: 4},
}

matrix_B = {
    0: {0: 5,
        1: 6},
    1: {0: 7,
        1: 8},
}

def multiply(A,B,n):
    C = {}
    for i in range(0,n):
        for j in range(0,n):
            soma = 0
            for k in range(0,n):
                soma = soma + A[i][k] * B[k][j]
            if i not in C:
                C[i] = {j: soma}
            if i in C:
                C[i].update({j: soma})
    
    return C

print(multiply(matrix_A, matrix_B, 2))               


