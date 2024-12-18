#!/bin/bash

#how to run
#qsub ~/research/AutomatAnts/code/run_model.sh 

cd

export PATH=/home/soft/python-3.9.5/bin:$PATH
export LD_LIBRARY_PATH=/home/soft/python-3.9.5/bin/$LD_LIBRARY_PATH

. ~/research/automatenv/bin/activate

# python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/2024/scenarios/J_0/ --filename J_0 -n 100 -p "Jij={'0-0':0, '0-1':0,'1-0':0,'1-1':0}"
# python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/2024/scenarios/J_0.01/ --filename J_0.01 -n 100 -p "Jij={'0-0':0.01, '0-1':0.01,'1-0':0.01,'1-1':0.01}"
# python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/2024/scenarios/J11_0/ --filename J11_0 -n 100 -p "Jij={'0-0':0.01, '0-1':0,'1-0':0.01,'1-1':0}"
# python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/2024/scenarios/J00_1/ --filename J00_1 -n 100 -p "Jij={'0-0':1, '0-1':1,'1-0':1,'1-1':1}"

python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/2024/scenarios/g0.25_J_0/ --filename J_0 -n 100 -p "Jij={'0-0':0, '0-1':0,'1-0':0,'1-1':0};g=100,U,0.25,0.25"
python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/2024/scenarios/g0.25_J_0.01/ --filename J_0.01 -n 100 -p "Jij={'0-0':0.01, '0-1':0.01,'1-0':0.01,'1-1':0.01};g=100,U,0.25,0.25"
python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/2024/scenarios/g0.25_J11_0/ --filename J11_0 -n 100 -p "Jij={'0-0':0.01, '0-1':0,'1-0':0.01,'1-1':0};g=100,U,0.25,0.25"
python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/2024/scenarios/g0.25_J00_1/ --filename J00_1 -n 100 -p "Jij={'0-0':1, '0-1':1,'1-0':1,'1-1':1};g=100,U,0.25,0.25"

python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/2024/scenarios/g0.5_J_0/ --filename g0.5_J_0 -n 100 -p "Jij={'0-0':0, '0-1':0,'1-0':0,'1-1':0};g=100,U,0.5,0.5"
python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/2024/scenarios/g0.5_J_0.01/ --filename g0.5_J_0.01 -n 100 -p "Jij={'0-0':0.01, '0-1':0.01,'1-0':0.01,'1-1':0.01};g=100,U,0.5,0.5"
python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/2024/scenarios/g0.5_J11_0/ --filename g0.5_J11_0 -n 100 -p "Jij={'0-0':0.01, '0-1':0,'1-0':0.01,'1-1':0};g=100,U,0.5,0.5"
python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/2024/scenarios/g0.5_J00_1/ --filename g0.5_J00_1 -n 100 -p "Jij={'0-0':1, '0-1':1,'1-0':1,'1-1':1};g=100,U,0.5,0.5"

python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/2024/scenarios/g0.75_J_0/ --filename g0.75_J_0 -n 100 -p "Jij={'0-0':0, '0-1':0,'1-0':0,'1-1':0};g=100,U,0.75,0.75"
python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/2024/scenarios/g0.75_J_0.01/ --filename g0.75_J_0.01 -n 100 -p "Jij={'0-0':0.01, '0-1':0.01,'1-0':0.01,'1-1':0.01};g=100,U,0.75,0.75"
python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/2024/scenarios/g0.75_J11_0/ --filename g0.75_J11_0 -n 100 -p "Jij={'0-0':0.01, '0-1':0,'1-0':0.01,'1-1':0};g=100,U,0.75,0.75"
python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/2024/scenarios/g0.75_J00_1/ --filename g0.75_J00_1 -n 100 -p "Jij={'0-0':1, '0-1':1,'1-0':1,'1-1':1};g=100,U,0.75,0.75"
# deactivate