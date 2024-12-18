import networkx as nx
from mesa import space, Agent, Model
import math
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from functions import *
from scipy.stats import pearsonr

""""""""""""""""""
""" PARAMETERS """
""""""""""""""""""
'''

### WORKING, kind of ###
N = 100 # number of automata
alpha = 10**-3# 7.5*10**-4# (5*10**-3)# 2*10**-3# 1.5*10**-3 # rate of action in nest
beta = 1/2# 1/5 # rate of action in arena
gamma = 10**-5# 5*10**-6
p = 0.2
Theta = 10**-15 # baseline loss of activity (threshold 1)
theta = 0 # threshold of activity (threshold 2)
Interactions = 4 # integer, number of max interactions in a node
xInteraction = 4
weight = 3 # integer >= 1, direction bias

# Coupling coefficients
# 0 - No info; 1 - Info
Jij = {'0-0': 0.9, '0-1': 2,
       '1-0': 0.75, '1-1': 0.5}
'''

'''
## WITHOUT SPONTANEOUS RETURN TO NEST, THIS WORKS SEMI-FINE
N = 100#150 # number of automata
alpha = 10**-3#1.25*10**-3# 10**-3 #1.5*10**-3#2*10**-3# 1*10**-3# 1.25*10**-3 # rate of action in nest
beta = 1/3#1/2#2/3 # 1/4 #3/4# 1.2 # 2/3# 1/5 # rate of action in arena
gamma = 0# 5*10**-6 # spontaneous activation
p = 0 # 0.1
Theta = 10**-15# 10**-15 # baseline loss of activity (threshold 1)
theta = 0 # threshold of activity (threshold 2)
Interactions = 1#1 # integer, number of max interactions in a node
xInteraction = 1#1
weight = 3 # integer >= 1, direction bias
'''
## alpha = 3*10**-3 ## Jij['0-0'] = 0.4

# N = 200#100 # number of automata
# alpha = 2*10**-3# 3* 10**-3 # 1.25*10**-3# 10**-3 #1.5*10**-3#2*10**-3# 1*10**-3# 1.25*10**-3 # rate of action in nest
# beta = 0.5 # 1/2#2/3 # 1/4 #3/4# 1.2 # 2/3# 1/5 # rate of action in arena
# gamma = 2*10**-5 # 5*10**-6 # spontaneous activation
# p = 0
# Theta = 10**-15# 10**-15 # baseline loss of activity (threshold 1)
# theta = 0 # threshold of activity (threshold 2)
# Interactions = 1#1 # integer, number of max interactions in a node
# xInteraction = 1#1
# weight = 3 # integer >= 1, direction bias


N = 100#100 # number of automata
alpha = 2*10**-3# 3* 10**-3 # 1.25*10**-3# 10**-3 #1.5*10**-3#2*10**-3# 1*10**-3# 1.25*10**-3 # rate of action in nest
beta = 1 # 1/2#2/3 # 1/4 #3/4# 1.2 # 2/3# 1/5 # rate of action in arena
gamma = 2*10**-5 # 5*10**-6 # spontaneous activation
p = 0
Theta = 10**-15# 10**-15 # baseline loss of activity (threshold 1)
theta = 0 # threshold of activity (threshold 2)
Interactions = 1#1 # integer, number of max interactions in a node
xInteraction = 1#1
weight = 3 # integer >= 1, direction bias

# Coupling coefficients
# 0 - No info; 1 - Info
# Jij = {'0-0': 0.9, '0-1': 1.5,
#        '1-0': 0.9, '1-1': 0.9}
# Jij = {'0-0': 0.9, '0-1': 1.5,
#        '1-0': 0.5, '1-1': 0.75}
# Jij = {'0-0': 1, '0-1': 1.5,
#        '1-0': 0.5, '1-1': 0.75}
# Jij = {'0-0': 0.9, '0-1': 1.5,
#        '1-0': 0.4, '1-1': 1}
# Jij = {'0-0': 0.9, '0-1': 1.25,
#        '1-0': 0.5, '1-1': 0.75}
# Jij = {'0-0': 0.75, '0-1': 1.25,
#        '1-0': 0.25, '1-1': 0.5}
# Jij = {'0-0': 0.9, '0-1': 1.5,
#        '1-0': 0.5, '1-1': 0.75}
# Jij = {'0-0': 0.5, '0-1': 1,
#        '1-0': 0.25, '1-1': 0.5} ## MATRIX WITHOUT SELF INTERACTION
# Jij = {'0-0': 0.5, '0-1': 1,
#        '1-0': 0.25, '1-1': 0.75} ## MATRIX WITHOUT SELF INTERACTION
# Jij = {'0-0': 0.75, '0-1': 1, '0-2': 1,
#        '1-0': 0.25, '1-1': 0.65, '1-2': 1,
#        '2-0': 0.25, '2-1': 0, '2-2': 0.25} ## MATRIX WITH NO INFO, NO FOOD INFO, FOOD INFO
Jij = {'0-0': 0.35, '0-1': 1,
       '1-0': 0.35, '1-1': 0.75} ## MATRIX WITH TWO G POPULATIONS

""""""""""""""""""""""""""
""" SPATIAL PARAMETERS """
""""""""""""""""""""""""""
nest = (0, 22)
nest_influence = [nest, (1, 21), (1, 22), (1, 23)]

# wrong matrix (?)
# mot_matrix = {1: [0.4377143, 0.2817919, 0.2804938],
#               0: [0.4825561, 0.2051468, 0.3122971],
#               -1: [0.2376265, 0.2802202, 0.4821533]}
# det            
mot_matrix = {1: [0.3574467, 0.1720547, 0.4704986],
              0: [0.3963954, 0.2160944, 0.3875102],
              -1: [0.4771861, 0.1759704, 0.3468435]}
# sto             
mot_matrix = {1: [0.3557945, 0.1432286, 0.5009769],
              0: [0.4235170, 0.1712218, 0.4052612],
              -1: [0.4926485, 0.1707956, 0.3365559]}
# nf              
mot_matrix = {1: [0.3618471, 0.1604845, 0.4776684],
              0: [0.4513639, 0.1348430, 0.4137931],
              -1: [0.4926485, 0.1707956, 0.3365559]}

# total matrix
mot_matrix = {1: [0.3587100, 0.1538814, 0.4874086],
              0: [0.4170414, 0.1813527, 0.4016059],
              -1: [0.4885684, 0.1592719, 0.3521597]}
              
# random matrix
# mot_matrix = {1: [1/3] * 3,
#               0: [1/3] * 3,
#               -1: [1/3] * 3}              

# DETERMINIST
food_positions = [(6, 33), (6, 34), (7, 34), # patch 1
	(7, 33), (7, 32), (6, 32),
	(6, 11), (6, 12), (7, 12), # patch 2
	(7, 11), (7, 10), (6, 10)]
 
# STOCHASTIC

## close - far
# food_positions = [(9, 44), (9, 45), (10, 45),
# (10, 44), (10, 43), (9, 43), # patch 1
# 	(6, 11), (6, 12), (7, 12), # patch 2
# 	(7, 11), (7, 10), (6, 10)]
 
## far - far
# food_positions = [(9, 44), (9, 45), (10, 45),
# (10, 44), (10, 43), (9, 43), # patch 1
# 	(12, 7), (12, 8), (13, 8), # patch 2
# 	(13, 7), (13, 6), (12, 6)]
 
 ## far - far
# food_positions = [(1, 32), (1, 33), (2, 33),
# (2, 32), (2, 31), (1, 31), # patch 1
# 	(2, 17), (2, 18), (3, 18), # patch 2
# 	(3, 17), (3, 16), (2, 16)]
foodXvertex = 1

food = dict.fromkeys(food_positions, foodXvertex)

#Lattice size
width    = 22
height   = 13


""""""""""""""""""
"""   CLASSES  """
""""""""""""""""""

''' ANT AGENT '''
class Ant(Agent):

	def __init__(self, unique_id, model):

		super().__init__(unique_id, model)

		self.Si = 0
		self.g = np.random.uniform(0.0, 1.0)
		# self.g = np.random.normal(0.5, 0.15) # np.random.normal(0.5, 0.2)

		self.is_active = False
		self.state = '0'
		self.status = 'gamma'

		self.activity = {'t': [0], 'Si': [self.Si]}
  
		self.food = []

		self.pos = 'nest'
		self.movement = 'random'
  
		# self.last_move = None
		self.move_history = (None, None, None)
		self.path = []

	# Move method
	def move(self):

		possible_steps = self.model.grid.get_neighbors(
		self.pos,
		include_center = False)
  
		l = list(range(len(possible_steps)))

		if self.movement == 'random':
			
			idx = np.random.choice(l)
      
		else:
			d = [dist(self.target, self.model.coords[i]) for i in possible_steps]
			idx = np.argmin(d)

			v = 1 / (len(d) + weight - 1)
			p = [weight / (len(d) + weight - 1) if i == idx else v for i in l]
			idx = np.random.choice(l, p = p)

		pos = possible_steps[idx]
		self.model.grid.move_agent(self, pos)
 
	def reset_movement(self):
		self.movement = 'random'
		self.move_history = (None, None, None)
 
	def update_movement(self):
		self.move_history = (self.move_history[1], self.move_history[2], self.pos)
 
	# def move(self):
    
	# 	# possible_steps = self.model.grid.get_neighbors(
	# 	# self.pos,
	# 	# include_center = False)
	# 	possible_steps = self.model.grid.get_neighbors(
	# 	self.pos,
	# 	include_center = True)
  
	# 	l = list(range(len(possible_steps)))

	# 	if self.movement == 'random':
	# 		# if None in self.move_history or len(l) < 10:
	# 		if None in self.move_history or len(l) != 3:
	# 			idx = np.random.choice(l)
    
	# 		else:
	# 			p = np.array(mot_matrix[direction([self.model.coords[i] for i in self.move_history])])
	# 			ords = []
	# 			for i in range(len(possible_steps)):
	# 				x = [self.move_history[1], self.move_history[2], possible_steps[i]]
	# 				y = [self.model.coords[z] for z in x]
	# 				ords.append(direction(y))
     
	# 			idx = np.random.choice(l, p = p[np.argsort(ords)[::-1]])
    
	# 	else:
	# 		d = [dist(self.target, self.model.coords[i]) for i in possible_steps]
	# 		idx = np.argmin(d)

	# 		v = 1 / (len(d) + weight - 1)
	# 		p = [weight / (len(d) + weight - 1) if i == idx else v for i in l]
	# 		idx = np.random.choice(l, p = p)

	# 	pos = possible_steps[idx]
	# 	self.model.grid.move_agent(self, pos)
	# 	self.path.append(self.pos)
	# 	self.update_movement()

	def find_neighbors(self, n = 1):

		if self.pos == 'nest':
   
			alist = self.model.states['alpha']
			# alist = list(filter(lambda a: a.unique_id != self.unique_id, list(self.model.states['alpha'])))

		else:
			alist = self.model.grid.get_cell_list_contents([self.pos])
			# alist = list(filter(lambda a: a.unique_id != self.unique_id, self.model.grid.get_cell_list_contents([self.pos])))

		# l = len(alist)
		idx = np.where([i.unique_id == self.unique_id for i in alist])[0]
		l = len(alist) # should be l-1
		if len(idx):

			l2 = l - len(idx)

			w = abs(np.array(list(range(l))) - idx)
			w2 = abs(w - (np.max(w) + 1))
			w2[idx] = 0
   
		else: # the ant just entered the nest
			l2 = l
			w2 = np.array(list(range((l), 0, -1)))
   
		w2 = np.array([1] * len(w2))
		p = w2 / np.sum(w2)

		if l2 > n:

			neighbors = np.random.choice(alist, size = n, replace = False, p = p)

		elif l2 > 0:

			neighbors = np.random.choice(alist, size = l2, replace = False, p = p)

		else:
			neighbors = []

		return neighbors

	def interaction(self, n = xInteraction):
		neighbors = self.find_neighbors(n)

		s = [] # state
		z = [] # activity
  
		l = len(neighbors)
		if l:
			for i in neighbors:
				s.append(i.state)
				z.append(Jij[self.state + "-" + i.state]* i.Si - Theta)

			z = sum(z)
   
			if self.pos in ['nest'] + nest_influence:
				self.model.I.append(0)
			else:
				self.model.I.append(+1)
    
		else:
			z = -Theta
			self.model.I.append(0)
		self.Si = math.tanh(self.g * (z + self.Si) ) # update activity
		# self.Si = math.tanh(self.g * (z + self.Si * Jij[self.state + "-" + self.state]) ) # update activity
		self.update_role(s) # update state

	def update_role(self, states):
    
		# if '2' in states and self.state == '1':
		# 	if np.random.random() < p:
		# 		self.state = '0'
    
		if '1' in states:
			if np.random.random() < p:
				self.state = '1'
    
	def update_status(self):
		self.check_status()
		for i in self.model.states:
			try:
				self.model.states[i].remove(self)
			except:
				continue
    
		if self.status == 'gamma':
			self.model.states['alpha'].append(self)
			self.model.states['gamma'].append(self)
   
		else:
			self.model.states[self.status].append(self)
    
	def check_status(self):
		if self.is_active:
			self.status = 'beta'
		else:
			if self.Si > theta:
				self.status = 'alpha'
			else:
				self.status = 'gamma'
 
	def report_info(self):
		neighbors = self.find_neighbors(Interactions)
		for i in neighbors:
			state = i.state + "-" + self.state
			i.Si = math.tanh(i.g * (i.Si * Jij[i.state + "-" + i.state] + (Jij[state] * self.Si - Theta)))
			i.update_status()
      
	# def report_exit(self):
	# 	self.model.S[0] -= 1
	# 	self.model.S[1] += 1
	# 	self.model.states['beta'].append(self.unique_id)
	# 	self.model.in_nest.remove(self.unique_id)
	# 	self.model.C.append(+1)

	# def report_entry(self):
	# 	self.model.S[0] += 1
	# 	self.model.S[1] -= 1
	# 	self.model.out.remove(self.unique_id)
	# 	self.model.in_nest.append(self.unique_id)
	# 	self.model.C.append(-1)

	def leave_nest(self):
		self.model.grid.place_agent(self, nest)
		self.is_active = True
		# self.report_exit()

	def enter_nest(self):
		self.model.remove_agent(self)
		self.is_active = False
		self.pos = 'nest'
		self.ant2explore()
		# self.report_info() ## DESACTIVAT NO HI HA COMUNICACIÓ CAP AL NIU !
		self.model.Si_flow['t'].append(self.model.time)
		self.model.Si_flow['g'].append(self.g)
		self.model.Si_flow['Si'].append(self.Si)
		self.model.Si_flow['info'].append(self.state)
		self.model.Si_flow['id'].append(self.unique_id)
		# self.report_entry()

	def ant2nest(self):
		self.target = self.model.coords[nest]
		self.movement = 'homing'
  
		# if self.state != '2':
		# 	if np.random.random() < 1:
		# 		self.state = '1'

	def ant2explore(self):
		if hasattr(self, 'target'):
			del self.target
		self.reset_movement()
		# self.movement = 'random'


	def pick_food(self):
		self.model.remove_agent(self.model.food[self.pos][0])
		self.food.append(self.model.food[self.pos].pop(0))
		self.model.food[self.pos].extend(self.food)
		self.model.food[self.pos][-1].collected(self.model.time)
		food[self.pos] -= 1
		self.food_location = self.pos
		# self.state = '2'
		self.state = '1'
		# print('Position: ' + str(self.pos) +'\n'+
  		# 	'Time: ' +str(round(self.model.time/60)) + ' min \n'+
     	# 	'ID: ' +str(self.unique_id)+'\n'+
		# 	'Si :' + str(self.Si) + '\n'+
		# 	'Prev Si: ' + str(self.prev_Si) + '\n'+
		# 	'New Si: ' + str(self.new_Si) +'\n'+
		# 	'Neighbors: '+ str(self.neighbors) +'\n'+
   		# 	'------------------------ \n')
  
	def eval_status(self):
		if hasattr(self, 'target') and not len(self.food):
			del self.target
			self.movement = 'random'

	def drop_food(self):
		self.food.pop()
  
	def action(self, rate):
		
		if rate == 'alpha':
			if len(self.food):
				self.drop_food()
			else:
				if self.Si > theta:
					self.leave_nest()

		elif rate == 'beta':
      
			if len(self.food) or self.Si < theta:
				self.ant2nest()

			if self.pos == nest:
				if hasattr(self, 'target') and self.target == self.model.coords[nest]:
					self.enter_nest()

				else:
					self.move()

			elif self.pos in food_positions:
       
				if food[self.pos] > 0 and not len(self.food):
					self.neighbors = self.find_neighbors()
					self.pick_food()

				else:
					self.move()

			else:
				self.move()
   
		else:
			self.Si = np.random.uniform(0.0, 1.0) ## spontaneous activation
			# self.Si = 0.1
		# if self.pos in food_positions:
		# 	self.prev_Si = self.Si
		# 	self.interaction()
		# 	self.new_Si = self.Si
			# print('Neighbors: ' + str(self.find_neighbors())+ '\n'+
			# '++++++++++++++++++++ \n')
		# else: 
		# 	self.interaction()
		self.interaction()
		self.update_status()
		self.activity['Si'].append(self.Si)
  
		## TEST MATERIAL !!
		# if self.pos == nest and np.random.random() < 1/3:
		# 	self.ant2nest()
  

	# def action(self):
	# 	if self.is_active: # in arena
	# 		if len(self.food) or self.Si < theta:
	# 			self.ant2nest()

	# 		if self.pos == nest:
	# 			if hasattr(self, 'target') and self.target == self.model.coords[nest]:
	# 				self.enter_nest()

	# 			else:
	# 				self.move()

	# 		elif self.pos in food_positions:
	# 			if food[self.pos] > 0 and not len(self.food):
	# 				self.pick_food()

	# 			else:
	# 				self.move()

	# 		else:
	# 			self.move()

	# 	else:
      
	# 		if len(self.food):
	# 			self.drop_food()
     
	# 		else:
	# 			if self.Si > theta:
	# 				self.leave_nest()

	# 	self.interaction()
	# 	self.update_status()
		# self.eval_status()

''' MODEL '''
class Model(Model):

	def __init__(self, alpha = alpha, beta = beta, gamma = gamma, N = N, width = width, height = height):

		super().__init__()

		nds = [(0, i) for i in range(1, 44, 2)]

		# Lattice
		self.g = nx.hexagonal_lattice_graph(width, height, periodic = False)
		[self.g.remove_node(i) for i in nds]
		self.coords = nx.get_node_attributes(self.g, 'pos')
		self.grid = space.NetworkGrid(self.g)
		x = [xy[0] for xy in self.coords.values()]
		y = [xy[1] for xy in self.coords.values()]
		xy = [rotate(x[i], y[i], theta = math.pi / 2) for i in range(len(x))]
		self.xy = dict(zip(self.coords.keys(), xy))
  
		# Agents
		self.agents = {}
		# for i in range(N):
		counter = 0
		for i in range((N-1), -1, -1):
			
			self.agents[i] = Ant(i, self)
			# if counter < 50:
			# 	self.agents[i].g = np.random.normal(0.75, 0.05)
			# else:
			# 	self.agents[i].g = np.random.normal(0.25, 0.05)
   
		# states & rates
		self.states = {'alpha': list(self.agents.values()), 'beta': [], 'gamma': list(self.agents.values())}
		self.S = np.array([N, 0, N])
		self.rates = np.array([alpha, beta, gamma])
  
		self.agents[0].Si = np.random.uniform(0.0, 1.0)
		self.agents[0].update_status()
  
		self.Si_flow = {'t': [], 'g': [], 'Si': [], 'info': [], 'id': []}
		
	
		# self.alpha = alpha
		# self.beta = beta
		# self.gamma = gamma

		self.Si = [np.mean([i.Si for i in list(self.agents.values())])]

  		# Food
		self.food_id = -1
		self.food_in_nest = 0
		if foodXvertex > 0:
			self.food = {}
			for i in food:
				self.food[i] = [Food(i)] * foodXvertex
				for x in range(foodXvertex):
					self.grid.place_agent(self.food[i][x], i)
					self.food[i][x].unique_id = self.food_id
					self.food_id -= 1

		else:
			self.food = dict.fromkeys(food.keys(), [np.nan])
   
		self.init_state = {'Si': [self.agents[i].Si for i in self.agents],
                     'g': [self.agents[i].g for i in self.agents],
                     'food': len(self.food), 'alpha': alpha, 'beta': beta,
                     'gamma': gamma, 'N': N}

		# Rates
		self.update_rates()
		self.rate2prob()

		# Time & Gillespie
		self.time = 0
		self.sample_time()

		# Metrics
		self.T = [0] # time
		self.N = [0] # population
		# self.Nexp = [0]
		self.I = [0] # interactions
		# self.C = [0] # alpha ~ nest departures and entries
		# self.XY = {self.T[-1]: [a.pos for a in self.agents.values()]}
		self.XY = dict(zip(list(self.coords.keys()), [0] *len(self.coords.keys())))
		# self.A = [self.rates[0]]
		self.n = [np.mean([self.agents[i].Si for i in self.agents])]
		self.o = [0]
		self.gOut = [0]
		self.gIn = [np.mean([self.agents[i].g for i in self.agents])]
		self.iters = 0
		self.a = [self.r[0]]
		self.gamma_counter = 0
		# self.alpha_counter = 0
		# self.beta_counter = 0

		self.sampled_agent = []
  
	def update_rates(self):
		self.S = np.array([len(i) for i in list(self.states.values())])
		self.r = self.S * self.rates # np.array([self.alpha, self.beta, self.gamma]) 

	def rate2prob(self):
		self.R_t = np.sum(self.r)
		self.r_norm = self.r / self.R_t

	def sample_time(self):
		self.rng = np.random.random()
		self.rng_t = (1 /self.R_t) * np.log(1 / self.rng)

	def remove_agent(self, agent: Agent) -> None:
		""" Remove the agent from the network and set its pos variable to None. """
		pos = agent.pos
		self._remove_agent(agent, pos)
		agent.pos = None

	def _remove_agent(self, agent: Agent, node_id: int) -> None:
		""" Remove an agent from a node. """

		self.g.nodes[node_id]["agent"].remove(agent)

	def step(self, tmax):

		while self.time < tmax:
      
			process = np.random.choice(['alpha', 'beta', 'gamma'], p = self.r_norm)
   
			if process == 'alpha':
					
				# w = 1 + np.unique([i.Si for i in self.states['alpha']], return_inverse = True)[1]
				# p = w / np.sum(w)
				# agent = np.random.choice(self.states['alpha'], p = p)
				agent = np.random.choice(self.states['alpha'])
				# self.alpha_counter += 1
    
			elif process == 'beta':
       
				# w = 1 + np.unique([i.Si for i in self.states['beta']], return_inverse = True)[1]
				# p = w / np.sum(w)
				# agent = np.random.choice(self.states['beta'], p = p)
				agent = np.random.choice(self.states['beta'])
				# self.beta_counter += 1
    
			else:
				# w = 1 + np.unique([i.Si for i in self.states['gamma']], return_inverse = True)[1]
				# p = w / np.sum(w)
				# agent = np.random.choice(self.states['gamma'], p = p)
				agent = np.random.choice(self.states['gamma'])

				self.gamma_counter += 1

			# agent = self.agents[id]
			self.sampled_agent.append(agent.unique_id)
			# self.sampled_agent.append(id)

			# do action
			agent.action(process)

			# if len(self.C) == len(self.T):
			# 	self.C.append(0)

			# self.A.append(self.rates[0])
   
			self.N.append(len(self.states['beta']))
			# self.Nexp.append(np.sum([self.agents[i].pos not in [nest, (1, 21)] for i in self.states['beta']]))


			# self.XY[self.T[-1]] = [a.pos for a in self.agents.values()]
			if agent.pos != 'nest':
				self.XY[agent.pos] += 1
			self.n.append(np.mean([i.Si for i in self.states['alpha']]))
			self.o.append(np.mean([i.Si for i in self.states['beta']]))
			self.gIn.append(np.mean([i.g for i in self.states['alpha']]))
			self.gOut.append(np.mean([i.g for i in self.states['beta']]))
			self.Si.append(np.mean([i.Si for i in list(self.agents.values())]))
   
			self.update_rates()
			self.rate2prob()
   
			self.a.append(self.r[0])

			self.iters += 1

			# get time for next iteration
			self.time += self.rng_t
			self.T.append(self.time)
			agent.activity['t'].append(self.time)

			# get rng for next iteration
			self.sample_time()

			
	def run(self, tmax = 10800, plots = False):

		self.step(tmax = tmax)
		if plots:
			self.plot_N()
			self.plot_I()
  
	def run_food(self, tmax, plots = False):
		n = sum(food.values())
		t = 1
		while sum(food.values()) == n:
			self.step(t)
			t += 1
		self.step(tmax + t)
		if plots:
			self.plot_N()
			# self.plot_I()

	def save_results(self, path):
		# self.results = pd.DataFrame({'N': self.N, 'T': self.T, 'I':self.I, 'C': self.C,
        #                        'nest': self.n, 'arena': self.o})
		# self.results['F'] = 0
		# self.results.iloc[np.where([self.T == x for x in [self.food[i][0].collection_time for i in self.food]])[1],-1] = 1
		# self.results.to_csv(path + 'N.csv')
		self.results = pd.DataFrame({'N': self.N, 'T': self.T, 'I':self.I})
		self.results.to_csv(path + 'N.csv')

	def plot_lattice(self, z = None, labels = False):
		# x = [xy[0] for xy in self.coords.values()]
		# y = [xy[1] for xy in self.coords.values()]
		# xy = [rotate(x[i], y[i], theta = math.pi / 2) for i in range(len(x))]
		# coordsfood = [self.coords[i] for i in self.food]
		coordsfood = [self.xy[i] for i in self.food]
		# xyfood = [[rotate(x[0], x[1], theta= math.pi / 2) for x in coordsfood[:6]],
		# 	 [rotate(x[0], x[1], theta= math.pi / 2) for x in coordsfood[6:]]]
		xyfood = [coordsfood[:6],coordsfood[6:]]
		plt.fill([x[0] for x in xyfood[0]], [x[1] for x in xyfood[0]], c = 'grey')
		plt.fill([x[0] for x in xyfood[1]], [x[1] for x in xyfood[1]], c = 'grey')

		if z is None:

			# plt.scatter([x[0] for x in xy], [x[1] for x in xy])
			plt.scatter([x[0] for x in self.xy.values()], [x[1] for x in self.xy.values()])

		else:
			# plt.scatter([x[0] for x in xy], [x[1] for x in xy], c = z, cmap = 'coolwarm')
			plt.scatter([x[0] for x in self.xy.values()], [x[1] for x in self.xy.values()], c = z, cmap = 'coolwarm')
   
		if labels:
			v = list(self.xy.values())
			for i, txt in enumerate(self.coords.keys()):
				plt.annotate(txt, v[i])
		# xynest = rotate(self.coords[nest][0], self.coords[nest][1], math.pi / 2)
		# plt.scatter(xynest[0], 0, marker = '^', s = 50, c = 'black')
		plt.scatter(self.xy[nest][0], self.xy[nest][1], marker = '^', s = 50, c = 'black')
		plt.show()
  
	def plot_trajectory(self, id):

		coordsfood = [self.xy[i] for i in self.food]
		xyfood = [coordsfood[:6],coordsfood[6:]]
		plt.fill([x[0] for x in xyfood[0]], [x[1] for x in xyfood[0]], c = 'grey')
		plt.fill([x[0] for x in xyfood[1]], [x[1] for x in xyfood[1]], c = 'grey')
  
		xy = [self.xy[i] for i in self.agents[id].path]
		plt.scatter([x[0] for x in xy], [x[1] for x in xy], alpha = 1, c = list(range(len(xy))),cmap = 'viridis', zorder = 2)
  
		e = list(self.g.edges)
		for i in e:
			coords = self.xy[i[0]], self.xy[i[1]]
			x = coords[0][0], coords[1][0]
			y = coords[0][1], coords[1][1]
			# plt.plot(x, y, linewidth = 3, c = '#4D4D4D')
			plt.plot(x, y, linewidth = 3, c = '#999999', zorder = 1)
   


		plt.scatter(self.xy[nest][0], self.xy[nest][1], marker = '^', s = 50, c = 'black')
		plt.show()
  
  
	def plot_N(self):

		t2min = 60
		v = self.N
		t = np.array(self.T) / t2min
		plt.plot(t, v)

		if 0 in list(food.values()):

			times = list(filter(lambda i: i[0].is_collected, self.food.values()))

			minv = np.min([i[0].collection_time for i in times]) / t2min
			maxv = np.max([i[0].collection_time for i in times]) / t2min

		else:
			minv = np.nan
			maxv = np.nan

		plt.axvline(x = minv, ymin = 0, ymax = np.max(self.N), color = 'midnightblue', ls = '--')
		plt.axvline(x = maxv, ymin = 0, ymax = np.max(self.N), color = 'midnightblue', ls = '--')
		plt.xlabel('Time (min)')
		plt.ylabel('Number of active ants')
		plt.xticks(list(range(0, 185, 15)))
		plt.show()
  
	# def multiplot(self):
		
	# 	fig, axs = plt.subplots(2, 2)

	# 	t2min = 120
	# 	v = discretize_time(self.N, self.T)
	# 	t = np.array(list(range(len(v)))) / t2min
	# 	plt.plot(t, v)

	# 	if 0 in list(food.values()):

	# 		times = list(filter(lambda i: i[0].is_collected, self.food.values()))

	# 		minv = np.min([i[0].collection_time for i in times]) / t2min
	# 		maxv = np.max([i[0].collection_time for i in times]) / t2min

	# 	else:
	# 		minv = np.nan
	# 		maxv = np.nan

	# 	plt.axvline(x = minv, ymin = 0, ymax = np.max(self.N), color = 'midnightblue', ls = '--')
	# 	plt.axvline(x = maxv, ymin = 0, ymax = np.max(self.N), color = 'midnightblue', ls = '--')
	# 	plt.xlabel('Time (min)')
	# 	plt.ylabel('Number of active ants')
	# 	plt.xticks(list(range(0, 185, 15)))
	# 	plt.show()

	def plot_I(self):
		i = moving_average(discretize_time(self.I, self.T, solve = 0), t = 60, overlap = 30)
		plt.plot(np.array(list(range(len(i)))) / 60, i)
		plt.xlabel('Time (min)')
		plt.ylabel('Interactions')
		plt.xticks(list(range(0, 185, 15)))
		plt.show()
  
	def plot_cumI(self):
		plt.plot(np.array(self.T) / 60, np.cumsum(self.I))
		plt.xlabel('Time (min)')
		plt.ylabel('Cumulated interactions')
		plt.xticks(list(range(0, 185, 15)))

	def depart_entry_correlation(self):

		if not hasattr(self, 'dpt_ent'):

			dpt = [1 if i > 0 else 0 for i in self.C]
			ent = [1 if i < 0 else 0 for i in self.C]

			dpt_disc = discretize_time(dpt, self.T, solve = 0)
			ent_disc = discretize_time(ent, self.T, solve = 0)

			dpt_ma = moving_average(dpt_disc, t = 30, overlap = 15)
			ent_ma = moving_average(ent_disc, t = 30, overlap = 15)

			dpt_ma = [i if i < 1 else 0 for i in dpt_ma]
			ent_ma = [i if i < 1 else 0 for i in ent_ma]

			R = pearsonr(dpt_ma, ent_ma)

			self.dpt_ent = {'dpt': dpt_ma, 'ent': ent_ma, 'R': R[0], 'pvalue': R[1]}

		else:

			dpt_ma = self.dpt_ent['dpt']
			ent_ma = self.dpt_ent['ent']
			R = [self.dpt_ent['R']]

		print('R = %s' % round(R[0], 3))
		plt.scatter(dpt_ma, ent_ma)
		plt.xlabel('Nest departures')
		plt.ylabel('Nest entries')
		plt.show()
  
class Food:
    
	def __init__(self, pos):
		self.state = '1'
		# self.state = '2'
		self.Si = 1 # Interactions
		self.initial_pos = pos
		self.is_collected = False

	def __repr__(self):
		if self.is_collected:
			t = self.collection_time /60
			t = (int(t), round((t - int(t)) * 60))
			msg = 'Food collected at %s minutes and %s seconds' % t
		else:
			msg = 'Food not collected yet!!'

		return msg

	def collected(self, time):
		self.collection_time = time
		self.is_collected = True