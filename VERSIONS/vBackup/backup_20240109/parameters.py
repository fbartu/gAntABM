""""""""""""""""""""""""""
""" DEFAULT PARAMETERS """
""""""""""""""""""""""""""

''' MODEL '''
N = 100 # number of automata
alpha = 4.25*10**-3 # rate of action in nest ## <---- used to be 4*10**-3
beta = 2 # rate of action in arena
gamma = 10**-5 # spontaneous activation
foodXvertex = 1

# sto_1: randomly distributed food (stochastic)
# sto_2: stochastic with clusterized food (hexagon patches)
# det: deterministic (sto_2 but with a specific and fixed positioning, emulating deterministic experiments)
# nf: no food (simulations without food)
food_condition = 'sto_1' # 'det', 'sto_2', 'nf'

''' LATTICE PARAMETERS '''
#Lattice size
width    = 22
height   = 13

nest = (0, 22)
nest_influence = [nest, (1, 21), (1, 22), (1, 23)] 
direction_bias = 3 # integer >= 1

''' THRESHOLDS ''' 
theta = 0
Theta = 10**-15 ## with 10**-16 works as well (maybe a little better even)

''' Coupling coefficients matrix '''
# 0 - No info; 1 - Info
Jij = {'0-0': 0.4, '0-1': 1,
	   '1-0': 0.4, '1-1': 1}

''' Motility matrix '''
# mot_matrix = {1: [0.3587100, 0.1538814, 0.4874086],
#               0: [0.4170414, 0.1813527, 0.4016059],
#               -1: [0.4885684, 0.1592719, 0.3521597]}
''' Rounded matrix '''
mot_matrix = {1: [0.35, 0.15, 0.50],
              0: [0.40, 0.20, 0.40],
              -1:[0.50, 0.15, 0.35]}