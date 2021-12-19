import sys

def printMatrix(M):
    for i in M.keys():
        print(M[i])

inputFilename = lambda prefix, n : f'../in/{prefix}{n}x{n}.txt'

def readMatrix(filename):
    matrix = {}
    with open(filename, 'r') as f:
        dims =[int(num) for num in f.readline().rstrip('\n').strip().split(' ')]
        # TODO treat exceptions
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

def parseArgs():
    """ Returns a tuple with the expected program's params if they were passed
        correctly; else, raise an exception.
    """

    args = [arg for arg in sys.argv[1:] if not arg.startswith("-")]

    isPowerOfTwo = lambda x : (x & (x-1)) == 0

    error = ""
    dimensions = 0
    alg_type = ""

    if len(args) != 2:
        error = "wrong program usage, try this instead:" \
          '\n multiplym N S'  \
          '\n\tN: dimenssions of the matrix' \
          '\n\tS | C : (S)equencial or (C)oncurrent'
             
    else: 
        dimensions = int(args[0])
        alg_type = args[1]
        if dimensions < 4 or 2048 < dimensions or (not isPowerOfTwo(dimensions)):
            error = 'the matrix dimensions (n x n) needs to be a power of 2, with 4 <= n <= 2048' \
                f'\nrecieved: {dimensions}'
            
        elif alg_type not in ['S', 'C']:
            error = 'enter the algorithm that wil run (\"C\" for concurrent and \"S\" for sequential)' \
                f'\nrecieved: {alg_type}'
    
    if error == "":
        return (dimensions, alg_type)
    else:
        raise Exception(error)

import os
import errno

def writeMatrix(C, n, mode):
    filename = f'out/{mode}{n}x{n}.txt'

    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    # write result
    with open(filename, 'w') as f:
        f.write(f'{n} {n}\n')
        for i in C.keys():
            line = [str(C[i][j]) for j in C[i].keys()]
            f.write(" ".join(line) + "\n")  


from functools import wraps
from time import time

def timing(f):
    """ Timing wrapper """      
    @wraps(f)
    def wrap(*args, **kw):
        """ Returns a tuple with the resultant matrix, the total elapsed time
            and metainfo
        """      
        # start the clock
        ts = time()
        result = f(*args, **kw)
        te = time()
        # finish the clock
        total_time = te-ts

        meta_info = 'func:%r dimension:%r took: %2.4f sec' % \
            (f.__name__, args[2], total_time)
        

        return (result, total_time, meta_info)
    return wrap
