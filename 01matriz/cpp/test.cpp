#include <iostream>
#include <vector>
#include <memory>

#include <thread>
#include <functional>
#include <fstream>
#include <string>
#include <stdexcept>

using namespace std;

struct matrix {
    int size;
    vector<shared_ptr<int>> data;

    matrix(){}

    void fill() {
        data = vector<shared_ptr<int>>(size*size);
        for ( int i = 0; i < size; ++i) {
            for (int j = 0; j < size; ++j) {
                data[(i*size)+j] = make_shared<int>(0);
            }
        }
    }

    static void print(matrix& m) {
        for ( int i = 0; i < m.size; ++i) {
            cout << "[ ";
            for (int j = 0; j < m.size; ++j) {
                cout << *(m.data[(i*m.size)+j]) << " ";
            }
            cout << "]\n";
        }
    }

    static matrix readFrom(string filepath) {
            matrix M = matrix();
            try {
                ifstream file(filepath);
                if(file.is_open()) {
                    file >> M.size; // get dimension

                    string foo;
                    int val;
                    getline (file, foo); // skip current line

                    M.data = vector<shared_ptr<int>>(M.size*M.size);
                    for (int i = 0; i < M.size; i++) {
                        for (int j = 0; j < M.size; j++) {
                            file >> val;
                            M.data[i*M.size+j] = make_shared<int>(val);
                        }
                    }
                    file.close();
                }
            } catch(const std::exception& e) {
                cerr << e.what();
            }
            return M;
        }
};

// typedef shared_ptr<matrix> matrix_ptr;

void calculate_cell(
    matrix& A, matrix& B, matrix& C,
    const int i, const int j,
    const size_t n)
{
    int sum = 0;
    for (int k = 0; k < n; k++) {
        sum = sum + (*A.data[i*n+k]) * (*B.data[k*n+j]);
    }
    C.data[i*n+j] = make_shared<int>(sum);
}

shared_ptr<matrix> concurrent_multiplication(shared_ptr<matrix> A, shared_ptr<matrix> B, size_t _size) {
    shared_ptr<matrix> C = make_shared<matrix>();

    vector<thread> threads = vector<thread>(_size * _size);
             
    C->data = vector<shared_ptr<int>>(_size * _size);
    C->size = _size;
    for(int i = 0; i < _size; i++) {
        for(int j = 0; j < _size; j++) {
            thread th(ref(calculate_cell), ref(*A), ref(*B), ref(*C), i, j, _size);
            threads.push_back(move(th));
        }
    }

    for (thread &th : threads) {
        if(th.joinable())
            th.join();
    }

    return C;
}


int main() {

    shared_ptr<matrix> A, B, C;
    A = make_shared<matrix>(matrix::readFrom("../ref/A2x2.txt"));
    B = make_shared<matrix>(matrix::readFrom("../ref/B2x2.txt"));
    C = concurrent_multiplication(A,B,2);
    matrix::print(*C);

    return 0;
}