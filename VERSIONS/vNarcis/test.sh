#!/bin/bash

# root directory
cd

. ~/research/automatenv/bin/activate
python3 ~/research/AutomatAnts/code/run_model.py -x minidebug -p alpha=0,eta=0 --nruns 1,False
# G:
# G:\research\automatenv\Scripts\activate
# cd G:\research\AutomatAnts\code\
# python G:\research\AutomatAnts\code\run_model.py -x phi0.9_ --nruns 20,True -p phi=0.9
#python3 ~/research/AutomatAnts/code/run_model.py -x parallel_testing --nruns 5,True
#python3 ~/research/AutomatAnts/code/run_model.py -x serial_testing --nruns 5,False
deactivate

#how to run
#qsub ~/research/AutomatAnts/code/run_model.sh 
#qsub -pe make 20 -l h_vmem=8G ~/research/AutomatAnts/code/run_model.sh