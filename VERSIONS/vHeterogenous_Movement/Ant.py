from mesa import Agent
import numpy as np
from functions import direction, get_cos , get_cos_180, dist 
import math
from parameters import nest, theta # , nest_influence, direction_bias

''' ANT AGENT '''
class Ant(Agent):

	def __init__(self, unique_id, model, mot_matrix, default_movement = 'exp', g = np.random.uniform(0.0, 1.0), recruitment = True):

		super().__init__(unique_id, model)

		self.Si = 0
		self.g = g

		self.is_active = False
		self.state = '0'
		self.status = 'gamma'

		self.origin = nest

		self.food = []

		self.pos = 'nest'
   
		self.reset_movement()
		self.move_default = self.check_movement(default_movement)
  
		self.mot_matrix = mot_matrix
  
		if recruitment:
			self.interaction = self.interaction_with_recruitment
		else:
			self.interaction = self.interaction_without_recruitment
		

	def reset_movement(self):
		self.movement = 'default'
		self.move_history = (None, None, None)
 
	def update_movement(self):
		self.move_history = (self.move_history[1], self.move_history[2], self.pos)
  
	def check_movement(self, type):
		if type == 'random':
			return self.move_random
		elif type == 'exp':
			return self.move_exp
		elif type == 'bal':
			return self.move_ballistic
		else:
			print('Invalid default movement, defaulting to experiment movement')
			return self.move_exp

	def move_exp(self, pos):
		if None in self.move_history:
			return self.move_random(pos)

		else:

			p = np.array(self.mot_matrix[direction([self.model.coords[i] for i in self.move_history])])
			ords = []
			pord = []
			for i in range(len(pos)):
				x = [self.model.coords[self.move_history[1]], self.model.coords[self.move_history[2]], self.model.coords[pos[i]]]
				ords.append(i)
				dirx = direction(x)
				if dirx == 1:
					pord.append(p[0])
				elif dirx == 0:
					pord.append(p[1])
				elif dirx == -1:
					pord.append(p[2])

			idx = np.random.choice(ords, p = pord / np.sum(pord)) # normalize to 1 in case probabilities don't already sum 1
			return pos[idx]

	def move_random(self, pos):
		l = list(range(len(pos)))
		idx = np.random.choice(l)
		return pos[idx]

	# def move_homing(self, pos):
	# 	l = list(range(len(pos)))
	# 	d = [dist(self.target, self.model.coords[i]) for i in pos]
	# 	idx = np.argmin(d)
	# 	v = 1 / (len(d) + direction_bias - 1)
	# 	p = [direction_bias / (len(d) + direction_bias - 1) if i == idx else v for i in l]
	# 	idx = np.random.choice(l, p = p)
	# 	return pos[idx]


	def move_homing(self, pos):
		
		x0 = np.array(self.model.coords[self.pos])
		x1 = np.array([self.model.coords[i] for i in pos])
	
		tpos = x1 - x0
		d = self.target - x0

		l = len(pos)
		if l == 2:
			A = 1+get_cos(d, tpos[0])
			p1 = (A) / (A + (1+get_cos(d, tpos[1])))
			p2 = 1-p1
			p = [p1, p2]
			idx = np.random.choice(l, p = p / np.sum(p))

		elif l == 3:
			p = []
			for i in range(l):
				pi = (1/3) * (1 + get_cos(d, tpos[i]))
				p.append(pi)
			idx = np.random.choice(l, p = p/np.sum(p))
		else:
			idx = 0

		return pos[idx]

	def move_ballistic(self, pos, bias = 1): # 10/7 ~ 1.43 = 10% d'error
    		
		x0 = np.array(self.model.coords[self.pos])
		x1 = np.array([self.model.coords[i] for i in pos])
	
		tpos = x1 - x0
		d = self.model.coords[nest] - x0

		l = len(pos)
		if l == 2:
			A = bias + get_cos_180(d, tpos[0])
			p1 = (A) / (A + (bias + get_cos_180(d, tpos[1])))
			p2 = 1-p1
			p = [p1, p2]
			idx = np.random.choice(l, p = p / np.sum(p))

		elif l == 3:
			p = []
			for i in range(l):
				pi = (1/(3*bias)) * (bias + get_cos_180(d, tpos[i]))
				p.append(pi)
			idx = np.random.choice(l, p = p/np.sum(p))
		else:
			idx = 0

		return pos[idx]

	# Move method
	def move(self):
     
		possible_steps = self.model.grid.get_neighbors(
		self.pos,
		include_center = False)

		if self.movement == 'default':
			pos = self.move_default(possible_steps)
	
		else:
			pos = self.move_homing(possible_steps) # works also towards food

		self.model.grid.move_agent(self, pos)
		self.model.nodes['N'][self.model.nodes['Node'].index(self.pos)] += 1
		# self.model.nodes.loc[self.model.nodes['Node'] == self.pos, 'N'] += 1
		self.update_movement()

	# def find_neighbors(self):

	# 	if self.pos == 'nest':
   
	# 		alist = self.model.states['alpha']

	# 	else:
	# 		alist = self.model.grid.get_cell_list_contents([self.pos])
   
	# 	flist = list(filter(lambda a: a.unique_id != self.unique_id, alist))
  
	# 	if len(flist):
	# 		neighbors = np.random.choice(flist, size = 1, replace = False)
	# 	else:
	# 		neighbors = []

	# 	return neighbors
 

	def find_neighbors(self):
    
		if self.pos == 'nest':
   
			alist = self.model.states['alpha']

		else:
			alist = self.model.grid.get_cell_list_contents([self.pos])
   
		flist = list(filter(lambda a: a.unique_id != self.unique_id, alist))
  
		if len(flist) <= 4 and len(flist) > 0:
			neighbors = np.random.choice(flist, size = len(flist), replace = False)
		elif len(flist) > 4:
			neighbors = np.random.choice(flist, size = 4, replace = False)
		else:
			neighbors = []

		return neighbors


	def interaction_with_recruitment(self):
		neighbors = self.find_neighbors()

		s = [] # state
		z = [] # activity
		t = [] # target
  
		l = len(neighbors)
		if l:
			# for more than one neighbor...
			for i in neighbors:
				s.append(i.state)
				z.append(self.model.Jij[self.state + "-" + i.state]* i.Si - self.model.Theta)
				if hasattr(i, 'food_location'): t.append(self.model.coords[i.food_location])

			z = sum(z)


		else:
			z = 0
		self.Si = math.tanh(self.g * (z + self.Si -self.model.Theta) ) # update activity
		if len(t):
		# if len(t) and not hasattr(self, 'target'):
			self.target = t[-1]
			self.movement = 'target'


	# def interaction_with_recruitment(self):
	# 	neighbors = self.find_neighbors()
  
	# 	l = len(neighbors)
	# 	if l:
	# 		z = self.model.Jij[self.state + "-" + neighbors[0].state]* neighbors[0].Si - self.model.Theta

	# 		## Food location communication!
	# 		if hasattr(neighbors[0], 'food_location') and self.state == '0':
	# 			self.target = self.model.coords[neighbors[0].food_location]
	# 			self.movement = 'target'
    
	# 	else:
	# 		z = -self.model.Theta
	# 	self.Si = math.tanh(self.g * (z + self.Si) ) # update activity
    
	# def interaction_without_recruitment(self):
	# 	neighbors = self.find_neighbors()
  
	# 	l = len(neighbors)
	# 	if l:
	# 		z = self.model.Jij[self.state + "-" + neighbors[0].state]* neighbors[0].Si - self.model.Theta
				
	# 	else:
	# 		z = -self.model.Theta
	# 	self.Si = math.tanh(self.g * (z + self.Si) ) # update activity
 
	def interaction_without_recruitment(self):
		neighbors = self.find_neighbors()

		s = [] # state
		z = [] # activity
  
		l = len(neighbors)
		if l:
			# for more than one neighbor...
			for i in neighbors:
				s.append(i.state)
				z.append(self.model.Jij[self.state + "-" + i.state]* i.Si - self.model.Theta)

			z = sum(z)
   
		else:
			z = 0
		self.Si = math.tanh(self.g * (z + self.Si -self.model.Theta) ) # update activity
	
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
 
	def leave_nest(self):
		self.model.grid.place_agent(self, nest)
		self.is_active = True

	def enter_nest(self):
		self.model.remove_agent(self)
		self.is_active = False
		self.pos = 'nest'
		self.ant2explore()
		self.origin = nest
		
		if len(self.food):
			self.food[-1].in_nest(self.model.time)

	def ant2nest(self):
		self.target = self.model.coords[nest]
		self.movement = 'homing'

	def ant2explore(self):
		if hasattr(self, 'target'):
			del self.target
		self.reset_movement()

	def pick_food(self):
		self.model.remove_agent(self.model.food[self.pos][0])
		self.food.append(self.model.food[self.pos].pop(0))
		self.model.food[self.pos].extend(self.food)
		self.model.food[self.pos][-1].collected(self.model.time)
		self.model.food_dict[self.pos] -= 1
		self.food_location = self.pos
		self.state = '1'
		### MODIFICATION OF DEFAULT MOVEMENT !!
		# self.model.set_default_movement('exp')


	def drop_food(self):
		self.food[-1].dropped(self.model.time)
		self.food.pop()
	
  
	def action(self, rate):
		
		if rate == 'alpha':
			if len(self.food):
				self.drop_food()
			else:
				if self.Si > theta:
					self.leave_nest()

		elif rate == 'beta':
	  
			if len(self.food):
				self.ant2nest()
    
			if self.Si < theta:
				self.ant2nest()

			if self.pos == nest:
				if hasattr(self, 'target') and self.target == self.model.coords[nest]:
					self.enter_nest()

				else:
					self.move()

			elif self.pos in self.model.food_positions:
       
				if not self.model.food[self.pos][-1].is_detected:
					self.model.food[self.pos][-1].detected(self.model.time, self.origin)
     
				self.origin = self.pos
       
				if hasattr(self, 'target') and self.model.coords[self.pos] == self.target:
					self.ant2explore()
	   
				if self.model.food_dict[self.pos] > 0 and not len(self.food):
					self.pick_food()

				else:
					self.move()
     
			else:
				self.move()
   
		else:
			self.Si = np.random.uniform(0.0, 1.0) ## spontaneous activation


		self.interaction()
		self.update_status()