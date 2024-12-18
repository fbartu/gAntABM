import random
import networkx as nx
from mesa import space, Agent, Model #, datacollection
import json
import math
import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import distance
# from copy import deepcopy
# from scipy.stats import rv_discrete
import statistics

# from networkx.algorithms.cluster import square_clustering
# import params

""""""""""""""""""
""" PARAMETERS """
""""""""""""""""""
N = 100 # number of automata
g = 1 # gain (sensitivity) parameter
Theta = 0
theta = 10**-16 # threshold of activity (inactive if Activity < theta) 
Sa = 0.1 # spontaneous activation activity
Pa = 0.01 # probability of spontaneous activation
Jij = {'Active-Active': 1, 'Active-Inactive' : 0.2,
 'Inactive-Active': 0.5, 'Inactive-Inactive': 0.1, 
 'Active-FoodActive': 1, 'Active-FoodInactive': -1,
 'Inactive-FoodActive': 1, 'Inactive-FoodInactive': 0} # Coupling coefficients

Jij = {'Active-Active': 1, 'Active-Inactive' : 1,
 'Inactive-Active': 1, 'Inactive-Inactive': 1, 
 'Active-FoodActive': 1, 'Active-FoodInactive': 1,
 'Inactive-FoodActive': 1, 'Inactive-FoodInactive': 1} # Coupling coefficients
weight = 2 # number of times it is more likely to choose the preferred direction over the other possibilities

nest = (0,22)
food_positions = [(6, 33), (6, 34), (7, 34), # patch 1
	(7, 33), (7, 32), (6, 32),
	(6, 11), (6, 12), (7, 12), # patch 2
	(7, 11), (7, 10), (6, 10)]
foodXvertex = 1

food = dict.fromkeys(food_positions, foodXvertex)

#Lattice size
width    = 22   
height   = 13 

# Si_t+1 = tanh { g [ sum(Jij * Sj_t-1) + Jii * Si_t-1 ] }
# Si_t1 = Phi * ( g * ( Jii * Si_t + np.sum( Jij * Sj_t - Theta_i ) ) ) # // STATE FUNCTION

""""""""""""""""""
""""""""""""""""""

""""""""""""""""""
""" FUNCTIONS  """
""""""""""""""""""

def dist(origin, target):
	return distance.euclidean(origin, target)


def rotate(x, y, theta = math.pi / 2):
	x1 = round(x * math.cos(theta) - y * math.sin(theta), 2)
	y1 = round(x * math.sin(theta) + y * math.cos(theta), 2)
	return x1, y1


""""""""""""""#
""" CLASSES """
""""""""""""""#

''' FOOD '''

class Food:
	def __init__(self):
		self.state = 'FoodInactive'
		self.Si = 1
		self.Si_t1 = self.Si
		self.unique_id = -1

	def compute_activity(self):
		pass

''' ANT AGENT '''

class Ant(Agent):
	
	def __init__(self, unique_id, model):
		
		super().__init__(unique_id, model)

		# self.Si = random.gauss(0, 1) # activity
		# self.Si = random.uniform(-1.0, 0.0) # activity
		self.Si = random.uniform(0, 1)
		self.Si_t1 = self.Si
		self.food = []
		
		self.check_state()
		self.movement = 'random'

	def update_activity(self):
		self.Si = self.Si_t1

	def check_state(self):
		if self.Si < theta:
			self.state = 'Inactive'
			
		else:
			self.state = 'Active'

	# Si_t+1 = tanh { g [ sum(Jij * Sj_t-1) + Jii * Si_t-1 ] }
	def compute_activity(self):
		neighbors = self.model.grid.get_cell_list_contents([self.pos])
		neighbors = list(filter(lambda a: a.unique_id != self.unique_id, neighbors))
		if len(neighbors) > 8:
			neighbors = random.sample(neighbors, random.randrange(8))
		z = [Jij[self.state+"-"+n.state] * n.Si - Theta for n in neighbors]
		z = sum(z) + Jij[self.state + "-" + self.state]* self.Si
		# self.Si_t1 = math.tanh(g * z)
		self.Si = math.tanh(g * z)
		return neighbors

	def ant2nest(self):
		self.target = self.model.coords[nest]
		self.movement = 'persistant'
  
	def ant2food(self):
		self.target = self.model.coords[random.sample(food.keys(), 1)[0]]
		self.movement = 'persistant'

	def pick_food(self):
		self.model.remove_agent(self.model.food[self.pos][0])
		self.food.append(self.model.food[self.pos].pop(0))
		self.model.food[self.pos].append(self.model.time)
		food[self.pos] -= 1

	def food2nest(self):
		self.model.grid.place_agent(self.food.pop(), self.pos)
		self.movement = 'random'
			
	# Move method
	def move(self):

		possible_steps = self.model.grid.get_neighbors(
		self.pos,
		include_center = False)

		if self.movement == 'random':
			pos = random.choice(possible_steps)

		else:
			d = [dist(self.target, self.model.coords[i]) for i in possible_steps]
			idx = np.argmin(d)

			if self.movement == 'persistant':
				v = 1 / (len(d) + weight - 1)
				p = [weight / (len(d) + weight - 1) if i == idx else v for i in range(len(d))]
				pos = np.random.choice(range(len(d)), p = p)
				pos = possible_steps[pos]

			else:
				pos = possible_steps[idx]

		self.model.grid.move_agent(self, pos)
			

	# Possible actions the ant may take
	def action(self):

		if self.state == 'Active':

			if self.pos in food_positions:
				if not len(self.food):
					if food[self.pos] > 0:
						# get time of retrieval?
						self.pick_food()
						self.ant2nest()

					else:
						self.move()
						# smell food ???
						# self.Si += 0.1

				else:
					self.ant2nest()
					self.move()

			elif self.pos == nest:
				
				if len(self.food):
					self.food2nest()

				else:
					self.move()

			else:
				self.move()

			# neighbors = self.compute_activity()

		else:
	
			# activate random ant in nest
			if random.random() < Pa:
				self.Si = Sa
				self.check_state()
    
			# else:
			# 	neighbors = self.compute_activity()
    
		neighbors = self.compute_activity()
		self.check_state()
    
		return neighbors


''' MODEL '''

class Model(Model):

	def __init__(self, N = N, width = width, height = height):

		super().__init__()

		# Lattice
		self.g = nx.hexagonal_lattice_graph(width, height, periodic = False)
		self.grid = space.NetworkGrid(self.g)
		self.coords = nx.get_node_attributes(self.g, 'pos')
		self.sample = []
		

		# Agents
		self.agents = []
		self.food = {}
		for i in range(N):
			self.agents.append(Ant(i, self))
			self.grid.place_agent(self.agents[-1], nest)
		for i in food:
			self.food[i] = [Food()] * foodXvertex
			for f in range(foodXvertex):
				self.grid.place_agent(self.food[i][f], i)

		# idx = random.randrange(N)
		# self.agents[idx].Si = 30 # ON PARAMETRIZATION !
		# self.agents[idx].check_state()
		
		# Rates
		# self.r = np.array([a.Si for a in self.agents])
		self.r = np.array([0.05] * N)
		# self.r = np.array([abs(a.Si) for a in self.agents])
		self.rate2prob()

		# Time & Gillespie
		self.time = 0
		self.sample_time()
		# self.rng_t = random.random()


		# Metrics
		self.T = [0] # time
		self.I = [0] # interactions
		self.N = [0] # 
		self.A = [self.active_agents()] # activity
		self.XY = {self.T[-1]: [a.pos for a in self.agents]}
		self.iters = 0
  
		self.dict = {self.T[-1]: [a.Si for a in self.agents]}
  
	def active_agents(self):
		return sum([a.state == 'Active' for a in self.agents]) / len(self.agents)
  
	def rate2prob(self):
		self.R_t = np.sum(self.r)
		self.r_norm = self.r / self.R_t
  
	def sample_time(self):
		self.rng_t = np.random.exponential(1 + 1 / np.sum(self.r))
		# self.rng_t = np.random.exponential(np.sum(self.r))

	# transforms rates into probabilities
	# def rate2prob(self):
	# 	m = np.min(self.r)

	# 	# normalization to only positive values if necessary
	# 	if m < 0:
	# 		self.R_t = np.sum(self.r + abs(m))
	# 		self.r_norm = (self.r + abs(m)) / self.R_t
	# 	else:
	# 		self.R_t = np.sum(self.r)
	# 		self.r_norm = self.r / self.R_t

	def remove_agent(self, agent: Agent) -> None:
		""" Remove the agent from the network and set its pos variable to None. """
		pos = agent.pos
		self._remove_agent(agent, pos)
		agent.pos = None

	def _remove_agent(self, agent: Agent, node_id: int) -> None:
		""" Remove an agent from a node. """

		self.g.nodes[node_id]["agent"].remove(agent)

	# def step(self, time):
		
	# 	while self.time < time:
	# 		idx = int(np.random.choice(list(range(len(self.agents))), 1, p = self.r_norm))

	# 		# get sampled id (for debugging)
	# 		self.sample.append(idx) 

	# 		# do action & report interactions
	# 		interactions = self.agents[idx].action()
	# 		interactions = list(filter(lambda a: a.__class__ == Ant, interactions))


	# 		# update interactions
	# 		self.I.append(len(interactions) - 1)

	# 		# update activity
	# 		self.N.append(len(list(filter(lambda a: a.pos != nest, self.agents))))
	# 		self.A.append(self.active_agents())
			
	# 		# update rates in the model
	# 		# for i in interactions:
	# 		# 	i.compute_activity()
	# 		# 	self.r[i.unique_id] = i.Si_t1
	# 		# self.update_agents([self.agents[idx]])
	# 		self.r[idx] = abs(self.agents[idx].Si)

	# 		# self.update_agents(interactions)

	# 		self.rate2prob()
		
	# 		# update time
	# 		self.T.append(self.time)
	# 		self.dict[self.T[-1]]=  [a.Si for a in self.agents]
	# 		self.XY[self.T[-1]] = [a.pos for a in self.agents]
   
	# 		# get time for next iteration
	# 		self.time += self.rng_t

	# 		# get rng for next iteration
	# 		self.sample_time()
   
	# 		self.iters += 1
 
	def step(self):
    		
		idx = int(np.random.choice(list(range(len(self.agents))), 1, p = self.r_norm)) 

		# do action & report interactions
		interactions = self.agents[idx].action()

		# update activity
		self.N.append(len(list(filter(lambda a: a.pos != nest, self.agents))))
		self.A.append(self.active_agents())
		
		if self.agents[idx].state == 'Active':
			self.r[idx] = 1
   
		else:
			self.r[idx] = 0.05

		self.rate2prob()
	
		# update time
		self.T.append(self.time)
		self.dict[self.T[-1]]=  [a.Si for a in self.agents]
		self.XY[self.T[-1]] = [a.pos for a in self.agents]

		# get time for next iteration
		self.time += self.rng_t

		# get rng for next iteration
		self.sample_time()

		self.iters += 1



	# def update_agents(self, agents):
	# 	for a in agents:
	# 		a.update_activity()
	# 		a.check_state()

	def run(self, steps = 21600):
		for i in range(steps):
			self.step()
   
		c = []
		for i in self.XY:
			c += self.XY[i]

		self.z = [0 if i == nest else c.count(i) for i in self.coords]
  
		print('Number of iterations: %s' % self.iters)
  
		print('Food status:\n %s' % self.food)
		self.plots()

	
	# def run(self, time = list(range(10800))):
	# 	for i in time:
	# 		self.step(time = i)
   
	# 	c = []
	# 	for i in self.XY:
	# 		c += self.XY[i]

	# 	self.z = [0 if i == nest else c.count(i) for i in self.coords]
  
	# 	print('Number of iterations: %s' % self.iters)
  
	# 	print('Food status:\n %s' % self.food)
	# 	self.plots()

   
	def plot_lattice(self, z = None):
		x = [xy[0] for xy in self.coords.values()]
		y = [xy[1] for xy in self.coords.values()]
		xy = [rotate(x[i], y[i], theta = math.pi / 2) for i in range(len(x))]
  
		if z is None:
			plt.scatter([x[0] for x in xy], [x[1] for x in xy])
			plt.show()
		else:
			plt.scatter([x[0] for x in xy], [x[1] for x in xy], c = z)
			plt.show()
   
	def plot_activity(self):
		plt.plot(self.T, self.A)
		plt.show()
  
	def plot_N(self):
		plt.plot(self.T, self.N)
		plt.show()
  
	def plots(self):
		self.plot_activity()
		self.plot_N()
		self.plot_lattice(self.z)

	def retrieve_positions(self):
		# result = {'agent': [],'pos': [],'t': [], 'state': [], 'tag': [], 'mia': []}
		result = {'agent': [],'pos': [],'t': [], 'state': []}
		for i in range(len(self.agents)):
			result['agent'].extend([i] * len(self.agents[i].path))
			result['pos'].extend(self.agents[i].path)
			result['t'].extend(list(map(self.T.__getitem__, np.where(self.sample == np.array([i]))[0])))
			if len(self.agents[i].state_history) > 1:
				result['state'].extend(self.agents[i].state_history)
			#result['tag'].extend(self.agents[i].tag)
			#result['mia'].append(self.agents[i].MIA)
		
		return result
    
class Visual(Model):
	def __init__(self):
		pass
    
    

''' METRICS '''

class ParameterMetrics():

	def __init__(self, environment, pos):

		self.environment = environment
		self.pos = pos


	def interactions(self):
		unique_values = list(set(self.pos))
		counts = []
		for i in unique_values:
			x = self.pos.count(i)
			counts.append(x)

		#return sum(np.array(counts) - 1)
		return int(sum(np.array(counts) > 1))
	
	def connectivity(self):
		if len(self.pos):
			pos = list(set(self.pos)) # eliminate duplicates
			k_length = []
			branch = []
			while len(pos) > 0:
				current_path = [pos.pop(0)]
				while len(current_path):
					# get neighbors
					neighbors = np.array(self.environment.grid.get_neighbors(current_path[-1]))
					# get only the neighbors that are available in path
					idx = np.where([(n[0], n[1]) in pos for n in neighbors])
					branch.extend(list(map(tuple, neighbors[idx])))
					
					while len(branch):
						current_path.append(branch.pop(0))
						try:
							pos.remove(current_path[-1])
						except:
							next
						neighbors = np.array(self.environment.grid.get_neighbors(current_path[-1]))
						idx = np.where([(n[0], n[1]) in pos for n in neighbors])
						branch.extend(list(map(tuple, neighbors[idx])))
					
					k_length.append(len(current_path))
					current_path = []
					branch = []

			return statistics.mean(k_length)
			#return k_length
		else:
			return 0

	
	def efficiency(self, tfood):
		if not len(self.environment.food_cluster):
			self.environment.cluster_food(pos = 0) # pos has no default // need to workaround

		food_found = np.array(list(map(lambda x: x == True, tfood['Flag'])))
		
		for p in list(self.environment.food_cluster.keys()):
			patch = []

			for i in self.environment.food_cluster[p]:
				food_visited = np.array(list(map(lambda x: x == i, tfood['Pos'])))
				try:
					idx = int(np.where(np.logical_and(food_found == True, food_visited == True))[0])
					patch.append(tfood['Time'][idx])
				except:
					patch.append('Not Found')

			self.environment.food_cluster[p] = {'x': [x[0] for x in self.environment.food_cluster[p]],
			'y': [y[1] for y in self.environment.food_cluster[p]],
			 't': patch}

		return self.environment.food_cluster