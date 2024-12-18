#!/bin/bash

#how to run
#qsub ~/research/AutomatAnts/code/run_model.sh 

cd

export PATH=/home/soft/python-3.9.5/bin:$PATH
export LD_LIBRARY_PATH=/home/soft/python-3.9.5/bin/$LD_LIBRARY_PATH

. ~/research/automatenv/bin/activate
# python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/2024/updated_params/ballistic_1/ --filename ballistic_1 -n 100 -p "Jij={'0-0':0.01, '0-1':1,'1-0':0.01,'1-1':1}"
python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/2024/updated_params/ballistic_2/ --filename ballistic_2 -n 100 -p "Jij={'0-0':0.01, '0-1':1,'1-0':0.01,'1-1':1}"

# deactivate