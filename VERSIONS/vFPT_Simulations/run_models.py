from Model import *

# path = '/home/polfer/research/gits/AutomatAnts/results/2024/movement_results/' ## local
path = '/home/usuaris/pol.fernandez/research/AutomatAnts/results/2024/movement_results/' ## cluster

# for r in np.arange(0, 1.01, 0.1):
#     ## experimental scales
#     for R in np.arange(2.5, 20.01, 1.25):
#         m = Model(rho = r, R = R)
#         m.run()
#         fn = 'rho_%s_R_%s' % (r, R)
#         m.save_results(path, fn)

for r in np.arange(0, 1.01, 0.1):
    ## experimental scales
    m = Model(rho = r, R = 'DET')
    m.run()
    fn = 'rho_%s_R_%s' % (r, 'DET')
    m.save_results(path, fn)

        
        
