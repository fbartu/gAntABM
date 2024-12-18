import random
import networkx as nx
from copy import deepcopy

from networkx.algorithms.cluster import square_clustering
import params

'''
STATES AND TAGS
'''

class State():
	
	WAITING = 'W' # waiting in nest
	EXPLORING = 'E' # exploring
	EXPLORING_FROM_FOOD = 'E2' # exploring from food patch
	RECRUITING = 'R' # recruiting or getting recruited
	EXPLORING_FOOD = 'EF' # transporting food as explorer
	RECRUITING_FOOD = 'RF' # transporting food as recruiter
	DEAD = 'D' # back to nest

class Tag():

	NAIVE = 'N' # no information about key locations
	INFORMED = 'I' # gets information when recruited by another ant

'''
ANT AGENT 
'''

class Ant():
	
	def __init__(self, unique_id, recruitment_strategy):

		# id initialization
		self.id = unique_id
		
		# Position, state and rates initialization
		self.pos = params.nest_node
		self.state = 'W'
		self.prev_state = 'W'
		self.state_history = []
		self.r_i = params.alpha
		self.movement = 'random'

		# Key locations initialization
		self.path = []
		self.path2nest = []
		self.path2food = []
		self.locations = []

		# Recruitment related
		self.recruitment_strategy = recruitment_strategy
		self.recruit, self.forage = self.choose_recruitment()
		self.recruited_ants = []

		# No information about food
		self.tag = Tag.NAIVE

		# Missing in action (lost during recruitment)
		self.MIA = 0

	# Pick the suitable recruitment method
	def choose_recruitment(cls):

		# recruitment strategies
		if 'IR' in cls.recruitment_strategy:
			m = cls.IR

		if 'HR' in cls.recruitment_strategy:
			m = cls.HR

		if 'GR' in cls.recruitment_strategy:
			m = cls.GR

		if 'F' in cls.recruitment_strategy:
			m = cls.F

		if 'm' not in locals() or 'NR' in cls.recruitment_strategy:
			m = cls.NR
		
		# serial / parallel recruitment
		if 's' in cls.recruitment_strategy:
			return m, cls.ant2nest

		else:
			return m, cls.ant2nearfood
	
	
	'''
	RECRUITMENT METHODS ARE DESCRIBED IN params.py:
	NR = 0
	IR = 1
	HR = [0, 5]
	GR = [3, 5]
	F  = X
	'''

	# One possibility is: if you don't recruit, stay in nest
	'''
	else:
		self.state = State.WAITING
		self.r_i = params.alpha
	'''

	# Individual recruitment
	def IR(self, environment, ant_pool):
		sample = random.choice(environment.waiting_ants)
		# del environment.waiting_ants[sample]
		# environment.out_nest[sample] = sample
		agent = ant_pool[sample]
		agent.r_i = params.omega
		agent.tag = Tag.INFORMED
		agent.state = State.RECRUITING
		agent.movement = '2food'
		agent.path2food = deepcopy(environment.paths2food[self.locations[-1]]) # path to where food was found
		return sample # return index of sampled ants
	
	# Hybrid recruitment
	def HR(self, environment, ant_pool):
		r = random.randrange(0, 6)
		if r > 0:
			samples = random.sample(list(environment.waiting_ants), r)
			for sample in samples:
				# del environment.waiting_ants[sample]
				# environment.out_nest[sample] = sample
				agent = ant_pool[sample]
				agent.r_i = params.omega
				agent.tag = Tag.INFORMED
				agent.state = State.RECRUITING
				agent.movement = '2food'
				agent.path2food = deepcopy(environment.paths2food[self.locations[-1]]) # path to where food was found

			return samples # return indices of sampled ants
		else:
			return []
  
	# Group recruitment
	def GR(self, environment, ant_pool):
		r = random.randrange(3, 6)
		samples = random.sample(list(environment.waiting_ants), r)
		for sample in samples:
			# del environment.waiting_ants[sample]
			# environment.out_nest[sample] = sample
			agent = ant_pool[sample]
			agent.r_i = params.omega
			agent.tag = Tag.INFORMED
			agent.state = State.RECRUITING
			agent.movement = '2food'
			agent.path2food = deepcopy(environment.paths2food[self.locations[-1]]) # path to where food was found
		return samples # return indices of sampled ants

	# Forced recruitment (of r individuals)
	def F(self, environment, ant_pool):
		r = 4 # Force a recruitment of 4 individuals
		samples = random.sample(list(environment.waiting_ants), r)
		for sample in samples:
			# del environment.waiting_ants[sample]
			# environment.out_nest[sample] = sample
			agent = ant_pool[sample]
			agent.r_i = params.omega
			agent.tag = Tag.INFORMED
			agent.state = State.RECRUITING
			agent.movement = '2food'
			agent.path2food = deepcopy(environment.paths2food[self.locations[-1]]) # path to where food was found
		return samples # return indices of sampled ants

	# No recruitment
	def NR(self):
		return []

	def ant2nest(self, environment):

		self.path2nest = nx.shortest_path(environment.G, self.pos, environment.initial_node)
		self.state = State.DEAD
		self.r_i = params.omega + params.eta # eta slightly increases the "celerity" of ants to return to nest
		self.movement = '2nest'

	def ant2explore(self, environment):

		self.state = State.EXPLORING
		self.r_i = params.omega + params.eta
		self.movement = 'random'

	def ant2nearfood(self, environment):
		if random.random() > params.phi:
			self.movement = 'local'
			self.move(environment)
		else:
			self.ant2explore(environment)

	def actualize_path(self):
		self.path.append(self.pos)

	def update_state(self):
		self.prev_state = self.state

	def leave_nest(self, environment):			
		del environment.waiting_ants[self.id]
		environment.out_nest[self.id] = self.id

	def enter_nest(self, environment):
		del environment.out_nest[self.id] 
		environment.waiting_ants[self.id] = self.id
			


	# Move method
	'''
	FUTURE MOVEMENT POSSIBILITIES TO IMPLEMENT:
	* Area restricted search : ars
	* Levy walks : levy
	* Directional persistance : dpersistance
	'''
	def move(self, environment):
		if self.movement == 'random':

			possible_steps = environment.grid.get_neighbors(
				self.pos,
				include_center = False)
			self.pos = random.choice(possible_steps)

		elif self.movement == '2nest':
			self.pos = self.path2nest.pop(0)

		elif self.movement == '2food':
			self.pos = self.path2food.pop(0)
		
		elif self.movement == 'local':
			possible_steps = environment.grid.get_neighbors(
				self.pos,
				include_center = False)
			
			is_food = list(filter(lambda x: x in environment.food.keys(), possible_steps))
			with_food = []
			for i in is_food:
				if environment.food[i] > 0:
					with_food.append(i)
				else:
					next

			if len(with_food):
				self.pos = random.choice(with_food)
			else:
				random.choice(possible_steps)
				self.ant2explore(environment)
				self.state = State.EXPLORING_FROM_FOOD

		elif self.movement == 'ars':
			pass

		elif self.movement == 'levy':
			pass

		elif self.movement == 'dpersistance':
			pass
		
		return 0

	# Possible actions the ant may take, based on the position and the state
	# returns true if food is found and picked up
	# this value is fed into the gillespie algorithm
	def action(self, environment, ant_pool):

		if self.prev_state == State.WAITING:
			self.leave_nest(environment)
			
		self.recruited_ants = []
		# If ant is waiting on the nest, explore.
		if self.state == State.WAITING:
			self.ant2explore(environment)
			

			return False

		# If ant's state is "Dead" go back to nest.
		elif self.state == State.DEAD:
			
			if self.pos == environment.initial_node:
				self.state = State.WAITING
				self.r_i = params.alpha
				self.movement = 'random'
				self.enter_nest(environment)
				self.path2nest = []
				
			else:
				self.move(environment)
			return False

		elif self.state == State.EXPLORING or self.state == State.EXPLORING_FROM_FOOD:
		
			# If food is found
			if (self.pos in environment.food and environment.food[self.pos] > 0):
				self.state = State.EXPLORING_FOOD
				self.movement = '2nest'
				self.r_i = params.beta_1
				environment.food[self.pos] -= 1
				#environment.tfood[self.pos] 
				self.locations.append(self.pos) # remember where food was found
				self.path2nest = deepcopy(environment.paths2nest[self.pos])
				self.path2food = deepcopy(environment.paths2food[self.pos])

				return True
			else:
				# Go to nest with a probability eta / (eta + omega) ~ 0.05%
				rng = random.random()
				if rng < params.eta / (params.omega + params.eta):
					self.ant2nest(environment)
				else:
					self.move(environment)
			
				return False

		elif (self.state == State.EXPLORING_FOOD):
			# if in nest node -> recruitment happens
			if(self.pos == environment.initial_node):
				self.state = State.RECRUITING
				environment.food_in_nest += 1
				self.r_i = params.gamma_1
				self.movement = '2food'
				
			# else keep moving to nest
			else:
				self.move(environment)
			
			return False

		elif (self.state == State.RECRUITING_FOOD):
			# if in nest node -> recruitment happens
			if(self.pos == environment.initial_node):
				self.state = State.RECRUITING
				environment.food_in_nest += 1
				self.r_i = params.gamma_2
				self.movement = '2food'
			# else keep moving to nest
			else:
				self.move(environment)
			
			return False

		elif (self.state == State.RECRUITING):
			# self.r_i should be equal to params.omega
			if random.random() < params.mu:
				self.state = State.EXPLORING_FROM_FOOD
				self.movement = 'random'
				self.r_i = params.omega
				self.MIA = 1 # missing in action

			else:
				# pick up food
				if (self.pos in environment.food):
					if environment.food[self.pos] > 0:
						self.state = State.RECRUITING_FOOD
						self.r_i = params.beta_2
						self.movement = '2nest'
						environment.food[self.pos] -= 1
						self.locations.append(self.pos) # remember where food was found
						self.path2nest = deepcopy(environment.paths2nest[self.pos])
						self.path2food = deepcopy(environment.paths2food[self.pos])

						return True

					else:
						# depending of foraging strategy:
						# if serial, the ant will return to nest
						# if parallel, the ant will explore	
						self.forage(environment)

					return False
				# recruit other ants
				elif self.pos == environment.initial_node:
					
					if self.r_i == params.gamma_1 or self.r_i == params.gamma_2:
						self.r_i = params.omega
						self.recruited_ants = self.recruit(environment, ant_pool)
						self.movement = '2food'

					else:
						# if not len(self.path):
						# 	self.leave_nest(environment)
						self.move(environment)

					return False
				else:
					self.move(environment)
					return False