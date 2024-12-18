from mesa import Agent
import numpy as np
from functions import direction


''' ANT AGENT '''
class Ant(Agent):

	def __init__(self, unique_id, model, mot_matrix, scout_type):

		super().__init__(unique_id, model)

		self.pos = model.nest
		self.model.grid.place_agent(self, self.pos)
   
		self.reset_movement()
  
		self.mot_matrix = mot_matrix
		self.scout_type = scout_type

	def reset_movement(self):
		self.movement = 'default'
		self.move_history = (None, None, None)
 
	def update_movement(self):
		self.move_history = (self.move_history[1], self.move_history[2], self.pos)


	def move_exp(self, pos):
		if None in self.move_history:
			return self.move_random(pos)

		else:
			try:
				p = np.array(self.mot_matrix[direction([self.model.coords[i] for i in self.move_history])])
			except:
				print(self.unique_id, self.pos)
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

	# Move method
	def move(self):
     
		possible_steps = self.model.grid.get_neighbors(
		self.pos,
		include_center = False)

		pos = self.move_exp(possible_steps)

		self.model.grid.move_agent(self, pos)
		self.model.nodes['N'][self.model.nodes['Node'].index(self.pos)] += 1
		self.update_movement()
 
	def action(self):
		self.move()
		self.model.data[self.unique_id].append(self.pos)
		self.model.nodes['N'][self.model.nodes['Node'].index(self.pos)] += 1
