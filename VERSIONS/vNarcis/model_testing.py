import random
import networkx as nx
from mesa import space, Agent, Model
import math
import random
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import distance

""""""""""""""""""
""" PARAMETERS """
""""""""""""""""""
N = 100 # number of automata
g = 1 # gain (sensitivity) parameter
Theta = 0.1
theta = 10**-16 # threshold of activity (inactive if Activity < theta) 
Sa = 0.1 # spontaneous activation activity
Pa = 0.01 # probability of spontaneous activation

Jij = {'Active-Active': 1, 'Active-Inactive' : 1,
 'Inactive-Active': 1, 'Inactive-Inactive': 1, 
 'Active-FoodActive': 1, 'Active-FoodInactive': 1,
 'Inactive-FoodActive': 1, 'Inactive-FoodInactive': 1} # Coupling coefficients

weight = 3 # number of times it is more likely to choose the preferred direction over the other possibilities

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

''' ANT AGENT '''


alpha = 0.0005 # N / 2e5 
beta = 1 # N / 80
phi = 0.05

class Ant(Agent):
	
	def __init__(self, unique_id, model):
		
		super().__init__(unique_id, model)
  
		self.rate = alpha
		self.Si = 0
		self.history = 0
		self.is_active = False
		
			
   
	def back2nest(self):
		pass
	# Possible actions the ant may take
	def action(self):
		if self.is_active:

			if self.Si < theta:
				self.back2nest()
		else:
			pass
	# def action(self):
     
	# 	if self.is_active:
     
	# 		if random.random() < phi:
	# 			self.Si += self.history
	# 			if self.Si < 0:
	# 				self.Si = alpha
	# 			self.is_active = False
	# 			self.rate = self.Si
	# 			if  self.model.time > 5000 and self.model.time < 15000:
        
	# 				self.interaction()

	# 		else:
	# 			self.Si = math.tanh(self.Si)
	# 			self.history += random.uniform(-0.01, 0.01)# random.random() * random.choice([1, -1])
	# 	else:
	# 		if self.Si < 0:
	# 			self.Si = alpha
	# 		else:
	# 			self.is_active = True
	# 			self.rate = beta

	def interaction(self):
		alist = list(filter(lambda a: a.is_active == False, self.model.agents))
		a = np.random.choice(alist, size = 3, replace = False)
		id = [i.unique_id for i in a]
		ids = [i.unique_id for i in self.model.agents]
		for i in self.model.agents:
			if i.unique_id in id:
				i.Si += self.history - Theta
				if i.Si < 0:
					i.rate = alpha
				else:   
					i.rate = i.Si
     
				self.model.r[i.unique_id] = i.rate
		


''' MODEL '''

class Model(Model):

	def __init__(self, N = N, width = width, height = height):

		super().__init__()

		# Lattice
		self.g = nx.hexagonal_lattice_graph(width, height, periodic = False)
		self.grid = space.NetworkGrid(self.g)
		self.coords = nx.get_node_attributes(self.g, 'pos')

		# Agents
		self.agents = []

		for i in range(N):
			self.agents.append(Ant(i, self))
			self.grid.place_agent(self.agents[-1], nest)

		
		# Rates
		self.r = np.array([alpha] * N)
		self.rate2prob()

		# Time & Gillespie
		self.time = 0
		self.sample_time()


		# Metrics
		self.T = [0] # time
		self.N = [0]
		self.iters = 0
  
	def rate2prob(self):
		self.R_t = np.sum(self.r)
		self.r_norm = self.r / self.R_t
  
	def sample_time(self):
		self.rng_t = np.random.exponential(1 + 1 / np.sum(self.r))
		# self.rng_t = np.random.exponential(np.sum(self.r))

	def remove_agent(self, agent: Agent) -> None:
		""" Remove the agent from the network and set its pos variable to None. """
		pos = agent.pos
		self._remove_agent(agent, pos)
		agent.pos = None

	def _remove_agent(self, agent: Agent, node_id: int) -> None:
		""" Remove an agent from a node. """

		self.g.nodes[node_id]["agent"].remove(agent)
 
	def step(self):
			
		idx = int(np.random.choice(list(range(len(self.agents))), 1, p = self.r_norm)) 

		# do action & report interactions
		self.agents[idx].action()

		# update activity
		self.N.append(len(list(filter(lambda a: a.is_active == True, self.agents))))
		
		self.r[idx] = self.agents[idx].rate
   
		self.rate2prob()
	
		# update time
		self.T.append(self.time)

		# get time for next iteration
		self.time += self.rng_t

		# get rng for next iteration
		self.sample_time()

		self.iters += 1

	def run(self, steps = 21600):
		for i in range(steps):
			self.step()

   
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
  
	def plot_N(self):
		plt.plot(self.T, self.N)
		plt.show()
  
	def plots(self):
		self.plot_N()
		# self.plot_lattice(self.z)