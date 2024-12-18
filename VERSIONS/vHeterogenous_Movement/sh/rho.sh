#!/bin/bash

#how to run
#qsub ~/research/AutomatAnts/code/run_model.sh 

cd

export PATH=/home/soft/python-3.9.5/bin:$PATH
export LD_LIBRARY_PATH=/home/soft/python-3.9.5/bin/$LD_LIBRARY_PATH

. ~/research/automatenv/bin/activate
# python3 ~/research/AutomatAnts/code/Heterogeneity/run_cluster.py --directory ~/research/AutomatAnts/results/2024/rho/wRec/rho_0.1/ --filename rho_0.1_wrec -n 100 -m exp -p rho=0.1 -r True
# python3 ~/research/AutomatAnts/code/Heterogeneity/run_cluster.py --directory ~/research/AutomatAnts/results/2024/rho/wRec/rho_0.5/ --filename rho_0.5_wrec -n 100 -m exp -p rho=0.5 -r True
# python3 ~/research/AutomatAnts/code/Heterogeneity/run_cluster.py --directory ~/research/AutomatAnts/results/2024/rho/wRec/rho_0.9/ --filename rho_0.9_wrec -n 100 -m exp -p rho=0.9 -r True

python3 ~/research/AutomatAnts/code/Heterogeneity/run_cluster.py --directory ~/research/AutomatAnts/results/2024/rho/woutRec/rho_0.1/ --filename rho_0.1_woutrec -n 100 -m exp -p rho=0.1 -r False
python3 ~/research/AutomatAnts/code/Heterogeneity/run_cluster.py --directory ~/research/AutomatAnts/results/2024/rho/woutRec/rho_0.5/ --filename rho_0.5_woutrec -n 100 -m exp -p rho=0.5 -r False
python3 ~/research/AutomatAnts/code/Heterogeneity/run_cluster.py --directory ~/research/AutomatAnts/results/2024/rho/woutRec/rho_0.9/ --filename rho_0.9_woutrec -n 100 -m exp -p rho=0.9 -r False
