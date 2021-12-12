from threading import Thread, Lock
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
    0: {0: -1,
        1: 3},
    1: {0: 4,
        1: 2},
}

def readMatrix(filename):
    matrix = {}
    with open("in/"+ filename + ".txt", 'r') as f:
        dims =[int(num) for num in f.readline().rstrip('\n').strip().split(' ')]
        # tratar exceções caso não tenha isto
        if (len(dims) != 2):
            raise Exception("The first line must have exactly 2 numbers (the dimensions of the matrix")
        
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

def multiplySeq(A,B,n):
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

def multiplyCon(A,B,n):

    def calcCell(A,B,C,n,lock):
        soma = 0
        for k in range(0,n):
            soma = soma + A[i][k] * B[k][j]
        # TODO solve data racing condition
        lock.acquire()
        if i not in C:
            C[i] = {j: soma}
        if i in C:
            C[i].update({j: soma})
        lock.release()

    C = {}  # result
    threads = []
    lock = Lock()
    for i in range(0,n):
        for j in range(0,n):
            t = Thread(target=calcCell, args=(A, B, C, n,lock))
            threads.append(t)
            t.start()
            
    for t in threads:
        t.join()

    return C

#print(multiplySeq(matrix_A,matrix_B,2))
print(multiplySeq(readMatrix("A4x4"), readMatrix("B4x4"), 4))               
# print(readMatrix("B4x4"))

