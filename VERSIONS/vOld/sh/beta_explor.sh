#!/bin/bash

#how to run
#qsub ~/research/AutomatAnts/code/run_model.sh 

cd

export PATH=/home/soft/python-3.9.5/bin:$PATH
export LD_LIBRARY_PATH=/home/soft/python-3.9.5/bin/$LD_LIBRARY_PATH

. ~/research/automatenv/bin/activate

beta=0.5
python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/2024/updated_params/beta_exploration/beta_0.5/ --filename beta_0.5 -n 100 -p "beta=${beta/,/.};Jij={'0-0':0.01, '0-1':1,'1-0':0.01,'1-1':1}"
beta=0.7
python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/2024/updated_params/beta_exploration/beta_0.7/ --filename beta_0.7 -n 100 -p "beta=${beta/,/.};Jij={'0-0':0.01, '0-1':1,'1-0':0.01,'1-1':1}"
beta=0.8
python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/2024/updated_params/beta_exploration/beta_0.8/ --filename beta_0.8 -n 100 -p "beta=${beta/,/.};Jij={'0-0':0.01, '0-1':1,'1-0':0.01,'1-1':1}"
beta=0.9
python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/2024/updated_params/beta_exploration/beta_0.9/ --filename beta_0.9 -n 100 -p "beta=${beta/,/.};Jij={'0-0':0.01, '0-1':1,'1-0':0.01,'1-1':1}"
# deactivate