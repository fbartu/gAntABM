#!/bin/bash

#how to run
#qsub ~/research/AutomatAnts/code/run_model.sh 

cd

export PATH=/home/soft/python-3.9.5/bin:$PATH
export LD_LIBRARY_PATH=/home/soft/python-3.9.5/bin/$LD_LIBRARY_PATH

. ~/research/automatenv/bin/activate
# for alpha in $(seq 0.00004 0.00004 0.0012)
for alpha in $(seq 0.00004 0.00005 0.00053)
do
    # for beta in $(seq 0.05 0.1 3)
    for beta in $(seq 0.05 0.2 3)
    do
    python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/parameter_space/ --filename alpha=${alpha/,/.}_beta=${beta/,/.} -n 100 -p alpha=${alpha/,/.},beta=${beta/,/.}
    # python3 ~/research/2022/ANTS/AutomatAnts/code/run_cluster.py --directory ~/research/2022/ANTS/AutomatAnts/results/parameter_space/ --filename alpha=${alpha/,/.}_beta=${beta/,/.} -n 100 -p alpha=${alpha/,/.},beta=${beta/,/.}
    done
done
# deactivate