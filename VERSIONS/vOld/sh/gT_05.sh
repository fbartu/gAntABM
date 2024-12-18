#!/bin/bash

#how to run
#qsub ~/research/AutomatAnts/code/run_cluster.sh 

cd

export PATH=/home/soft/python-3.9.5/bin:$PATH
export LD_LIBRARY_PATH=/home/soft/python-3.9.5/bin/$LD_LIBRARY_PATH

. ~/research/automatenv/bin/activate

## Theta = 10**-5
python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/with_recruitment/parameters/gains_thetas/theta_05/ --food det --filename theta05_g01 -n 100 -p Theta="10**-5" -g 100,U,0.1,0.1
python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/with_recruitment/parameters/gains_thetas/theta_05/ --food det --filename theta05_g02 -n 100 -p Theta="10**-5" -g 100,U,0.2,0.2
python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/with_recruitment/parameters/gains_thetas/theta_05/ --food det --filename theta05_g03 -n 100 -p Theta="10**-5" -g 100,U,0.3,0.3
python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/with_recruitment/parameters/gains_thetas/theta_05/ --food det --filename theta05_g04 -n 100 -p Theta="10**-5" -g 100,U,0.4,0.4
python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/with_recruitment/parameters/gains_thetas/theta_05/ --food det --filename theta05_g05 -n 100 -p Theta="10**-5" -g 100,U,0.5,0.5
python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/with_recruitment/parameters/gains_thetas/theta_05/ --food det --filename theta05_g06 -n 100 -p Theta="10**-5" -g 100,U,0.6,0.6
python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/with_recruitment/parameters/gains_thetas/theta_05/ --food det --filename theta05_g07 -n 100 -p Theta="10**-5" -g 100,U,0.7,0.7
python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/with_recruitment/parameters/gains_thetas/theta_05/ --food det --filename theta05_g08 -n 100 -p Theta="10**-5" -g 100,U,0.8,0.8
python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/with_recruitment/parameters/gains_thetas/theta_05/ --food det --filename theta05_g09 -n 100 -p Theta="10**-5" -g 100,U,0.9,0.9


deactivate