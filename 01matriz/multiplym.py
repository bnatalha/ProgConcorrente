from threading import Thread, Lock
from time import sleep
import sys

def printMatrix(M):
    for i in M.keys():
        print(M[i])


def readMatrix(filename):
    matrix = {}
    with open(filename, 'r') as f:
        dims =[int(num) for num in f.readline().rstrip('\n').strip().split(' ')]
        # tratar exceções caso não tenha isto
        if (len(dims) != 2):
            raise Exception("The first line must have exactly 2 numbers (the dimensions of the matrix)")
        
        for i in range(0, dims[0]):
            line = f.readline().strip().rstrip('\n').split(' ')
            # print(line) #DEBUG
            for j in range(0, len(line)): # ou dims[-1]
                val = int(line[j].strip())
                if i not in matrix:
                   matrix[i] = {j: val}
                if i in matrix:
                   matrix[i].update({j: val})
    return matrix
    # print(matrix) #DEBUG

def calcCell(A,B,C,i,j,n):
    soma = 0
    for k in range(0,n):
        soma = soma + A[i][k] * B[k][j]
    C[i][j] = soma

def multiplySeq(A,B,n):
    C = {}
    for i in range(0,n):
        C[i] = {} # prefill matrix dictionaries
        for j in range(0,n):
            calcCell(A,B,C,i,j,n)
    
    return C

def multiplyCon(A,B,n):
    threads = []

    C = {}  # result
    for i in range(0,n):
        C[i] = {} # prefill matrix dictionaries
        for j in range(0,n):
            t = Thread(target=calcCell, args=(A, B, C, i,j,n))
            threads.append(t)
            t.start()
            
    for t in threads:
        t.join()

    return C

def runAlg(_dimension, _type):
    
    inputFilename = lambda prefix, n : f'in/{prefix}{n}x{n}.txt'
    
    # build filenames
    matrix_a_path = inputFilename("A", str(_dimension))
    matrix_b_path = inputFilename("B", str(_dimension))

    # read matrixes
    matrix_a = readMatrix(matrix_a_path)
    matrix_b = readMatrix(matrix_b_path)

    # multiply
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


## Program arguments
args = [arg for arg in sys.argv[1:] if not arg.startswith("-")]

if __name__ == "__main__":

    isPowerOfTwo = lambda x : (x & (x-1)) == 0

    # args parser
    if len(args) != 2:
        print("wrong program usage")
    else: 
        dimensions = int(args[0])
        alg_type = args[1]
        if dimensions < 4 or 2048 < dimensions or (not isPowerOfTwo(dimensions)):
            print('matrix dimensions n needs to be a power of 2, with 4 < n <= 2048')
            print(f'recieved: {dimension}')
        elif alg_type not in ['S', 'C', 'X']:
            print(f'enter the algorithm that wil run ({C} for the concurrent and {S} for the sequential version)')
            print(f'recieved: {alg_type}')
        else:
            result = runAlg(dimensions, alg_type)
            print(result)
    
    # print(multiplySeq(matrix_A,matrix_B,2))
    # print(multiplySeq(readMatrix("A4x4"), readMatrix("B4x4"), 4))               
    # print(readMatrix("B4x4"))