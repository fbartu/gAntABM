import networkx as nx
from mesa import space, Agent, Model
import math
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from functions import *
from scipy.stats import pearsonr
# from copy import deepcopy

""""""""""""""""""
""" PARAMETERS """
""""""""""""""""""
N = 100 # number of automata
fact = N
alpha = 0.5 / N # expected average of a random uniform U(0, 1)
beta = 1 / 4
gamma = beta# alpha # handling time
Theta = 0 # threshold
theta = 10**-15 # threshold of activity (inactive if Activity < theta)
Interactions = 4 # integer
weight = 4 # must be an integer equal or greater than 1

orientation = {'up-right': 1, 'up-left': -1,'up-down': 0,
               'down-right': -1, 'down-left':1, 'down-up':0,
               'right-right': 1, 'right-left': 0, 'right-up': -1}

mot_matrix = {1: [0.4377143, 0.2817919, 0.2804938],
              0: [0.4825561, 0.2051468, 0.3122971],
              -1: [0.2376265, 0.2802202, 0.4821533]}

# Coupling coefficients
# 1: No info, 2: Indirect info, 3: Direct info
Jij = {'0-0': 0.75, '0-1': 1, '0-2': 2, '0-3': 3,
        '1-0': 0.5, '1-1': 0.75, '1-2': 1, '1-3': 2,
	   '2-0': 0.25, '2-1': 0.5, '2-2': 0.75, '2-3': 1,
	   '3-0': 0, '3-1': 0.25, '3-2': 0.5, '3-3': 0.75}

# 1: No info, 2: Indirect info, 3: Direct info
Jij = {'1-1': 0.75, '1-2': 2, '1-3': 5,
	   '2-1': 0.3, '2-2': 0.75, '2-3': 2,
	   '3-1': 0.1, '3-2': 0.3, '3-3': 0.75}

# Jij = {'1-1': 0.1, '1-2': 1, '1-3': 2,
# 	   '2-1': 0.05, '2-2': 0.1, '2-3': 1,
# 	   '3-1': 0, '3-2': 0.05, '3-3': 0.1}

# Jij = {'1-1': 0.5, '1-2': 1.5, '1-3': 2,
# 	   '2-1': 0.25, '2-2': 0.5, '2-3': 1.5,
# 	   '3-1': 0.1, '3-2': 0.25, '3-3': 0.5}


# REFERENCE MATRIX, WORKS "KIND OF"
Jij = {'0-0': 0.6, '0-1': 10**2, '0-2': 10**5, '0-3': 10**10,
		'1-0': 0.25, '1-1': 0.6, '1-2': 10**2, '1-3': 10**5,
	   '2-0': 0.25, '2-1': 0.5, '2-2': 0.6, '2-3': 10**2,
	   '3-0': 0.25, '3-1': 0.5, '3-2': 0.5, '3-3': 0.6}

# nest coords
nest = (0, 22)
nest_influence = [nest, (1, 21), (1, 22), (1, 23)]

food_positions = [(6, 33), (6, 34), (7, 34), # patch 1
	(7, 33), (7, 32), (6, 32),
	(6, 11), (6, 12), (7, 12), # patch 2
	(7, 11), (7, 10), (6, 10)]
foodXvertex = 1

food = dict.fromkeys(food_positions, foodXvertex)

#Lattice size
width    = 22
height   = 13

'''FOOD'''

class Food:
	def __init__(self, pos):
		self.state = '3'
		# self.is_active = True
		self.Si = 1 # Interactions
		# self.Si_t1 = self.Si
		self.initial_pos = pos
		# self.rate = 0
		self.is_collected = False

	def __repr__(self):
		if self.is_collected:
			# t = self.collection_time / 120
			t = self.collection_time /60
			t = (int(t), round((t - int(t)) * 60))

			msg = 'Food collected at %s minutes and %s seconds' % t

		else:
			msg = 'Food not collected yet!!'

		return msg

	def collected(self, time):
		self.collection_time = time
		self.is_collected = True

''' ANT AGENT '''
class Ant(Agent):

	def __init__(self, unique_id, model):

		super().__init__(unique_id, model)

		self.Si = np.random.uniform(-1.0, 1.0)# np.random.normal(0.5, 0.2)
		self.g = np.random.normal(0.6, 0.2)
		# self.theta = np.random.uniform(10**-10, 10**-20)
		self.history = 0

		self.is_active = False
		self.state = '0'
		# self.state = '1'
  
		self.food = []

		self.pos = 'nest'
		self.movement = 'random'

	# Move method
	def move(self):
		self.history += 1

		possible_steps = self.model.grid.get_neighbors(
		self.pos,
		include_center = False)
  
		l = list(range(len(possible_steps)))

		if self.movement == 'random':
			
			if self.pos == nest:
				idx = np.random.choice([0, 'nest'], p = [0.9, 0.1])

				if idx == 'nest':
					self.enter_nest()
					return None
		
				else:
					idx = int(idx)
     
			else:
				idx = np.random.choice(l)
      
			# if hasattr(self, 'last_move'):
			# 	pass

			# 	if self.last_move == 'up':
			# 		idx = np.random.choice(list(range(len(possible_steps))))

			# 	else:
        
			# else:
       
				# idx = np.random.choice(list(range(len(possible_steps))))
				# self.last_move = 'up'    

		else:
			d = [dist(self.target, self.model.coords[i]) for i in possible_steps]
			idx = np.argmin(d)

			v = 1 / (len(d) + weight - 1)
			p = [weight / (len(d) + weight - 1) if i == idx else v for i in l]
			idx = np.random.choice(l, p = p)

		pos = possible_steps[idx]
		self.model.grid.move_agent(self, pos)

	def find_neighbors(self):

		if self.pos == 'nest':
			l = len(self.model.in_nest)

			if l > Interactions:

				alist = list(filter(lambda a: a.unique_id in self.model.in_nest and
					a.unique_id != self.unique_id,
					list(self.model.agents.values())))

				neighbors = np.random.choice(alist, size = np.random.choice(list(range(Interactions))), replace = False)

			elif l > 1:
				alist = list(filter(lambda a: a.unique_id in self.model.in_nest and
				a.unique_id != self.unique_id,
				list(self.model.agents.values())))

				neighbors = np.random.choice(alist, size = np.random.choice(list(range(l - 1))), replace = False)
			else:
				neighbors = []

		else:
			neighbors = self.model.grid.get_cell_list_contents([self.pos])

			if len(neighbors):
				neighbors = list(filter(lambda a: a.unique_id != self.unique_id, neighbors))
				# neighbors = list(filter(lambda a: a.unique_id != self.unique_id and a.unique_id > -1, neighbors))
				if len(neighbors) > Interactions:
					neighbors = np.random.choice(neighbors, size = Interactions, replace = False)

		return neighbors

	def interaction(self):
		neighbors = self.find_neighbors()

		# g = [] # gain
		s = [] # state
		z = [] # activity
  
		l = len(neighbors)
		if l:
			for i in neighbors:
				# g.append(i.g)
				s.append(i.state)
				z.append(Jij[self.state + "-" + i.state]* i.Si - Theta)

			z = sum(z)
   
			if self.pos in ['nest'] + nest_influence:
				self.model.I.append(+1)
			else:
				self.model.I.append(0)
    
		else:
			z = -Theta
			self.model.I.append(0)


  
		# prev_Si = self.Si
		self.Si = math.tanh(self.g * (z + self.Si * Jij[self.state + "-" + self.state]) ) # update activity
		# self.model.update_alpha(self.Si - prev_Si)

		# self.Si = math.tanh(self.g * (z + self.Si) ) # update activity
		# self.g = np.mean(g + [self.g]) # update gain
		self.update_role(s) # update state

	# tambe podria fer-ho tirant una moneda: 50/50 de canviar o seguir igual
	def update_role(self, states):
		if self.state != '3':
		# if self.state == '3' or sum(food) > 0:
		# 	self.state = '3'
			if self.state == '1' and '2' in states:
				self.state = '2'
			elif '3' in states:
				self.state = '2'

	# def update_rate(self):
	# 	self.rate = beta
		# self.rate = abs(self.Si)
		# self.rate = self.g
  
	# def update_model_alpha(self, alpha):
	# 	self.model.alpha += (alpha) / fact

	def report_info(self):
		neighbors = self.find_neighbors()
		for i in neighbors:
			state = i.state + "-" + self.state
			Si = i.Si
			i.Si = math.tanh(i.g * (i.Si + Jij[state] * self.Si))
			# self.model.update_alpha(i.Si - Si)
			
			# i.Si = math.tanh(i.g * np.mean([i.Si, Jij[i.state + "-" + self.state] * self.Si]))
			# i.Si = math.tanh(i.g * Jij[i.state + "-" + self.state] * self.Si)
			# self.model.r[i.unique_id] = rate
			# i.rate = rate

	# def report(self):
	# 	if self.Si > theta:
	# 		neighbors = self.find_neighbors()
	# 		for i in neighbors:
	# 			rate = math.tanh(i.g * (i.Si + Jij[i.state + "-" + self.state] * self.Si))
	# 			self.model.r[i.unique_id] = rate
	# 			i.rate = rate

	def report_exit(self):
		self.model.S[0] -= 1
		self.model.S[1] += 1
		self.model.out.append(self.unique_id)
		self.model.in_nest.remove(self.unique_id)
		self.model.C.append(+1)

	def report_entry(self):
		self.model.S[0] += 1
		self.model.S[1] -= 1
		self.model.out.remove(self.unique_id)
		self.model.in_nest.append(self.unique_id)
		self.model.C.append(-1)

	def leave_nest(self):
		self.model.grid.place_agent(self, nest)
		self.is_active = True
		# self.model.in_nest.remove(self.unique_id)
		if self.state == '0':
			self.state = '1'
		# self.rate = beta
		self.report_exit()

	def enter_nest(self):
		self.model.remove_agent(self)
		self.is_active = False
		# self.model.in_nest.append(self.unique_id)
		self.pos = 'nest'
		self.ant2explore()
		self.report_info()
		self.report_entry()
		self.rate = self.model.alpha

	def ant2nest(self):
		self.target = self.model.coords[nest]
		self.movement = 'persistant'
		# self.rate = beta

	def ant2explore(self):
		if hasattr(self, 'target'):
			del self.target
		self.movement = 'random'

	def pick_food(self):
		self.model.remove_agent(self.model.food[self.pos][0])
		self.food.append(self.model.food[self.pos].pop(0))
		self.model.food[self.pos].extend(self.food)
		self.model.food[self.pos][-1].collected(self.model.time)
		food[self.pos] -= 1
		self.food_location = self.pos
		# self.rate = gamma
		self.state = '3'
		# self.model.info += 1

	def drop_food(self):
		# self.model.in_nest.append(self.food.pop())
		# self.model.food_in_nest += 1
		self.food.pop() # possibilitat de que el food actui dins el nest (com a estat '3')

	def action(self):
		if self.is_active: # in arena
			if len(self.food) or self.Si < theta:
			# if len(self.food) or self.Si < self.theta:
				self.ant2nest()

			if self.pos == nest:
				if hasattr(self, 'target') and self.target == self.model.coords[nest]:
					self.enter_nest()

				else:
					self.move()

			elif self.pos in food_positions:
				if food[self.pos] > 0 and not len(self.food):
					self.pick_food()

				else:
					self.move()

			else:
				self.move()

		else:
      
			# if self.state == '3':

			if len(self.food):
				self.drop_food()
     
				# self.report_info()
    
				# if np.random.uniform(0.0, 1.0) > self.Si:
				# 	self.state = '2'

			else:
				# if self.Si > self.theta:
				if self.Si > theta:
					self.leave_nest()


		self.interaction()
		# self.history.append(+1)


''' MODEL '''
class Model(Model):

	def __init__(self, N = N, width = width, height = height):

		super().__init__()

		nds = [(0, i) for i in range(1, 44, 2)]

		# Lattice
		self.g = nx.hexagonal_lattice_graph(width, height, periodic = False)
		[self.g.remove_node(i) for i in nds]
		self.coords = nx.get_node_attributes(self.g, 'pos')
		self.grid = space.NetworkGrid(self.g)

  
		# Agents
		self.agents = {}
		self.ids = list(range(N))
		for i in range(N):
			self.agents[i] = Ant(i, self)
   
		# states & rates
		self.in_nest = list(range(N))
		self.out = []
		self.S = np.array([N, 0])
		# self.alpha = abs(np.mean([self.agents[i].Si for i in self.agents])) / 10# / fact
		self.alpha = 0.005
		self.beta = 2 # 1/2
		# self.info = 0
    
		self.Si = [0]

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

		# Rates
		self.update_rates()
		self.rate2prob()

		# Time & Gillespie
		self.time = 0
		self.sample_time()

		# Metrics
		self.T = [0] # time
		self.N = [0] # population
		self.Nexp = [0]
		self.I = [0] # interactions
		self.C = [0] # alpha ~ nest departures and entries
		self.XY = {self.T[-1]: [a.pos for a in self.agents.values()]}
		self.A = [self.alpha]
		self.n = [np.mean([self.agents[i].Si for i in self.agents])]
		self.o = [0]
		self.gOut = [0]
		self.gIn = [np.mean([self.agents[i].g for i in self.agents])]
		self.iters = 0
		self.a = [self.r[0]]
		# self.df = {0: deepcopy(self.Si)}

		self.sampled_agent = []
  
	def update_rates(self):
		self.r = self.S * np.array([self.alpha, self.beta]) 
		# self.r[0] = self.alpha * N

	def rate2prob(self):
		self.R_t = np.sum(self.r)
		self.r_norm = self.r / self.R_t

	def sample_time(self):
		self.rng = np.random.random()
		self.rng_t = (1 /self.R_t) * np.log(1 / self.rng)

	# def update_beta(self, beta):
	# 	if self.o[-1] != np.nan:
	# 		self.beta = self.o[-1]
  
	def update_alpha(self, alpha):
		pass
		# self.alpha = self.n[-1]**2
		# self.alpha = abs(self.n[-1]) / 100
		# self.alpha = (1 + sum([self.agents[i].state != '1' for i in self.agents])) / 1000
		# self.alpha += alpha #/ fact
		# self.alpha = abs(self.alpha)
		# if not math.isnan(self.n[-1]):
		# 	self.alpha = abs((N * self.n[-1]) / fact)
		# else:
		# 	self.alpha = 0.0005
		# self.alpha = abs(self.alpha)

	# def update_alpha(self):
	# 	self.alpha = abs(np.mean(self.Si)/20)
		# self.alpha = abs(np.mean(self.Si) / N)
		# self.alpha = abs(np.mean(self.Si)) / (N * 20)

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
      
			process = np.random.choice(['alpha', 'beta'], p = self.r_norm)
   
			if process == 'alpha':
				id = np.random.choice(self.in_nest)
    
			else:
				id = np.random.choice(self.out)

			agent = self.agents[id]
			self.sampled_agent.append(id)

			# do action
			agent.action()
			if len(self.C) == len(self.T):
				self.C.append(0)

			# tmp_o = []
			# tmp_n = []
			# for i in self.agents:
			# 	if not self.agents[i].is_active:
			# 		self.agents[i].rate = self.alpha
			# 		tmp_n.append(self.agents[i].Si)
			# 	else:
			# 		tmp_o.append(self.agents[i].Si)
			# 	self.Si[i] = self.agents[i].Si

			# self.r[agent.unique_id] = agent.rate
			# self.update_rates()
			# self.rate2prob()
			# self.Si[agent.unique_id] = agent.Si
			# self.Si = [self.agents[i].Si for i in self.agents]

			# update activity
			# self.N.append(N - len(self.in_nest) + self.food_in_nest)


			# update time
			# self.T.append(int(self.time))

			self.A.append(self.alpha)
   
			self.N.append(len(self.out))
			self.Nexp.append(np.sum([self.agents[i].pos not in [nest, (1, 21)] for i in self.out]))


			self.XY[self.T[-1]] = [a.pos for a in self.agents.values()]
			self.n.append(np.mean([self.agents[i].Si for i in self.in_nest]))
			self.o.append(np.mean([self.agents[i].Si for i in self.out]))
			self.gIn.append(np.mean([self.agents[i].g for i in self.in_nest]))
			self.gOut.append(np.mean([self.agents[i].g for i in self.out]))


			self.update_alpha(0)
			# self.update_beta(0)
			self.update_rates()
			self.rate2prob()
   
			self.a.append(self.r[0])


			# self.df[self.T[-1]] = deepcopy(self.Si)

			self.iters += 1

			# get time for next iteration
			self.time += self.rng_t
			self.T.append(self.time)

			# get rng for next iteration
			self.sample_time()

			



	def run(self, steps = 21600):
		# for i in range(steps):
		# 	self.step(tmax = i)

		self.step(tmax = steps)

		# c = []
		# for i in self.XY:
		# 	c += self.XY[i]

		# self.z = [0 if i == nest else c.count(i) for i in self.coords]
		# self.z = [c.count(i) for i in self.coords]
		# q = np.quantile(self.z, 0.99)
		# self.z = [i if i < q else q for i in self.z]

		# self.plots()
		self.plot_N()

	def save_results(self, path):
		self.results = pd.DataFrame({'N': self.N, 'T': self.T, 'C': self.C,
                               'alpha': self.A, 'nest': self.n, 'arena': self.o})
		x = [xy[0] for xy in self.coords.values()]
		y = [xy[1] for xy in self.coords.values()]
		xy = [rotate(x[i], y[i], theta = math.pi / 2) for i in range(len(x))]
		self.xyz = pd.DataFrame({'x': [i[0] for i in xy],
						  'y': [i[1] for i in xy],
						  'z': self.z})
		self.results.to_csv(path + 'N.csv')
		self.xyz.to_csv(path + 'xyz.csv')


	def plot_lattice(self, z = None):
		x = [xy[0] for xy in self.coords.values()]
		y = [xy[1] for xy in self.coords.values()]
		xy = [rotate(x[i], y[i], theta = math.pi / 2) for i in range(len(x))]
		coordsfood = [self.coords[i] for i in self.food]
		xyfood = [[rotate(x[0], x[1], theta= math.pi / 2) for x in coordsfood[:6]],
			 [rotate(x[0], x[1], theta= math.pi / 2) for x in coordsfood[6:]]]

		plt.fill([x[0] for x in xyfood[0]], [x[1] for x in xyfood[0]], c = 'grey')
		plt.fill([x[0] for x in xyfood[1]], [x[1] for x in xyfood[1]], c = 'grey')

		if z is None:

			plt.scatter([x[0] for x in xy], [x[1] for x in xy])

		else:
			plt.scatter([x[0] for x in xy], [x[1] for x in xy], c = z, cmap = 'coolwarm')
		xynest = rotate(self.coords[nest][0], self.coords[nest][1], math.pi / 2)
		plt.scatter(xynest[0], 0, marker = '^', s = 50, c = 'black')
		plt.show()

	def plot_N(self):

		t2min = 60
		# t2min = 120
		# v = discretize_time(self.N, self.T)
		v = self.N
		t = np.array(self.T) / t2min
		# t = np.array(list(range(len(v)))) / t2min
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
  
	def multiplot(self):
		
		fig, axs = plt.subplots(2, 2)


     
		t2min = 120
		v = discretize_time(self.N, self.T)
		t = np.array(list(range(len(v)))) / t2min
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

	def plot_I(self):
		plt.plot(self.T, self.I)
		plt.show()

	def plots(self):
		self.plot_N()
		self.plot_lattice(self.z)

	def depart_entry_correlation(self):

		if not hasattr(self, 'dpt_ent'):

			# diff = np.diff(self.N)

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
			R = (self.dpt_ent['R'])

		print('R = %s' % round(R[0], 3))
		plt.scatter(dpt_ma, ent_ma)
		plt.xlabel('Nest departures')
		plt.ylabel('Nest entries')
		plt.show()