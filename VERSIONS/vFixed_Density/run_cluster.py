import Model
from multiprocessing import Pool, cpu_count
import os, time, uuid
import numpy as np
from functions import argparser
import gc

parameters = argparser()   

food_condition = parameters.pop('food_condition')
results_path = os.path.expanduser(parameters.pop('results_path'))
filename = parameters.pop('filename')
runs = parameters.pop('runs')
beta = parameters.pop('beta')
# alpha, beta, gamma = parameters.pop('alpha'), parameters.pop('beta'), parameters.pop('gamma')


def run_model(i):
    pid = os.getpid()
    t = int(time.time())
    uid = uuid.uuid4().int
    seed = hash((pid, t, uid, i)) % (2**32 - 1)
    np.random.seed(seed)

    try:
        m = Model.Model(beta=beta,
                    food_condition= food_condition, **parameters)
        print('Model loaded', flush = True)
        m.run()
        print('Model successfully run', flush = True)
        m.save_results(results_path, filename + '_' + str(i))
        del m
        gc.collect()
        return True
    except:
        with open(results_path + '_VOID_' + filename + str(i) + '.txt', 'w') as f:
            f.write('')
        return False
        
        
if __name__ == '__main__':

    num_processes = cpu_count()
    pool = Pool(processes=num_processes)

    pool.map(run_model, range(runs))
    pool.close()
    pool.join()
