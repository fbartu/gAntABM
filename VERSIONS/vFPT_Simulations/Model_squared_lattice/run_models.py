from Model import *

# path = '/home/polfer/research/gits/AutomatAnts/results/2024/movement_results/' ## local
path = '/home/usuaris/pol.fernandez/research/AutomatAnts/results/2024/movement_results/' ## cluster

for r in np.arange(0, 1.01, 0.1):
    ## small scales (experiments)
    for R in np.arange(2.0, 20.01, 2.0):
        m = Model(rho = r, R = R)
        m.run()
        fn = 'rho_%s_R_%s' % (r, R)
        m.save_results(path, fn)
    
    ## large scales (hypothetical)
    for R in np.arange(24, 101, 4):
        m = Model(rho = r, R = R)
        m.run()
        fn = 'rho_%s_R_%s' % (r, R)
        m.save_results(path, fn)

        
        
