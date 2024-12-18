#!/bin/bash

#how to run
#qsub ~/research/AutomatAnts/code/run_model.sh 
cd

export PATH=/home/soft/python-3.9.5/bin:$PATH
export LD_LIBRARY_PATH=/home/soft/python-3.9.5/bin/$LD_LIBRARY_PATH

. ~/research/automatenv/bin/activate
for v in $(seq 0.1 0.1 1)
do 
    # calculate different amounts of pheromone for food and any other node
    v1=${v/,/.}
    v2=`echo "scale=2;$v1*2" | bc | sed 's/^\./0./'`
    v3=`echo "scale=2;$v1*2.5" | bc | sed 's/^\./0./'` 
    python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/pheromone/ --filename pheromone=$v1,$v1 -n 100 -q $v1,$v1 -m pheromone -f det
    python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/pheromone/ --filename pheromone=$v1,$v2 -n 100 -q $v1,$v2 -m pheromone -f det
    python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/pheromone/ --filename pheromone=$v1,$v3 -n 100 -q $v1,$v3 -m pheromone -f det
done
deactivate