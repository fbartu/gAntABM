from Model import *
import os, uuid, time
from multiprocessing import Pool, cpu_count
import itertools

# path = '/home/polfer/research/gits/AutomatAnts/results/2024/movement_results/' ## local
path = '/home/usuaris/pol.fernandez/research/AutomatAnts/results/2024/movement_simulations/' ## cluster
        
rho_range = np.round(np.arange(0, 1.01, 0.1), 3)
R_range = np.round(np.arange(2.5, 20.01, 1.25), 3)
args = list(itertools.product(rho_range, R_range))

def run_model(rho, R):
    pid = os.getpid()
    t = int(time.time())
    uid = uuid.uuid4().int
    seed = hash((pid, t, uid, rho+R)) % (2**32 - 1)
    np.random.seed(seed)

    m = Model(rho = rho, R = R)
    m.run()
    fn = 'rho_%s_R_%s' % (rho, R)
    m.save_results(path, fn)
        
        
if __name__ == '__main__':

    num_processes = cpu_count()
    pool = Pool(processes=num_processes)

    pool.starmap(run_model, args)
    pool.close()
    pool.join()
