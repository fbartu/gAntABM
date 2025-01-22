#!/bin/bash

#how to run
#qsub ~/research/AutomatAnts/code/run_model.sh 

cd

export PATH=/home/soft/python-3.9.5/bin:$PATH
export LD_LIBRARY_PATH=/home/soft/python-3.9.5/bin/$LD_LIBRARY_PATH

. ~/research/automatenv/bin/activate
for rho in $(seq 0.001 0.1 1.001)
do
    for epsilon in $(seq 0.001 0.1 1.001)
    do
        # python3 ~/research/AutomatAnts/code/Heterogeneity/run_cluster.py --directory ~/research/AutomatAnts/results/2024/hetero_model/rho_epsilon/ --filename rho_${rho/,/.}_epsilon_${epsilon/,/.} --social_feedbacks both -n 100 -p "rho=${rho/,/.};epsilon=${epsilon/,/.}"
        python3 ~/research/AutomatAnts/VERSIONS/vHeterogenous_Movement/run_cluster.py --directory ~/research/AutomatAnts/results/2025/rho_epsilon_with_tags/ --filename rho_${rho/,/.}_epsilon_${epsilon/,/.} --social_feedbacks both -n 100 -p "rho=${rho/,/.};epsilon=${epsilon/,/.}"

    done
done