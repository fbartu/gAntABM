#!/bin/bash

# root directory
cd

export PATH=/home/soft/python-3.9.5/bin:$PATH
export LD_LIBRARY_PATH=/home/soft/python-3.9.5/bin/$LD_LIBRARY_PATH

. ~/research/automatenv/bin/activate

# normal model
python3 ~/research/AutomatAnts/code/run_model.py -x Control_1000 --nruns 1000,True

# scanning parameter phi (noise in recruitment)
for i in $(seq 0.01 0.03 1)
do 
echo "Running model with phi = $i"
python3 ~/research/AutomatAnts/code/run_model.py -p phi=$i -x 1000phi$i --nruns 1000,True 
done

# serial recruitment
python3 ~/research/AutomatAnts/code/run_model.py -r HR,s -x SerialR_1000 --nruns 1000,True
deactivate

#how to run
#qsub ~/research/AutomatAnts/code/run_model.sh 
#qsub -pe make 20 -l h_vmem=8G ~/research/AutomatAnts/code/run_model.sh