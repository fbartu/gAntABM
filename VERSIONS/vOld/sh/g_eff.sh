#!/bin/bash

#how to run
#qsub ~/research/AutomatAnts/code/run_model.sh 

cd

export PATH=/home/soft/python-3.9.5/bin:$PATH
export LD_LIBRARY_PATH=/home/soft/python-3.9.5/bin/$LD_LIBRARY_PATH

. ~/research/automatenv/bin/activate

for g in $(seq 0.1 0.05 0.9)
do
    python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/2024/scenarios/g_eff/J_0/ --filename g_${g/,/.}_J_0/ -n 100 -p "Jij={'0-0':0, '0-1':0,'1-0':0,'1-1':0}" -g 100,U,${g/,/.},${g/,/.}
    python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/2024/scenarios/g_eff/J_0.01/ --filename g_${g/,/.}_J_0.01 -n 100 -p "Jij={'0-0':0.01, '0-1':0.01,'1-0':0.01,'1-1':0.01}" -g 100,U,${g/,/.},${g/,/.}
    python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/2024/scenarios/g_eff/J11_0/ --filename g_${g/,/.}_J11_0 -n 100 -p "Jij={'0-0':0.01, '0-1':0,'1-0':0.01,'1-1':0}" -g 100,U,${g/,/.},${g/,/.}
    python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/2024/scenarios/g_eff/J00_1/ --filename g_${g/,/.}_J00_1 -n 100 -p "Jij={'0-0':1, '0-1':1,'1-0':1,'1-1':1}" -g 100,U,${g/,/.},${g/,/.}
done
