#!/bin/bash

#how to run
#qsub ~/research/AutomatAnts/code/run_cluster.sh 

cd

export PATH=/home/soft/python-3.9.5/bin:$PATH
export LD_LIBRARY_PATH=/home/soft/python-3.9.5/bin/$LD_LIBRARY_PATH

. ~/research/automatenv/bin/activate

### HOMOGENEOUS Jij
# Jij = 0
# python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/with_recruitment/parameters/homogeneous_Jij/Jij_0/uniform/ --food det --filename "Jij0_uniform" -n 100 -p Jij="{'0-0':0,'0-1':0,'1-0':0,'1-1':0}"

# Jij = 0.4
# python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/with_recruitment/parameters/homogeneous_Jij/Jij_0.4/uniform/ --food det --filename "Jij0.4_uniform" -n 100 -p Jij="{'0-0':0.4,'0-1':0.4,'1-0':0.4,'1-1':0.4}"

# python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/with_recruitment/parameters/homogeneous_Jij/Jij_0.4/gaussian/ --food det --filename "Jij0.4_gaussian" -n 100 -g 100,B,2,2 -p Jij="{'0-0':0.4,'0-1':0.4,'1-0':0.4,'1-1':0.4}"
# python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/with_recruitment/parameters/homogeneous_Jij/Jij_0.4/bimodal_50/ --food det --filename "Jij0.4_bimodal_50" -n 100 -g 50,B,2,6:50,B,6,2 -p Jij="{'0-0':0.4,'0-1':0.4,'1-0':0.4,'1-1':0.4}"
# python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/with_recruitment/parameters/homogeneous_Jij/Jij_0.4/bimodal_90/ --food det --filename "Jij0,4_bimodal_90" -n 100 -g 90,B,2,6:10,B,6,2 -p Jij="{'0-0':0.4,'0-1':0.4,'1-0':0.4,'1-1':0.4}"
# python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/with_recruitment/parameters/homogeneous_Jij/Jij_0.4/bimodal_10/ --food det --filename "Jij0.4_bimodal_10" -n 100 -g 10,B,2,6:90,B,6,2 -p Jij="{'0-0':0.4,'0-1':0.4,'1-0':0.4,'1-1':0.4}"

# Jij = 1
# python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/with_recruitment/parameters/homogeneous_Jij/Jij_1/uniform/ --food det --filename "Jij1_uniform" -n 100 -p Jij="{'0-0':1,'0-1':1,'1-0':1,'1-1':1}"

# python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/with_recruitment/parameters/homogeneous_Jij/Jij_1/gaussian/ --food det --filename "Jij1_gaussian" -n 100 -g 100,B,2,2 -p Jij="{'0-0':1,'0-1':1,'1-0':1,'1-1':1}"
# python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/with_recruitment/parameters/homogeneous_Jij/Jij_1/bimodal_50/ --food det --filename "Jij1_bimodal_50" -n 100 -g 50,B,2,6:50,B,6,2 -p Jij="{'0-0':1,'0-1':1,'1-0':1,'1-1':1}"
# python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/with_recruitment/parameters/homogeneous_Jij/Jij_1/bimodal_90/ --food det --filename "Jij1_bimodal_90" -n 100 -g 90,B,2,6:10,B,6,2 -p Jij="{'0-0':1,'0-1':1,'1-0':1,'1-1':1}"
# python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/with_recruitment/parameters/homogeneous_Jij/Jij_1/bimodal_10/ --food det --filename "Jij1_bimodal_10" -n 100 -g 10,B,2,6:90,B,6,2 -p Jij="{'0-0':1,'0-1':1,'1-0':1,'1-1':1}"

# Jij = 1.5
# python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/with_recruitment/parameters/homogeneous_Jij/Jij_1.5/uniform/ --food det --filename "Jij1.5_uniform" -n 100 -p Jij="{'0-0':1.5,'0-1':1.5,'1-0':1.5,'1-1':1.5}"

# python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/with_recruitment/parameters/homogeneous_Jij/Jij_1.5/gaussian/ --food det --filename "Jij1.5_gaussian" -n 100 -g 100,B,2,2 -p Jij="{'0-0':1.5,'0-1':1.5,'1-0':1.5,'1-1':1.5}"
# python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/with_recruitment/parameters/homogeneous_Jij/Jij_1.5/bimodal_50/ --food det --filename "Jij1.5_bimodal_50" -n 100 -g 50,B,2,6:50,B,6,2 -p Jij="{'0-0':1.5,'0-1':1.5,'1-0':1.5,'1-1':1.5}"
# python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/with_recruitment/parameters/homogeneous_Jij/Jij_1.5/bimodal_90/ --food det --filename "Jij1.5_bimodal_90" -n 100 -g 90,B,2,6:10,B,6,2 -p Jij="{'0-0':1.5,'0-1':1.5,'1-0':1.5,'1-1':1.5}"
# python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/with_recruitment/parameters/homogeneous_Jij/Jij_1.5/bimodal_10/ --food det --filename "Jij1.5_bimodal_10" -n 100 -g 10,B,2,6:90,B,6,2 -p Jij="{'0-0':1.5,'0-1':1.5,'1-0':1.5,'1-1':1.5}"


### HETEROGENEOUS Jij

# Jij = 0 + 1.5
# python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/with_recruitment/parameters/heterogeneous_Jij/Jij_0_1.5/uniform/ --food det --filename "Jij0_1.5_uniform" -n 100 -p Jij="{'0-0':0,'0-1':1.5,'1-0':0,'1-1':1.5}"
# Jij = 0.4 + 1
# python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/with_recruitment/parameters/heterogeneous_Jij/Jij_0.4_1/uniform/ --food det --filename "Jij0.4_1_uniform" -n 100 -p Jij="{'0-0':0.4,'0-1':1,'1-0':0.4,'1-1':1}"
# Jij = 0.4 + 1.5
# python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/with_recruitment/parameters/heterogeneous_Jij/Jij_0.4_1.5/uniform/ --food det --filename "Jij0.4_1.5_uniform" -n 100 -p Jij="{'0-0':0.4,'0-1':1.5,'1-0':0.4,'1-1':1.5}"
# Jij = 0.4 + 3
python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/with_recruitment/parameters/heterogeneous_Jij/Jij_0.4_3/uniform/ --food det --filename "Jij0.4_3_uniform" -n 100 -p Jij="{'0-0':0.4,'0-1':3,'1-0':0.4,'1-1':3}"
# Jij = 0.4 + 5
python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/with_recruitment/parameters/heterogeneous_Jij/Jij_0.4_5/uniform/ --food det --filename "Jij0.4_5_uniform" -n 100 -p Jij="{'0-0':0.4,'0-1':5,'1-0':0.4,'1-1':5}"

deactivate