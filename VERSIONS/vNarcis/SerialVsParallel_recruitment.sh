#!/bin/bash

# root directory
cd

export PATH=/home/soft/python-3.9.5/bin:$PATH
export LD_LIBRARY_PATH=/home/soft/python-3.9.5/bin/$LD_LIBRARY_PATH

. ~/research/automatenv/bin/activate
# normal model
python3 ~/research/AutomatAnts/code/run_model.py -x control
# scanning parameter mu (noise in recruitment)
python3 ~/research/AutomatAnts/code/run_model.py -p mu=0.01 -x mu0.01
python3 ~/research/AutomatAnts/code/run_model.py -p mu=0.05 -x mu0.05
python3 ~/research/AutomatAnts/code/run_model.py -p mu=0.10 -x mu0.10
python3 ~/research/AutomatAnts/code/run_model.py -p mu=0.15 -x mu0.15
python3 ~/research/AutomatAnts/code/run_model.py -p mu=0.20 -x mu0.20
python3 ~/research/AutomatAnts/code/run_model.py -p mu=0.25 -x mu0.25
python3 ~/research/AutomatAnts/code/run_model.py -p mu=0.30 -x mu0.30
python3 ~/research/AutomatAnts/code/run_model.py -p mu=0.35 -x mu0.35
python3 ~/research/AutomatAnts/code/run_model.py -p mu=0.40 -x mu0.40
python3 ~/research/AutomatAnts/code/run_model.py -p mu=0.50 -x mu0.50
python3 ~/research/AutomatAnts/code/run_model.py -p mu=0.75 -x mu0.75
python3 ~/research/AutomatAnts/code/run_model.py -p mu=1.00 -x mu1.00
python3 ~/research/AutomatAnts/code/run_model.py -p mu=2.00 -x mu2.00
python3 ~/research/AutomatAnts/code/run_model.py -p mu=3.00 -x mu3.00
# serial recruitment
python3 ~/research/AutomatAnts/code/run_model.py -r HR,s -x serial_recruitment
deactivate

#how to run
#qsub ~/research/AutomatAnts/code/run_model.sh 
#qsub -pe make 20 -l h_vmem=8G ~/research/AutomatAnts/code/run_model.sh