from mesa import Agent
import numpy as np
from functions import direction, get_cos
import math
from parameters import nest, theta
import random

''' ANT AGENT '''
class Ant(Agent):

	def __init__(self, unique_id, model, mot_matrix, behavior, init_position, social = True, g = np.random.uniform(0.0, 1.0)):

		super().__init__(unique_id, model)

		self.Si = 0
		# self.g = g
		self.g = 1

		self.is_active = False
		self.state = '0'
		self.behavior_tag = behavior
		self.init_position = init_position
		self.informed = False

		self.origin = nest

		self.food = []

		self.leave_nest()
   
		self.reset_movement()
		self.move_default = self.move_exp
  
		self.mot_matrix = mot_matrix
  
		if social:
			self.interaction = self.interaction_with_recruitment
		else:
			self.interaction = self.interaction_without_recruitment
		

	def reset_movement(self):
		self.movement = 'default'
		# self.move_history = (None, None, None)
		self.move_history = (self.init_position, 
                       random.choice(self.model.grid.get_neighbors(self.init_position)),
                       self.init_position)
 
	def update_movement(self):
		self.move_history = (self.move_history[1], self.move_history[2], self.pos)

	def move_exp(self, pos):
		if None in self.move_history:
			return self.move_random(pos)

		else:

			p = []
			r = range(len(pos))
			for i in r:
				x = [self.model.coords[self.move_history[1]], self.model.coords[self.move_history[2]], self.model.coords[pos[i]]]
				p.append(self.mot_matrix[direction(x)])

			idx = np.random.choice(r, p = p / np.sum(p)) # normalize to 1 in case probabilities don't already sum 1
			return pos[idx]

	def move_random(self, pos):
		l = list(range(len(pos)))
		idx = np.random.choice(l)
		return pos[idx]

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


	def find_neighbors(self):
    
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
		int_type = self.behavior_tag + '_' + self.movement + '+'
  
		l = len(neighbors)
		if l:
			# for more than one neighbor...
			for i in neighbors:
				s.append(i.state)
				z.append(self.model.Jij[self.state + "-" + i.state]* i.Si - self.model.Theta)
				if hasattr(i, 'food_location'): t.append(self.model.coords[i.food_location])
				int_type += i.behavior_tag + '_' + i.movement + '+'

			z = sum(z)


		else:
			z = 0
		self.Si = math.tanh(self.g * (z + self.Si -self.model.Theta) ) # update activity
		if len(t):
		# if len(t) and not hasattr(self, 'target'):
			self.target = t[-1]
			self.movement = 'target'
   
		return int_type[:-1]

	def interaction_without_recruitment(self):
		neighbors = self.find_neighbors()

		s = [] # state
		z = [] # activity
		int_type = self.behavior_tag + '_' + self.movement + '+'
  
		l = len(neighbors)
		if l:
			# for more than one neighbor...
			for i in neighbors:
				s.append(i.state)
				z.append(self.model.Jij[self.state + "-" + i.state]* i.Si - self.model.Theta)
				int_type += i.behavior_tag + '_' + i.movement + '+'

			z = sum(z)
   
		else:
			z = 0
		self.Si = math.tanh(self.g * (z + self.Si -self.model.Theta) ) # update activity
		
		return int_type[:-1]
 
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
  
	def activate(self):
		self.Si = np.random.random()
		self.is_active = True
 
	def leave_nest(self):
		self.model.grid.place_agent(self, self.init_position)
		self.is_active = True
		# self.activate()

	def enter_nest(self):
		self.is_active = False
		self.ant2explore()
		
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


	def drop_food(self):
		self.food[-1].dropped(self.model.time)
		self.food.pop()
	
  
	def action(self):
	
		# if len(self.food):
		# 	self.ant2nest()

		# if self.Si < theta:
		# 	self.ant2nest()
   
		# 	if self.pos == nest:
		# 		self.enter_nest()

		# 		## SPONTANEOUS ACTIVATION
		# 		if np.random.random() < 0.01:
		# 			self.activate()
    
		# 	else:
		# 		self.move()

		# else:
		# 	self.move()

		# -------------------------------------------------#
		# elif self.pos in self.model.food_positions:
	
		# 	if not self.model.food[self.pos][-1].is_detected:
		# 		self.model.food[self.pos][-1].detected(self.model.time, self.origin)
	
		# 	self.origin = self.pos
	
		# 	if hasattr(self, 'target') and self.model.coords[self.pos] == self.target:
		# 		self.ant2explore()
	
		# 	if self.model.food_dict[self.pos] > 0 and not len(self.food):
		# 		self.pick_food()

		# 	else:
		# 		self.move()
	
		# else:
		# 	self.move()
		# -------------------------------------------------#
  
		self.move()

		int_type = self.interaction()
		return int_type