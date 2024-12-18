#-----------------------------------------------------------
#-
#-          Foraging Ant Model
#-
#----------------------------------------------------------

Execution instructions:

Is recommended to use a virtual enviroment:

	python3 -m venv env
	source env/bin/activate
	deactivate
	
To install all the libraries to run the model:

	pip install -r requeriments.txt

Running instructions:
	
	- Modify the paramaters and the file names in the params.py script
	- Execute the program: python3 run_model.py (1 Run)
	- Visualize the plots: python3 plots.py
	
Scripts

	- run_model.py : 1 Run of the model
	- run_model_eta.py : Execute the model for diferent values of eta
	- run_model_time.py : Various runs of the mdoel
	
Outputs:

	The model outputs can be found insede the Results folder
	
	- _info.dat = Contains the run information
	- _food.dat = Contains the food evolution
	- _state.dat = Contains the system evolution
	- _k.dat = Constains the "Snapshots" of the evoluton of the connectivity and the interactions
	
	
	- _eta.dat = Study of the parameter eta (previously run  run_model_eta.py)
	
	
	- _evolution_runs.dat = averaged states runs evolution (previously run  run_model_time.py)
	- _time_runs.dat = characteristic times of the different runs averages + errors(previously run  run_model_time.py)
	- _time_food_runs.dat =  averaged food quantity of the different runs (previously run  run_model_time.py)
	- _time_tag_runs.dat = averaged tags evolution of the different runs (previously run  run_model_time.py)
