#!/bin/bash

#how to run
#qsub ~/research/AutomatAnts/code/run_model.sh 

cd

export PATH=/home/soft/python-3.9.5/bin:$PATH
export LD_LIBRARY_PATH=/home/soft/python-3.9.5/bin/$LD_LIBRARY_PATH

. ~/research/automatenv/bin/activate
beta=0.5
python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/2024/updated_params/beta_0.5/ --filename beta=${beta/,/.} -n 100 -p beta=${beta/,/.}
# beta=0.7
# python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/2024/updated_params/beta_0.7/ --filename beta=${beta/,/.} -n 100 -p beta=${beta/,/.}
# beta=0.8
# python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/2024/updated_params/beta_0.8/ --filename beta=${beta/,/.} -n 100 -p beta=${beta/,/.}
# beta=0.9
# python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/2024/updated_params/beta_0.9/ --filename beta=${beta/,/.} -n 100 -p beta=${beta/,/.}

# deactivate