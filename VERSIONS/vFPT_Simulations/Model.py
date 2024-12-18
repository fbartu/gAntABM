from mesa import space, Model, Agent
import networkx as nx
from Ant import np, Ant
import math
from functions import rotate, dist
from parameters import N, width, height, mot_matrix_LR, mot_matrix_SR, nest
# import pyarrow as pa
# import pyarrow.parquet as pq
import matplotlib.pyplot as plt


''' MODEL '''
class Model(Model):

	def __init__(self, rho, R, N = N, width = width, height = height):
	
		super().__init__()
   
		self.matrices = {'LR': mot_matrix_LR, 'SR': mot_matrix_SR}
		self.distance = R
  
		self.nest = nest
		self.N = N

  
		nds = [(0, i) for i in range(1, 44, 2)]

		# Lattice
		self.g = nx.hexagonal_lattice_graph(width, height, periodic = False)
		[self.g.remove_node(i) for i in nds]
		self.coords = nx.get_node_attributes(self.g, 'pos')
		for i in self.coords:
			self.coords[i] = tuple(np.round(self.coords[i], 5))
		self.grid = space.NetworkGrid(self.g)
		x = [xy[0] for xy in self.coords.values()]
		y = [xy[1] for xy in self.coords.values()]
		xy = [rotate(x[i], y[i], theta = math.pi / 2) for i in range(len(x))]
		self.xy = dict(zip(self.coords.keys(), xy))
  

		# Agents
		self.data = {i: [(0, 22)] for i in range(self.N)}
		self.init_agents(rho)
		self.init_targets()


		self.iters = 0
		self.init_nodes() ## initializes some metrics by node

		


	def init_targets(self):
		self.targets = [(6, 33), (6, 34), (7, 34), # patch 1
    (7, 33), (7, 32), (6, 32),
    (6, 11), (6, 12), (7, 12), # patch 2
    (7, 11), (7, 10), (6, 10)]
		
	# def init_targets(self):
	# 	tolerance = 1
	# 	darray = np.array([dist(self.xy[i], self.xy[nest]) for i in self.xy])
	# 	idx = np.where((darray > (self.distance - tolerance)) & (darray < (self.distance + tolerance)))[0]

	# 	nodes = np.array(list(self.xy.keys()))
	# 	self.targets = [tuple(x) for x in nodes[idx]]
	# 	self.targets = [tuple(x) for x in nodes[idx]]


	def step(self):

		while len(self.agents):
      
			remove_list = []

			for agent in self.agents.values():
				agent.action()
				if agent.pos in self.targets:
					remove_list.append(agent.unique_id)
    
			for agent in remove_list:
				del self.agents[agent]
			self.iters += 1

	def init_agents(self, rho):
		LR = round(rho * len(self.data))
		SR = round((1-rho) * len(self.data))
		indices = ['LR'] * LR + ['SR'] * SR
	 
		self.agents = {i: Ant(unique_id=i, model=self, mot_matrix=self.matrices[indices[i]], scout_type=indices[i]) for i in range(self.N)}
			
	def run(self):

		self.step()
  
		self.z = self.nodes['N']
		self.zq = np.unique(self.z, return_inverse = True)[1]
		self.pos = {'node': self.nodes['Node'], 'x': [x[0] for x in self.nodes['Coords']],
						  'y': [x[1] for x in self.nodes['Coords']], 'z': self.zq}
  
	def save_results(self, path, filename):

		data_long = {'id': [], 'pos': []}
		for k, v in self.data.items():
			data_long['id'].extend([k] * len(v))
			data_long['pos'].extend(v)
	 
   
		try:
			data = pa.Table.from_pydict(data_long)
			pq.write_table(data, path + filename + '_data.parquet', compression = 'gzip')
			print('Saved data', flush = True)
		except:
			Exception('Not saved!')
			print('Data not saved!', flush = True)

		try:
			pos = pa.Table.from_pydict(self.pos)
			pq.write_table(pos, path + filename + '_positions.parquet',compression = 'gzip')
			print('Saved positions', flush = True)
		except:
			Exception('Not saved!')
			print('Positions not saved!', flush = True)

	def remove_agent(self, agent: Agent) -> None:
		""" Remove the agent from the network and set its pos variable to None. """
		pos = agent.pos
		self._remove_agent(agent, pos)
		agent.pos = None

	def _remove_agent(self, agent: Agent, node_id: int) -> None:
		""" Remove an agent from a node. """

		self.g.nodes[node_id]["agent"].remove(agent)
  
	def init_nodes(self):
		if not hasattr(self, 'nodes'):
   
			self.nodes = {'Node': list(self.xy.keys()), 'Coords': list(self.xy.values()), 'N': [0]*len(self.xy)}

	def plot_lattice(self, z = None, labels = False):
    		
		coordsfood = [self.xy[i] for i in self.targets]

		plt.scatter([x[0] for x in coordsfood], [x[1] for x in coordsfood], c = 'grey', s = 200, alpha = 0.5)

		if z is None:

			plt.scatter([x[0] for x in self.xy.values()], [x[1] for x in self.xy.values()])

		else:
			plt.scatter([x[0] for x in self.xy.values()], [x[1] for x in self.xy.values()], c = z, cmap = 'coolwarm')
   
		if labels:
			v = list(self.xy.values())
			for i, txt in enumerate(self.coords.keys()):
				plt.annotate(txt, v[i])
		plt.scatter(self.xy[nest][0], self.xy[nest][1], marker = '^', s = 125, c = 'black')
		plt.show()
  
	def plot_trajectory(self, id):
     
		coordsfood = [self.xy[i] for i in self.targets]

		plt.scatter([x[0] for x in coordsfood], [x[1] for x in coordsfood], c = 'grey', s = 300, alpha = 0.25)
    
		xy = [self.xy[i] for i in self.data[id]]
		# point_size = 10 + np.array(list(range(len(xy))))
		# point_size = point_size / np.sum(point_size)
		# point_size *= 1000
		plt.scatter([x[0] for x in xy], [x[1] for x in xy], alpha = 0.6, c = list(range(len(xy))),
              cmap = 'viridis',s = 100, zorder = 2)
  
		e = list(self.g.edges)
		for i in e:
			coords = self.xy[i[0]], self.xy[i[1]]
			x = coords[0][0], coords[1][0]
			y = coords[0][1], coords[1][1]
			plt.plot(x, y, linewidth = 3, c = '#999999', zorder = 1)
   
		plt.scatter(self.xy[nest][0], self.xy[nest][1]-0.5, marker = '^', s = 200, c = 'black')
		plt.show()