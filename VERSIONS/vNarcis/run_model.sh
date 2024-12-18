#!/bin/bash

export PATH=/home/soft/python-3.9.5/bin:$PATH
export LD_LIBRARY_PATH=/home/soft/python-3.9.5/bin/$LD_LIBRARY_PATH

. ~/research/automatenv/bin/activate
#python3 ~/research/AutomatAnts/code/run_model_time.py
python3 ~/research/AutomatAnts/code/run_model.py -x Control_Noise -r GR --nruns 20,True
deactivate

#how to run
#qsub ~/research/AutomatAnts/run_model.sh 
#qsub -pe make 1 -l h_vmem=8G ~/research/AutomatAnts/run_model.sh
