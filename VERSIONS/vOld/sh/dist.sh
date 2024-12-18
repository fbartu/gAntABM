#!/bin/bash

#how to run
#qsub ~/research/AutomatAnts/code/run_model.sh 
#qsub -pe make 20 -l h_vmem=8G ~/research/AutomatAnts/code/run_model.sh

cd

export PATH=/home/soft/python-3.9.5/bin:$PATH
export LD_LIBRARY_PATH=/home/soft/python-3.9.5/bin/$LD_LIBRARY_PATH

. ~/research/automatenv/bin/activate
python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/food_conditions/dist/ --food dist,3 --filename "dist=3" -n 100
python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/food_conditions/dist/ --food dist,8 --filename "dist=8" -n 100
python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/food_conditions/dist/ --food dist,13 --filename "dist=13" -n 100
python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/food_conditions/dist/ --food dist,18 --filename "dist=18" -n 100
python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/food_conditions/dist/ --food dist,23 --filename "dist=23" -n 100

deactivate

