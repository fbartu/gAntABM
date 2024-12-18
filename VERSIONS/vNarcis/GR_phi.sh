#!/bin/bash

# root directory
cd

export PATH=/home/soft/python-3.9.5/bin:$PATH
export LD_LIBRARY_PATH=/home/soft/python-3.9.5/bin/$LD_LIBRARY_PATH

. ~/research/automatenv/bin/activate

# normal model
python3 ~/research/AutomatAnts/code/run_model.py -r GR -x control_GR
# scanning parameter phi (noise in recruitment)
python3 ~/research/AutomatAnts/code/run_model.py -p phi=0.01 -x GRphi0.01 -r GR
python3 ~/research/AutomatAnts/code/run_model.py -p phi=0.05 -x GRphi0.05 -r GR
python3 ~/research/AutomatAnts/code/run_model.py -p phi=0.10 -x GRphi0.10 -r GR
python3 ~/research/AutomatAnts/code/run_model.py -p phi=0.15 -x GRphi0.15 -r GR
python3 ~/research/AutomatAnts/code/run_model.py -p phi=0.20 -x GRphi0.20 -r GR
python3 ~/research/AutomatAnts/code/run_model.py -p phi=0.25 -x GRphi0.25 -r GR
python3 ~/research/AutomatAnts/code/run_model.py -p phi=0.30 -x GRphi0.30 -r GR
python3 ~/research/AutomatAnts/code/run_model.py -p phi=0.35 -x GRphi0.35 -r GR
python3 ~/research/AutomatAnts/code/run_model.py -p phi=0.40 -x GRphi0.40 -r GR
python3 ~/research/AutomatAnts/code/run_model.py -p phi=0.45 -x GRphi0.45 -r GR
python3 ~/research/AutomatAnts/code/run_model.py -p phi=0.50 -x GRphi0.50 -r GR
python3 ~/research/AutomatAnts/code/run_model.py -p phi=0.55 -x GRphi0.55 -r GR
python3 ~/research/AutomatAnts/code/run_model.py -p phi=0.60 -x GRphi0.60 -r GR
python3 ~/research/AutomatAnts/code/run_model.py -p phi=0.65 -x GRphi0.65 -r GR
python3 ~/research/AutomatAnts/code/run_model.py -p phi=0.70 -x GRphi0.70 -r GR
python3 ~/research/AutomatAnts/code/run_model.py -p phi=0.75 -x GRphi0.75 -r GR
python3 ~/research/AutomatAnts/code/run_model.py -p phi=0.80 -x GRphi0.80 -r GR
python3 ~/research/AutomatAnts/code/run_model.py -p phi=0.85 -x GRphi0.85 -r GR
python3 ~/research/AutomatAnts/code/run_model.py -p phi=0.90 -x GRphi0.90 -r GR
python3 ~/research/AutomatAnts/code/run_model.py -p phi=0.95 -x GRphi0.95 -r GR
python3 ~/research/AutomatAnts/code/run_model.py -p phi=1.00 -x GRphi1.00 -r GR
python3 ~/research/AutomatAnts/code/run_model.py -p phi=2.00 -x GRphi2.00 -r GR
python3 ~/research/AutomatAnts/code/run_model.py -p phi=3.00 -x GRphi3.00 -r GR
# serial recruitment
python3 ~/research/AutomatAnts/code/run_model.py -r GR,s -x SerialR_GR
deactivate

#how to run
#qsub ~/research/AutomatAnts/code/run_model.sh 
#qsub -pe make 20 -l h_vmem=8G ~/research/AutomatAnts/code/run_model.sh