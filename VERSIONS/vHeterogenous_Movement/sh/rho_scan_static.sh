#!/bin/bash

#how to run
#qsub ~/research/AutomatAnts/code/run_model.sh 

cd

export PATH=/home/soft/python-3.9.5/bin:$PATH
export LD_LIBRARY_PATH=/home/soft/python-3.9.5/bin/$LD_LIBRARY_PATH

. ~/research/automatenv/bin/activate
for rho in $(seq 0.001 0.05 1.001)
do
    # python3 ~/research/AutomatAnts/code/Heterogeneity/run_cluster.py --directory ~/research/AutomatAnts/results/2024/hetero_model/rho/DET/static/ --filename rho_${rho/,/.} -n 100 -p rho=${rho/,/.}
    # python3 ~/research/AutomatAnts/code/Heterogeneity/run_cluster.py --directory ~/research/AutomatAnts/results/2024/hetero_model/rho/NFD/static/ --filename rho_${rho/,/.} -n 100 -p rho=${rho/,/.}
    python3 ~/research/AutomatAnts/code/Heterogeneity/run_cluster.py --directory ~/research/AutomatAnts/results/2024/hetero_model/rho/prob_rec/ --filename rho_${rho/,/.} -n 100 -p rho=${rho/,/.}

done