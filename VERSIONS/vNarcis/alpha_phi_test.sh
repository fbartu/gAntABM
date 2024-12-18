#!/bin/bash

# root directory
cd

. ~/research/automatenv/bin/activate
#python3 ~/research/AutomatAnts/code/run_model.py -x alpha_eta_0 -p eta=0,alpha=0 --nruns 20,True
#python3 ~/research/AutomatAnts/code/run_model.py -x alpha_eta_0_phi0.1 -p eta=0,alpha=0,phi=0.1 --nruns 20,True
#python3 ~/research/AutomatAnts/code/run_model.py -x alpha_eta_0_phi0.9 -p eta=0,alpha=0,phi=0.9 --nruns 20,True
python3 ~/research/AutomatAnts/code/run_model.py -x alpha_eta_0_phi1 -p eta=0,alpha=0,phi=1 --nruns 5,True
deactivate

#how to run
#qsub ~/research/AutomatAnts/code/run_model.sh 
#qsub -pe make 20 -l h_vmem=8G ~/research/AutomatAnts/code/run_model.sh