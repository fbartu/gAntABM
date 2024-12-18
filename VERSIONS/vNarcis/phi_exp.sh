#!/bin/bash
cd
# . ~/research/automatenv/bin/activate
# python3 ~/research/AutomatAnts/code/run_model.py -x exp_alphaeta0 -p alpha=0,eta=0 --nruns 1,False
# deactivate

. ~/research/automatenv/bin/activate
python3 ~/research/AutomatAnts/code/run_model.py -x exp_phi0.1 -p phi=0.1 --nruns 1,False
deactivate

# . ~/research/automatenv/bin/activate
# python3 ~/research/AutomatAnts/code/run_model.py -x exp_phi0.9 -p phi=0.9 --nruns 1,False
# deactivate