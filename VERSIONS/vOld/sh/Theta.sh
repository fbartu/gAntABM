#!/bin/bash

#how to run
#qsub ~/research/AutomatAnts/code/run_cluster.sh 

cd

export PATH=/home/soft/python-3.9.5/bin:$PATH
export LD_LIBRARY_PATH=/home/soft/python-3.9.5/bin/$LD_LIBRARY_PATH

. ~/research/automatenv/bin/activate

python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/with_recruitment/parameters/theta/theta_01/ --food det --filename theta01 -n 100 -p Theta="10**-1"
python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/with_recruitment/parameters/theta/theta_02/ --food det --filename theta02 -n 100 -p Theta="10**-2"
python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/with_recruitment/parameters/theta/theta_03/ --food det --filename theta03 -n 100 -p Theta="10**-3"
python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/with_recruitment/parameters/theta/theta_04/ --food det --filename theta04 -n 100 -p Theta="10**-4"
python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/with_recruitment/parameters/theta/theta_06/ --food det --filename theta06 -n 100 -p Theta="10**-6"
python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/with_recruitment/parameters/theta/theta_07/ --food det --filename theta07 -n 100 -p Theta="10**-7"
python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/with_recruitment/parameters/theta/theta_09/ --food det --filename theta09 -n 100 -p Theta="10**-9"
python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/with_recruitment/parameters/theta/theta_11/ --food det --filename theta11 -n 100 -p Theta="10**-11"
python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/with_recruitment/parameters/theta/theta_12/ --food det --filename theta12 -n 100 -p Theta="10**-12"


# python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/with_recruitment/parameters/theta/theta_05/ --food det --filename theta05 -n 100 -p Theta="10**-5"
# python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/with_recruitment/parameters/theta/theta_08/ --food det --filename theta08 -n 100 -p Theta="10**-8"
# python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/with_recruitment/parameters/theta/theta_10/ --food det --filename theta10 -n 100 -p Theta="10**-10"
# python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/with_recruitment/parameters/theta/theta_13/ --food det --filename theta13 -n 100 -p Theta="10**-13"

# python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/with_recruitment/parameters/theta/theta_16/ --food det --filename theta16 -n 100 -p Theta="10**-16"
# python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/with_recruitment/parameters/theta/theta_17/ --food det --filename theta17 -n 100 -p Theta="10**-17"
# python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/with_recruitment/parameters/theta/theta_18/ --food det --filename theta18 -n 100 -p Theta="10**-18"
# python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/with_recruitment/parameters/theta/theta_19/ --food det --filename theta19 -n 100 -p Theta="10**-19"
# python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/with_recruitment/parameters/theta/theta_20/ --food det --filename theta20 -n 100 -p Theta="10**-20"

# python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/with_recruitment/parameters/theta/theta_25/ --food det --filename theta25 -n 100 -p Theta="10**-25"
# python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/with_recruitment/parameters/theta/theta_30/ --food det --filename theta30 -n 100 -p Theta="10**-30"
# python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/with_recruitment/parameters/theta/theta_50/ --food det --filename theta50 -n 100 -p Theta="10**-50"

# python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/with_recruitment/parameters/theta/theta_35/ --food det --filename theta35 -n 100 -p Theta="10**-35"
# python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/with_recruitment/parameters/theta/theta_40/ --food det --filename theta40 -n 100 -p Theta="10**-40"
# python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/with_recruitment/parameters/theta/theta_45/ --food det --filename theta45 -n 100 -p Theta="10**-45"


python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/with_recruitment/parameters/theta/theta_60/ --food det --filename theta60 -n 100 -p Theta="10**-60"
python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/with_recruitment/parameters/theta/theta_70/ --food det --filename theta70 -n 100 -p Theta="10**-70"
python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/with_recruitment/parameters/theta/theta_80/ --food det --filename theta80 -n 100 -p Theta="10**-80"
python3 ~/research/AutomatAnts/code/run_cluster.py --directory ~/research/AutomatAnts/results/with_recruitment/parameters/theta/theta_90/ --food det --filename theta90 -n 100 -p Theta="10**-90"



deactivate