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
  
	def in_nest(self, time):
		self.nest_time = time
  
	def dropped(self, time):
		self.drop_time = time
		self.is_dropped = True