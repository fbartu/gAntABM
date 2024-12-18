#!/bin/bash

#how to run
#qsub ~/research/AutomatAnts/code/run_model.sh 

cd

export PATH=/home/soft/python-3.9.5/bin:$PATH
export LD_LIBRARY_PATH=/home/soft/python-3.9.5/bin/$LD_LIBRARY_PATH

. ~/research/automatenv/bin/activate
python3 ~/research/AutomatAnts/code/Heterogeneity/run_cluster.py --directory ~/research/AutomatAnts/results/2024/hetero_model/s1/ --filename rho_0.5 -n 100 -p "rho=0.5;epsilon=1"
python3 ~/research/AutomatAnts/code/Heterogeneity/run_cluster.py --directory ~/research/AutomatAnts/results/2024/hetero_model/s1/ --filename rho_1.0 -n 100 -p "rho=1;epsilon=1"
python3 ~/research/AutomatAnts/code/Heterogeneity/run_cluster.py --directory ~/research/AutomatAnts/results/2024/hetero_model/s1/ --filename rho_0.0 -n 100 -p "rho=0;epsilon=1"
python3 ~/research/AutomatAnts/code/Heterogeneity/run_cluster.py --directory ~/research/AutomatAnts/results/2024/hetero_model/s1/ --filename rho_0.9 -n 100 -p "rho=0.9;epsilon=1"
python3 ~/research/AutomatAnts/code/Heterogeneity/run_cluster.py --directory ~/research/AutomatAnts/results/2024/hetero_model/s1/ --filename rho_0.1 -n 100 -p "rho=0.1;epsilon=1"

