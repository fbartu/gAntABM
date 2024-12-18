#!/bin/bash

#how to run
#qsub ~/research/AutomatAnts/code/run_model.sh 

cd

export PATH=/home/soft/python-3.9.5/bin:$PATH
export LD_LIBRARY_PATH=/home/soft/python-3.9.5/bin/$LD_LIBRARY_PATH

. ~/research/automatenv/bin/activate
for sd in $(seq 0.1 0.05 0.3)
do
    python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/gains/ --filename "gain=N(0.5,${sd/,/.})" -n 100 -g 100,N,0.5,${sd/,/.}
done

for p in $(seq 50 10 90)
do
    python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/gains/ --filename $p,U,0,0.5:$((100-$p)),U,0.5,1 -n 100 -g $p,U,0,0.5:$((100-$p)),U,0.5,1
done

deactivate