#!/bin/bash

#how to run
#qsub ~/research/AutomatAnts/code/run_cluster.sh 

cd

export PATH=/home/soft/python-3.9.5/bin:$PATH
export LD_LIBRARY_PATH=/home/soft/python-3.9.5/bin/$LD_LIBRARY_PATH

. ~/research/automatenv/bin/activate

# NO FOOD
python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/rec_noRec_nf/nf/uniform/ --food nf --filename "uniform" -n 100 -r False > chk_nf_uniform.txt

deactivate