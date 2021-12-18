from threading import Thread, Lock
from time import sleep
from aux import *

def calcCell(A,B,C,i,j,n):
    """ Calculates the value of the of the cell C[i][j] where
        C = A x B and attributes it to C.

        All matrixes have nxn dimensions.   
    """
    soma = 0
    for k in range(0,n):
        soma = soma + A[i][k] * B[k][j]
    C[i][j] = soma

def multiplySeq(A,B,n):
    """ Using only one thread, returns the value of the matrix C where
        C = A x B

        All matrixes have nxn dimensions.   
    """
    C = {}
    for i in range(0,n):
        C[i] = {} # prefill matrix dictionaries
        for j in range(0,n):
            calcCell(A,B,C,i,j,n)
    
    return C

def multiplyCon(A,B,n):
    """ Using concurrent proggraming, returns the value of the matrix C where
        C = A x B

        All matrixes have nxn dimensions.   
    """
    threads = []

    C = {}  # result
    for i in range(0,n):
        C[i] = {} # prefill matrix dictionaries
        for j in range(0,n):
            # start threads
            t = Thread(target=calcCell, args=(A, B, C, i,j,n))
            threads.append(t)
            t.start()
            
    # wait for threads to finish
    for t in threads:
        t.join()

    return C

def runAlg(_dimension, _type):
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
    result = {}
    if _type == "S":
        result = multiplySeq(matrix_a, matrix_b, _dimension)
    elif _type == "C":
        result = multiplyCon(matrix_a, matrix_b, _dimension)
    elif _type == "X":  # compare two results
        s = multiplySeq(matrix_a, matrix_b, _dimension)
        c = multiplyCon(matrix_a, matrix_b, _dimension)
        for i in range(0, _dimension):
            for j in range(0, _dimension):
                if s[i][j] != c[i][j] :
                    print(f's[{i}][{j}] = {s[i][j]}; c = {c[i][j]}')
    else:
        raise Exception(f'There is no implementation for _type={_type}')

    return result



if __name__ == "__main__":

    try :
        params = parseArgs()
        if len(params) == 2:
            result = runAlg(params[0], params[1])
            print(result)
    except Exception as err:
        print(err)