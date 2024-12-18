from mesa.space import NetworkGrid
import networkx as nx

class Lattice():

	"""A model with some number of ant agents."""

	def __init__(self, n_agents, width, height, nest_node, food):

		# Initialize key components in the lattice
		self.initial_node = nest_node
		self.food = food
		self.food_in_nest = 0
		self.food_cluster = {}
		self.waiting_ants = dict(zip(list(range(n_agents)), list(range(n_agents))))
		self.out_nest = {}
		self.tfood = {}

		#Create the hexagonal lattice
		self.G = nx.hexagonal_lattice_graph(width,height,periodic=False)
		self.grid = NetworkGrid(self.G)

		# Compute the shortest paths of the lattice (food to nest, and backwards)
		self.paths2nest = [nx.shortest_path(self.G, pos, self.initial_node) for pos in self.food.keys()]
		self.paths2food = [list(reversed(path)) for path in self.paths2nest]

		# The key of the dictionary holds the food position, so it is easy to keep track of the path
		self.paths2nest = dict(zip(self.food.keys(), self.paths2nest))
		self.paths2food = dict(zip(self.food.keys(), self.paths2food))


	# splits food list into packs of 6 positions (that usually conform a patch of food)
	# assumes ordered positions 
	def split_food_patches(self, each = 6):
		lst = list(self.food.keys())
		self.patch_positions = [lst[i:i + each] for i in range(0, len(lst), each)]

	# method for grouping the food (in a list of positions) in clusters (patches)
	def cluster_food(self, pos, id = 0, iterative = True):
		if iterative:
			self.split_food_patches()
			for i in range(len(self.patch_positions)):
				self.food_cluster['Patch ' + str(i)] = self.patch_positions[i]
		else:
			self.food_cluster['Patch ' + str(id)] = list(pos)

	def scatter_food(self):
		import random
		pos = nx.get_node_attributes(self.G, 'pos')
		if self.initial_node in pos.keys():
			del pos[self.initial_node]

		L = []
		for i in range(sum(self.food.values())):
			L.append(random.choice(list(pos.keys())))
			del pos[L[-1]]

		self.food = dict.fromkeys(L, 1)