#!/bin/bash

# root directory
cd

export PATH=/home/soft/python-3.9.5/bin:$PATH
export LD_LIBRARY_PATH=/home/soft/python-3.9.5/bin/$LD_LIBRARY_PATH

. ~/research/automatenv/bin/activate
# normal model
python3 ~/research/AutomatAnts/code/run_model.py -x control_phi
# scanning parameter phi (noise in recruitment)
python3 ~/research/AutomatAnts/code/run_model.py -p phi=0.45 -x phi0.45
python3 ~/research/AutomatAnts/code/run_model.py -p phi=0.55 -x phi0.55
python3 ~/research/AutomatAnts/code/run_model.py -p phi=0.60 -x phi0.60
python3 ~/research/AutomatAnts/code/run_model.py -p phi=0.65 -x phi0.65
python3 ~/research/AutomatAnts/code/run_model.py -p phi=0.70 -x phi0.70
python3 ~/research/AutomatAnts/code/run_model.py -p phi=0.80 -x phi0.80
python3 ~/research/AutomatAnts/code/run_model.py -p phi=0.85 -x phi0.85
python3 ~/research/AutomatAnts/code/run_model.py -p phi=0.90 -x phi0.90
python3 ~/research/AutomatAnts/code/run_model.py -p phi=0.95 -x phi0.95
# serial recruitment
python3 ~/research/AutomatAnts/code/run_model.py -r HR,s -x serial_recruitment
deactivate

#how to run
#qsub ~/research/AutomatAnts/code/run_model.sh 
#qsub -pe make 20 -l h_vmem=8G ~/research/AutomatAnts/code/run_model.sh