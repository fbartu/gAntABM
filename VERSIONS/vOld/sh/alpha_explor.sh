#!/bin/bash

#how to run
#qsub ~/research/AutomatAnts/code/run_model.sh 

cd

export PATH=/home/soft/python-3.9.5/bin:$PATH
export LD_LIBRARY_PATH=/home/soft/python-3.9.5/bin/$LD_LIBRARY_PATH

. ~/research/automatenv/bin/activate

alpha=0.003
beta=1
python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/2024/updated_params/beta_alpha/alpha_3/ --filename alpha_3 -n 100 -p "beta=${beta/,/.};alpha=${alpha/,/.}"
alpha=0.004
python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/2024/updated_params/beta_alpha/alpha_4/ --filename alpha_4 -n 100 -p "beta=${beta/,/.};alpha=${alpha/,/.}"
alpha=0.005
python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/2024/updated_params/beta_alpha/alpha_5/ --filename alpha_5 -n 100 -p "beta=${beta/,/.};alpha=${alpha/,/.}"
# deactivate