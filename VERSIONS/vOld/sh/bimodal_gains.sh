#!/bin/bash

#how to run
#qsub ~/research/AutomatAnts/code/run_cluster.sh 

cd

export PATH=/home/soft/python-3.9.5/bin:$PATH
export LD_LIBRARY_PATH=/home/soft/python-3.9.5/bin/$LD_LIBRARY_PATH

. ~/research/automatenv/bin/activate
python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/with_recruitment/parameters/uniform/ --food det --filename "uniform" -n 100
python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/with_recruitment/parameters/bimodal/ --food det --filename "bimodal" -n 100 -g 100,B,0.5,0.5
python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/with_recruitment/parameters/gaussian/ --food det --filename "gaussian" -n 100 -g 100,B,2,2
python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/with_recruitment/parameters/bimodal_50/ --food det --filename "bimodal_50" -n 100 -g 50,B,2,6:50,B,6,2
python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/with_recruitment/parameters/bimodal_90/ --food det --filename "bimodal_90" -n 100 -g 90,B,2,6:10,B,6,2
python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/with_recruitment/parameters/bimodal_10/ --food det --filename "bimodal_10" -n 100 -g 10,B,2,6:90,B,6,2

deactivate