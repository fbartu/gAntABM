#!/bin/bash

#how to run
#qsub ~/research/AutomatAnts/code/run_model.sh 

cd

export PATH=/home/soft/python-3.9.5/bin:$PATH
export LD_LIBRARY_PATH=/home/soft/python-3.9.5/bin/$LD_LIBRARY_PATH

. ~/research/automatenv/bin/activate

python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/2024/updated_params/Jij_0.01/ --filename Jij_0.01 -n 100 -p "Jij={'0-0':0.01, '0-1':1,'1-0':0.01,'1-1':1}"
python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/2024/updated_params/Jij_0.02/ --filename Jij_0.02 -n 100 -p "Jij={'0-0':0.02, '0-1':1,'1-0':0.02,'1-1':1}"
python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/2024/updated_params/Jij_0.03/ --filename Jij_0.03 -n 100 -p "Jij={'0-0':0.03, '0-1':1,'1-0':0.03,'1-1':1}"
python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/2024/updated_params/Jij_0.04/ --filename Jij_0.04 -n 100 -p "Jij={'0-0':0.04, '0-1':1,'1-0':0.04,'1-1':1}"
python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/2024/updated_params/Jij_0.05/ --filename Jij_0.05 -n 100 -p "Jij={'0-0':0.05, '0-1':1,'1-0':0.05,'1-1':1}"

# deactivate