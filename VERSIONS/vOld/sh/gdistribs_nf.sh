#!/bin/bash

#how to run
#qsub ~/research/AutomatAnts/code/run_cluster.sh 

cd

export PATH=/home/soft/python-3.9.5/bin:$PATH
export LD_LIBRARY_PATH=/home/soft/python-3.9.5/bin/$LD_LIBRARY_PATH

. ~/research/automatenv/bin/activate
python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/without_food/parameters/uniform/ --food nf --filename "nf_uniform" -n 100
python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/without_food/parameters/bimodal/ --food nf --filename "nf_bimodal" -n 100 -g 100,B,0.5,0.5
python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/without_food/parameters/gaussian/ --food nf --filename "nf_gaussian" -n 100 -g 100,B,2,2
python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/without_food/parameters/bimodal_50/ --food nf --filename "nf_bimodal_50" -n 100 -g 50,B,2,6:50,B,6,2
python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/without_food/parameters/bimodal_90/ --food nf --filename "nf_bimodal_90" -n 100 -g 90,B,2,6:10,B,6,2
python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/without_food/parameters/bimodal_10/ --food nf --filename "nf_bimodal_10" -n 100 -g 10,B,2,6:90,B,6,2

deactivate