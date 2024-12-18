#!/bin/bash

# root directory
cd

export PATH=/home/soft/python-3.9.5/bin:$PATH
export LD_LIBRARY_PATH=/home/soft/python-3.9.5/bin/$LD_LIBRARY_PATH

. ~/research/automatenv/bin/activate
python3 ~/research/AutomatAnts/code/Run.py --directory /home/usuaris/pol.fernandez/research/AutomatAnts/results/food_conditions/det/ --food det --filename det
#python3 ~/research/AutomatAnts/code/Run.py --directory /home/usuaris/pol.fernandez/research/AutomatAnts/results/food_conditions/sto/ --food sto_1 --filename sto
#python3 ~/research/AutomatAnts/code/Run.py --directory /home/usuaris/pol.fernandez/research/AutomatAnts/results/food_conditions/sto_clustered/ --food sto_2 --filename sto_clustered 
#python3 ~/research/AutomatAnts/code/Run.py --directory /home/usuaris/pol.fernandez/research/AutomatAnts/results/food_conditions/nf/ --food nf --filename nf

deactivate

#how to run
#qsub ~/research/AutomatAnts/code/run_model.sh 
#qsub -pe make 20 -l h_vmem=8G ~/research/AutomatAnts/code/run_model.sh
