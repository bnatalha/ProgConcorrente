from threading import Thread, Lock
from aux import *

def calculate_cell(A,B,C,i,j,n):
    """ Calculates the value of the of the cell C[i][j] where
        C = A x B and attributes it to C.

        All matrixes have nxn dimensions.   
    """
    soma = 0
    for k in range(0,n):
        soma = soma + A[i][k] * B[k][j]
    C[i][j] = soma

def sequential_multiplication(A,B,n):
    """ Using only one thread, returns the value of the matrix C where
        C = A x B

        All matrixes have nxn dimensions.   
    """
    C = {}
    for i in range(0,n):
        C[i] = {} # prefill matrix dictionaries
        for j in range(0,n):
            calculate_cell(A,B,C,i,j,n)
    
    return C

def concurrent_multiplication(A,B,n):
    """ Using concurrent programming, returns the value of the matrix C where
        C = A x B

        All matrixes have nxn dimensions.   
    """
    threads = []

    C = {}  # result
    for i in range(0,n):
        C[i] = {} # prefill matrix dictionaries
        for j in range(0,n):
            # start threads
            t = Thread(target=calculate_cell, args=(A, B, C, i,j,n))
            threads.append(t)
            t.start()
            
    # wait for threads to finish
    for t in threads:
        t.join()

    return C

def run(_dimension, _type):
    """ Will execute the matrix multiplication as defined by
        the _dimension and the _type  
    """

    # build the filenames
    matrix_a_path = inputFilename("A", str(_dimension))
    matrix_b_path = inputFilename("B", str(_dimension))

    # read the matrixes
    matrix_a = readMatrix(matrix_a_path)
    matrix_b = readMatrix(matrix_b_path)

    # multiply using one of the strategies
    selectAlg = lambda t : (sequential_multiplication if _type == 'S' else concurrent_multiplication)
    multiply = timing(selectAlg(_type))
    result, elapsed_time, meta_info = multiply(matrix_a, matrix_b, _dimension)
    writeMatrix(result, _dimension, _type)
    return result, elapsed_time



if __name__ == "__main__":

    try :
        params = parseArgs()
        if len(params) == 2:
            result, elapsed_time = run(*params)
            print('%2.4f' % (elapsed_time))
    except Exception as err:
        print(f'Error: {err}')