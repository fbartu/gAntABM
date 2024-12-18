""""""""""""""""""""""""""
""" DEFAULT PARAMETERS """
""""""""""""""""""""""""""

''' MODEL '''
N = 100 # number of automata
alpha = 2*10**-3 # 4.25*10**-3 # rate of action in nest
beta = 0.6 # 1.5 # rate of action in arena
gamma = 10**-5 # spontaneous activation
foodXvertex = 1

# sto_1: randomly distributed food (stochastic)
# sto_2: stochastic with clusterized food (hexagon patches)
# det: deterministic (sto_2 but with a specific and fixed positioning, emulating deterministic experiments)
# nf: no food (simulations without food)
food_condition = 'det'# 'sto_1', 'sto_2', 'nf'

''' LATTICE PARAMETERS '''
#Lattice size
width    = 22
height   = 13

nest = (0, 22)
nest_influence = [nest, (1, 21), (1, 22), (1, 23)] 
# direction_bias = 2 

''' THRESHOLDS ''' 
theta = 0
Theta = 10**-10 # 10**-15

''' Coupling coefficients matrix '''
# 0 - No info; 1 - Info
Jij = {'0-0': 0.01, '0-1': 1,
	   '1-0': 0.01, '1-1': 1}
# Jij = {'0-0': 0.4, '0-1': 1,
# 	   '1-0': 0.4, '1-1': 1}
    
''' Rounded matrix '''
mot_matrix = {1: [0.35, 0.15, 0.50], # <-- OG!
              0: [0.40, 0.20, 0.40],
              -1:[0.50, 0.15, 0.35]}
              
# mot_matrix = {1: [0.40, 0.15, 0.45], # <-- LR-scouts!
#               0: [0.45, 0.10, 0.45],
#               -1:[0.45, 0.15, 0.40]}      
              
# mot_matrix = {1: [0.375, 0.250, 0.375], # <-- LR-scouts!
#               0: [0.450, 0.100, 0.450],
#               -1:[0.375, 0.250, 0.375]}
        
              
# mot_matrix = {1: [0.40, 0.20, 0.40],
# 0: [0.40, 0.20, 0.40],
# -1:[0.40, 0.20, 0.40]}
              
# mot_matrix = {1: [0.20, 0.10, 0.70],
#               0: [0.45, 0.10, 0.45],
#               -1:[0.70, 0.10, 0.20]}
              
# mot_matrix = {1: [0.30, 0.10, 0.60],
#               0: [0.40, 0.20, 0.40],
#               -1:[0.60, 0.10, 0.30]}