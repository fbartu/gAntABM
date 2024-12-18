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
              
### NF
              
# mot_matrix_LR = {1: [0.40, 0.15, 0.45], # <-- LR-scouts!
#               0: [0.45, 0.10, 0.45],
#               -1:[0.45, 0.15, 0.40]}      
              
# mot_matrix_SR = {1: [0.375, 0.250, 0.375], # <-- SR-scouts!
#               0: [0.450, 0.100, 0.450],
#               -1:[0.375, 0.250, 0.375]}
              
### DET
# mot_matrix_LR = {1: [0.40, 0.20, 0.40], # <-- LR-scouts!
#               0: [0.40, 0.20, 0.40],
#               -1:[0.40, 0.20, 0.40]}      
              
# mot_matrix_SR = {1: [0.36, 0.28, 0.36], # <-- SR-scouts!
#               0: [0.40, 0.20, 0.40],
#               -1:[0.36, 0.28, 0.36]}
              
## DET LR -- FREE TRACKLETS
# mot_matrix_LR = {1: [0.3770950,0.1703911, 0.4525140],
# 0: [0.46616541, 0.06015038, 0.47368421],
# -1: [0.4373259, 0.1838440, 0.3788301]}

## DET SR -- FREE TRACKLETS
# mot_matrix_SR = {1: [0.3571429, 0.2362637, 0.4065934],
# 0: [0.3928571,  0.0625000,  0.5446429],
# -1: [0.3594470, 0.2580645, 0.3824885]}

## NFD LR -- FREE TRACKLETS
mot_matrix_LR = {1: [0.3622642, 0.1716981, 0.4660377],
0: [0.4120879, 0.1098901, 0.4780220],
-1: [0.4904580, 0.1335878, 0.3759542]}

## NFD SR -- FREE TRACKLETS
mot_matrix_SR = {1: [0.3678571,0.2821429, 0.3500000],
0: [0.58273381, 0.04316547, 0.37410072],
-1: [0.4377880, 0.2488479, 0.3133641]}


