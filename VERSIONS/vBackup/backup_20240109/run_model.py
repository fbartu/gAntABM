import Model
import json
from functions import argparser

parameters = argparser()   

food_condition = parameters.pop('food_condition')
results_path = parameters.pop('results_path')
filename = parameters.pop('filename')
runs = parameters.pop('runs')
alpha, beta, gamma = parameters.pop('alpha'), parameters.pop('beta'), parameters.pop('gamma')

m = Model.Model(alpha=alpha, beta=beta, gamma=gamma,
                    food_condition= food_condition, **parameters)

for i in range(runs):
    m.run()
    # result = {'T': m.T, 'N': m.N, 'I': m.I, 'gIn': m.gIn, 'gOut': m.gOut}
    # result = {'T': m.T, 'N': m.N, 'I': m.I, 'SiIn': m.n, 'SiOut': m.o}
    result = {'T': m.T, 'N': m.N, 'I': m.I, 'SiOut': m.o, 'pos': m.position_history}
    path = '%s%s_%s.json' % (results_path,filename, i)
    with open (path, 'w') as f:
        json.dump(result, f)
    with open (results_path+filename+str(i)+'_config.json', 'w') as f:
        json.dump(m.init_state, f)
    del m
    m = Model.Model(alpha=alpha, beta=beta, gamma=gamma,
                    food_condition= food_condition, **parameters)