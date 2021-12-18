#!/bin/bash

PROGRAM_NAME='multiplym.py'
MAX_REPS=20

exec_program(){
    dimension=$1
    exec_mode=$2
    python3 $PROGRAM_NAME $dimension $exec_mode
}

for mode in 'S' 'C'
do 
    # for dimension in 4 8 16 32 64 128 256 1024 2048
    for dimension in 8
    do
        output="out/metrics/${mode}${dimension}_times.txt"
        echo $(date) >> $output
        for reps in {1..2}
        do
            timing=$(exec_program $dimension $mode)
            echo "[$reps/$MAX_REPS] $mode $dimension $timing"
            echo $timing >> $output
            sleep 0.1
        done
    done
done



# for [m in ['S', 'C']]
#     for [n in [2, 8, 16, 32 .. 2048]] :
#         for [i -in 0..20] :
#             exec_program(NOME_DO_PROGRAMA, n, m)