#!/bin/bash

#how to run
#qsub ~/research/AutomatAnts/code/run_model.sh 

cd

export PATH=/home/soft/python-3.9.5/bin:$PATH
export LD_LIBRARY_PATH=/home/soft/python-3.9.5/bin:$LD_LIBRARY_PATH

. ~/research/automatenv/bin/activate

for rho in $(seq 0.001 0.1 1.001)
do
    float_rho=$(echo $rho | tr ',' '.')
    for N in 5 10 20 30 40 50
    # for N in 5 10 20 30 40 50 75 100 150 200 400 620
    do
        # python3 ~/research/AutomatAnts/VERSIONS/vFixed_Density/run_cluster.py --directory ~/research/AutomatAnts/results/2025/agent_density/random_position/ --filename "rho_${rho}_N_${N}" -n 100 -p "rho=${rho/,/.};N=${N};init_position=random;tmax=2000"
        python3 ~/research/AutomatAnts/VERSIONS/vFixed_Density/run_until.py --directory ~/research/AutomatAnts/results/2025/agent_density/random_position/ --filename "rho_${rho}_N_${N}" -n 100 -p "rho=${rho/,/.};N=${N};init_position=random"

    done
done
# rho=0
# for N in 2 5 10 20 30 40 50 75 100 150 200 400 600 1000
# do
#     python3 ~/research/AutomatAnts/VERSIONS/vFixed_Density/run_cluster.py --directory ~/research/AutomatAnts/results/2025/agent_density/random_position/ --filename "rho_${rho}_N_${N}" -n 100 -p "rho=${rho};N=${N};init_position=random"
# done