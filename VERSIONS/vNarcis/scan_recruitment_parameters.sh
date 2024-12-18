#!/bin/bash

# root directory
cd

export PATH=/home/soft/python-3.9.5/bin:$PATH
export LD_LIBRARY_PATH=/home/soft/python-3.9.5/bin/$LD_LIBRARY_PATH

. ~/research/automatenv/bin/activate

# default model
python3 ~/research/AutomatAnts/code/run_model.py -x Control_Noise -r GR --nruns 20,True

# scanning noise in recruitment
for i in $(seq 0.0001 0.35 5)
do 
#echo "Running model with gamma_1 = $i"
#python3 ~/research/AutomatAnts/code/run_model.py -p gamma_1=$i -x gamma_1$i --nruns 20,True 
#echo "Running model with gamma_2 = $i"
#python3 ~/research/AutomatAnts/code/run_model.py -p gamma_2=$i -x gamma_2$i --nruns 20,True 
echo "Running model with both gammas = $i"
python3 ~/research/AutomatAnts/code/run_model.py -p gamma_1=$i,gamma_2=$i -x gamma_effect$i --nruns 20,True 
done

deactivate

#how to run
#qsub ~/research/AutomatAnts/code/run_model.sh 
#qsub -pe make 20 -l h_vmem=8G ~/research/AutomatAnts/code/run_model.sh