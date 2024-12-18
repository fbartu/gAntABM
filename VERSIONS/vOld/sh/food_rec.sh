#!/bin/bash

#how to run
#qsub -pe make 20 -l h_vmem=8G ~/research/AutomatAnts/code/sh/food_rec.sh

cd

export PATH=/home/soft/python-3.9.5/bin:$PATH
export LD_LIBRARY_PATH=/home/soft/python-3.9.5/bin/$LD_LIBRARY_PATH

. ~/research/automatenv/bin/activate
python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/with_recruitment/food_conditions/det/ --food det --filename det -n 100
python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/with_recruitment/food_conditions/sto/ --food sto_1 --filename sto -n 100
python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/with_recruitment/food_conditions/sto_clustered/ --food sto_2 --filename sto_clustered -n 100
python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/with_recruitment/food_conditions/nf/ --food nf --filename nf -n 100

deactivate

