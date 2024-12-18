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
N = 100 # number of automata
alpha = 0.0015 # rate of action in nest
beta = 1 # rate of action in arena
p = 0.1 # probability of changing state
Theta = 10**-15 # baseline loss of activity (threshold 1)
theta = 0 # threshold of activity (threshold 2)
Interactions = 4 # integer, number of max interactions in a node
weight = 3 # integer >= 1, direction bias

# Coupling coefficients
# 0 - No info; 1 - Info
Jij = {'0-0': 1, '0-1': 10**5,
       '1-0': 0.5, '1-1': 0.5}

""""""""""""""""""""""""""
""" SPATIAL PARAMETERS """
""""""""""""""""""""""""""
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


""""""""""""""""""
"""   CLASSES  """
""""""""""""""""""

''' ANT AGENT '''
class Ant(Agent):

	def __init__(self, unique_id, model):

		super().__init__(unique_id, model)

		self.Si = np.random.normal(0.0, 0.2)# np.random.uniform(-1.0, 1.0) 
		self.g = np.random.normal(0.8, 0.1)
		# self.theta = np.random.uniform(10**-10, 10**-20)
		self.history = 0

		self.is_active = False
		self.state = '0'
  
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
				idx = np.random.choice([0, 'nest'], p = [2/3, 1/3])

				if idx == 'nest':
					self.enter_nest()
					return None
		
				else:
					idx = int(idx)
     
			else:
				idx = np.random.choice(l)
      
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
				if len(neighbors) > Interactions:
					neighbors = np.random.choice(neighbors, size = Interactions, replace = False)

		return neighbors

	def interaction(self):
		neighbors = self.find_neighbors()

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

		self.Si = math.tanh(self.g * (z + self.Si * Jij[self.state + "-" + self.state]) ) # update activity
		self.update_role(s) # update state

	def update_role(self, states):
		if '1' in states:
			if np.random.random() < p:
				self.state = '1'
 
	def report_info(self):
		neighbors = self.find_neighbors()
		for i in neighbors:
			state = i.state + "-" + self.state
			i.Si = math.tanh(i.g * (i.Si * Jij[i.state + "-" + i.state] + (Jij[state] * self.Si - Theta)))
   
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
		self.report_exit()

	def enter_nest(self):
		self.model.remove_agent(self)
		self.is_active = False
		self.pos = 'nest'
		self.ant2explore()
		self.report_info()
		self.report_entry()

	def ant2nest(self):
		self.target = self.model.coords[nest]
		self.movement = 'persistant'

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
		self.state = '1'
  
	def eval_status(self):
		if hasattr(self, 'target') and not len(self.food):
			del self.target
			self.movement = 'random'

	def drop_food(self):
		self.food.pop()

	def action(self):
		if self.is_active: # in arena
			if len(self.food) or self.Si < theta:
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
      
			if len(self.food):
				self.drop_food()
     
			else:
				if self.Si > theta:
					self.leave_nest()


		self.interaction()
		# self.eval_status()

''' MODEL '''
class Model(Model):

	def __init__(self, alpha = alpha, beta = beta, N = N, width = width, height = height):

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
		self.S = np.array([N, 0])
		self.alpha = alpha
		self.beta = beta
  
		self.in_nest = list(range(N))
		self.out = []
    
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
   
		self.init_state = {'Si': [self.agents[i].Si for i in self.agents],
                     'g': [self.agents[i].g for i in self.agents],
                     'food': len(self.food), 'alpha': self.alpha, 'beta':self.beta,
                     'N': N}

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
		self.alpha_counter = 0
		self.beta_counter = 0

		self.sampled_agent = []
  
	def update_rates(self):
		self.r = self.S * np.array([self.alpha, self.beta]) 

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
      
			process = np.random.choice(['alpha', 'beta'], p = self.r_norm)
   
			if process == 'alpha':
				id = np.random.choice(self.in_nest)
				self.alpha_counter += 1
    
			else:
				id = np.random.choice(self.out)
				self.beta_counter += 1

			agent = self.agents[id]
			self.sampled_agent.append(id)

			# do action
			agent.action()
			if len(self.C) == len(self.T):
				self.C.append(0)

			self.A.append(self.alpha)
   
			self.N.append(len(self.out))
			self.Nexp.append(np.sum([self.agents[i].pos not in [nest, (1, 21)] for i in self.out]))


			self.XY[self.T[-1]] = [a.pos for a in self.agents.values()]
			self.n.append(np.mean([self.agents[i].Si for i in self.in_nest]))
			self.o.append(np.mean([self.agents[i].Si for i in self.out]))
			self.gIn.append(np.mean([self.agents[i].g for i in self.in_nest]))
			self.gOut.append(np.mean([self.agents[i].g for i in self.out]))
   
			self.update_rates()
			self.rate2prob()
   
			self.a.append(self.r[0])

			self.iters += 1

			# get time for next iteration
			self.time += self.rng_t
			self.T.append(self.time)

			# get rng for next iteration
			self.sample_time()

			
	def run(self, tmax = 10800):

		self.step(tmax = tmax)
		self.plot_N()

	def save_results(self, path):
		self.results = pd.DataFrame({'N': self.N, 'T': self.T, 'I':self.I, 'C': self.C,
                               'nest': self.n, 'arena': self.o})
		self.results['F'] = 0
		self.results.iloc[np.where([self.T == x for x in [self.food[i][0].collection_time for i in self.food]])[1],-1] = 1
		self.results.to_csv(path + 'N.csv')

	# def plot_lattice(self, z = None):
	# 	x = [xy[0] for xy in self.coords.values()]
	# 	y = [xy[1] for xy in self.coords.values()]
	# 	xy = [rotate(x[i], y[i], theta = math.pi / 2) for i in range(len(x))]
	# 	coordsfood = [self.coords[i] for i in self.food]
	# 	xyfood = [[rotate(x[0], x[1], theta= math.pi / 2) for x in coordsfood[:6]],
	# 		 [rotate(x[0], x[1], theta= math.pi / 2) for x in coordsfood[6:]]]

	# 	plt.fill([x[0] for x in xyfood[0]], [x[1] for x in xyfood[0]], c = 'grey')
	# 	plt.fill([x[0] for x in xyfood[1]], [x[1] for x in xyfood[1]], c = 'grey')

	# 	if z is None:

	# 		plt.scatter([x[0] for x in xy], [x[1] for x in xy])

	# 	else:
	# 		plt.scatter([x[0] for x in xy], [x[1] for x in xy], c = z, cmap = 'coolwarm')
	# 	xynest = rotate(self.coords[nest][0], self.coords[nest][1], math.pi / 2)
	# 	plt.scatter(xynest[0], 0, marker = '^', s = 50, c = 'black')
	# 	plt.show()

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