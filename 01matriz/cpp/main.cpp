#include <iostream>
#include <vector>
#include <memory>

#include <thread>
#include <functional>
#include <fstream>
#include <string>
#include <stdexcept>
#include <chrono>

using namespace std;
using namespace std::chrono;

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

shared_ptr<matrix> concurrent_multiplication(shared_ptr<matrix> A, shared_ptr<matrix> B) {
    int _size = A->size;
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

void time_it() {
    auto start = high_resolution_clock::now(); 

    shared_ptr<matrix> A, B, C;
    A = make_shared<matrix>(matrix::readFrom("../in/A8x8.txt"));
    B = make_shared<matrix>(matrix::readFrom("../in/B8x8.txt"));
    // clocking
    C = concurrent_multiplication(A,B);
    matrix::print(*C);
    // clocking

    auto stop = high_resolution_clock::now();
    auto duration = duration_cast<milliseconds>(stop - start);
    cout << duration.count() << endl;
}

const string dims_arg_error("the matrix dimensions (n x n) needs to be a power of 2, with 4 < n <= 2048\n");


struct experiment_meta {
    size_t dimension;
    char mode;

    experiment_meta(size_t d, char m) : dimension{d}, mode{m} {};
    experiment_meta(){}

};

experiment_meta parse_args(int argc, char *argv[]) {
    experiment_meta metainfo;
    try{
        auto is_power_of_two = [](int x) { return (x & (x-1)) == 0; };
        // cout << is_power_of_two(11); // false 0
        // cout << is_power_of_two(8); // true 1

        if(argc != 3) {
            throw std::invalid_argument("wrong program usage\n");
        } else {
            string s_dims = argv[1];
            int dims = stoi(s_dims);
            if(dims < 4 || 2048 < dims || (!is_power_of_two(dims)) ) {
                throw std::invalid_argument(dims_arg_error);
            }

            string mode(argv[2]);
            if(mode.compare("S") != 0 & mode.compare("C") != 0) {
                throw std::invalid_argument("enter the algorithm that wil run (\"C\" for concurrent and \"S\" for sequential)\n");
            }

            metainfo = experiment_meta(dims, char(mode[0]));

        }
    } catch (std::exception& e) {
        if (string("stoi").compare(e.what()) == 0) {
            throw std::invalid_argument(dims_arg_error);
        } else {
            throw;
        }
    }

    return metainfo;
}

int main(int argc, char *argv[]) {

    try {
        experiment_meta metainfo = parse_args(argc, argv);
        cout << metainfo.dimension << " " << metainfo.mode << "\n";
    } catch (std::exception& e) {
        cerr << e.what();
    }
    // time_it();
    return 0;
}