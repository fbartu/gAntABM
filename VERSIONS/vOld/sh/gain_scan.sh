#!/bin/bash

#how to run
#qsub ~/research/AutomatAnts/code/run_model.sh 

cd

export PATH=/home/soft/python-3.9.5/bin:$PATH
export LD_LIBRARY_PATH=/home/soft/python-3.9.5/bin/$LD_LIBRARY_PATH

. ~/research/automatenv/bin/activate
for g in $(seq 0.1 0.05 0.9)
do
    python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/2024/gains/ --filename "g_${g/,/.}" -n 100 -g 100,U,${g/,/.},${g/,/.}
done

deactivate