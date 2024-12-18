#!/bin/bash

cd

export PATH=/home/soft/python-3.9.5/bin:$PATH
export LD_LIBRARY_PATH=/home/soft/python-3.9.5/bin/$LD_LIBRARY_PATH

. ~/research/automatenv/bin/activate
for alpha in $(seq 0.00001 0.00005 0.0075)
do
    for beta in $(seq 0.05 0.1 3)
    do
    python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/with_recruitment/parameter_space/ --filename alpha=${alpha/,/.}_beta=${beta/,/.} -n 100 -p alpha=${alpha/,/.},beta=${beta/,/.}
    done
done
deactivate