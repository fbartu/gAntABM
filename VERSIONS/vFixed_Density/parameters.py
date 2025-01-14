""""""""""""""""""""""""""
""" DEFAULT PARAMETERS """
""""""""""""""""""""""""""

''' MODEL '''
N = 25 # number of automata
beta = 0.25 # 1.5 # rate of action in arena
foodXvertex = 1

# sto_1: randomly distributed food (stochastic)
# sto_2: stochastic with clusterized food (hexagon patches)
# det: deterministic (sto_2 but with a specific and fixed positioning, emulating deterministic experiments)
# nf: no food (simulations without food)
food_condition = 'nf'# 'sto_1', 'sto_2', 'nf'

''' LATTICE PARAMETERS '''
#Lattice size
width    = 22
height   = 13

nest = (0, 22)

''' THRESHOLDS ''' 
theta = 0
Theta = 10**-10 # 10**-15

''' Coupling coefficients matrix '''
# 0 - No info; 1 - Info
Jij = {'0-0': 0.01, '0-1': 1,
	   '1-0': 0.01, '1-1': 1}

''' Turning probabilities '''              
scout_mov = {'l': 0.4185, 'b': 0.1841, 'r': 0.3974}
recruit_mov = {'l': 0.3783, 'b': 0.3038, 'r': 0.3179}


