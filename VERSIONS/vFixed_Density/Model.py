from mesa import space, Model, Agent
from Food import Food
import networkx as nx
from Ant import np, Ant, math, nest
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import pearsonr
from functions import rotate, moving_average, discretize_time, fill_hexagon, dist
from parameters import N, beta,foodXvertex, food_condition, width, height, Jij, Theta, scout_mov, recruit_mov
import pyarrow as pa
import pyarrow.parquet as pq
import random


''' MODEL '''
class Model(Model):

    def __init__(self, beta = beta, Theta = Theta, Jij = Jij, N = N, 
              width = width, height = height, food_condition = food_condition, 
              **kwargs):

        super().__init__()
        
        self.matrices = {'scout': scout_mov, 'recruit': recruit_mov}

        if 'Theta' not in kwargs:
            self.Theta = Theta
        else:
            self.Theta = kwargs['Theta']
   
        if 'Jij' not in kwargs:
            self.Jij = Jij
        else:
            self.Jij = kwargs['Jij']
   
        if 'tmax' not in kwargs:
            self.tmax = 2000
        else:
            self.tmax = kwargs['tmax']
            
        if 'init_position' not in kwargs:
            init_position = 'random'
        else:
            init_position = kwargs.pop('init_position')
   
        if 'feedback' not in kwargs:
            self.feedback = 'both'
        else:
            self.feedback = kwargs['feedback']

        if 'rho' not in kwargs:
            self.rho = 0.5
        else:
            self.rho = round(kwargs['rho'], 2)
   
        if 'epsilon' not in kwargs:
            self.epsilon = 1
        else:
            self.epsilon = round(kwargs['epsilon'], 2)
   
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
        # self.network = dict(zip(self.coords.keys(), [0]))
        # self.network[nest] = N
        # if 'd' in kwargs:
        #     d = float(kwargs["d"])
        #     if d < 0:
        #         self.distance = 3
        #     elif d > 26:
        #         self.distance = 26
        #     else:
        #         self.distance = d
        # else:
        #     self.distance = 13
  
        # Agents
        self.N = N
        self.init_agents(init_position, **kwargs)
            # self.agents[i] = Ant(i, self)
   
        # Init first active agent
        # self.agents[0].Si = np.random.uniform(0.0, 1.0)
        self.agents[0].Si = 1
  
        # Food
        self.food_condition = food_condition
        self.init_food()
        self.food_coords = [self.coords[i] for i in self.food_positions]
        print(self.food_coords, flush = True)

# 		self.data = pd.DataFrame({'T': [], 'Frame': [],
#    'N': [], 'Si_out': [], 'pos': [],
#    'id_out': [], 'Si_in': []})
#         self.data = {'T': [], 'Frame': [],
#    'N': [], 'Si_out': [], 'pos': [],
#    'id_out': [], 'Si_in': []}
#         self.data = {'T': [], 'Frame': [],
#    'N': [], 'pos': [], 'food_target': [], 'id_out': []}
        self.data = {'T': [], 'id': [], 'int_type': [], 
                     'node': [], 'x': [], 'y': [], 'movement': [], 'information' : []}


        # Rates
        self.R_t = beta * self.N

        # Time & Gillespie
        self.time = 0
        self.sample_time()

        self.iters = 0
        # self.gamma_counter = 0
        self.init_nodes() ## initializes some metrics by node

        self.sampled_agent = [np.nan]

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

            agent = np.random.choice(list(self.agents.values()))
            self.sampled_agent.append(agent.unique_id)
   
            # do action
            int_type = agent.action()

            self.collect_data(int_type=int_type)
            # self.collect_data(agent = agent, prev_state = prev_state)
            
            # get time for next iteration
            self.time += self.rng_t

            # get rng for next iteration
            self.sample_time()
            self.iters += 1
            
            
    def collect_data(self, int_type):
        node = []
        x = []
        y = []
        id = []
        target = []
        interaction = []
        # information transfer
        information = []

        for i in self.agents.values():
            node.append(str(i.pos))
            xy = self.xy[i.pos]
            x.append(xy[0])
            y.append(xy[1])
            target.append(i.movement)
            id.append(i.unique_id)
            if id[-1] == self.sampled_agent[-1]:
                interaction.append(int_type)
            else:
                interaction.append('none_none')
            information.append(i.informed)


        self.data['T'].extend([self.time] * self.N)
        self.data['id'].extend(id)
        self.data['int_type'].extend(interaction)
        self.data['node'].extend(node)
        self.data['x'].extend(x)
        self.data['y'].extend(y)
        self.data['movement'].extend(target)
        self.data['information'].extend(information)

    # def collect_data(self):

    #     pos = ''
    #     # target = 0
    #     # id_out = ''
    #     for i in self.agents.values():
    #         pos += str(i.pos) + ';'
    #         # target += int(hasattr(i, 'target') and i.target in self.food_coords)
    #         # Si_out += str(i.Si) + ','
    #         # id_out += str(i.unique_id) +','
   
    #     # for i in self.states['alpha']:
    #     #     Si_in += str(i.Si) +','
   
    #     self.data['T'].append(self.time)
    #     self.data['Frame'].append(round(self.time * 2))
    #     # self.data['Si_out'].append(Si_out[:-1])
    #     self.data['pos'].append(pos[:-1])
    #     # self.data['id_out'].append(id_out[:-1])
    #     # self.data['Si_in'].append(Si_in[:-1])
    #     # self.data['food_target'].append(target)
   
    def init_agents(self, init_position, **kwargs):
     
        if 'g' in kwargs:
            
            # must be passed as: size, type, value 1, value 2
            # e.g. '75,N,0.5,0.2' -> 75 % of gaussian with mu = 0.5 and sigma = 0.2
            # e.g. '25,B,0.5,0.5' -> 25 % of beta with shapes a = b = 0.5
            code = kwargs['g'].split(':')
            g = []
            try:
                for i in range(len(code)):
                        s, t, v1, v2 = code[i].split(',')
                        if t == 'N':
                            g += list(np.random.normal(loc = float(v1), scale = float(v2), size = int(s)))
                        elif t == 'B':
                            g += list(np.random.beta(a = float(v1), b = float(v2), size = int(s)))
                        else:
                            g += list(np.random.uniform(low = float(v1), high = float(v2), size = int(s)))
                if len(g) < self.N:
                    print('Warning: Less gains than population size passed to parametrization')
                    g += np.random.uniform(low = 0.0, high = 1.0, size = N - len(g))
                elif len(g) > self.N:
                    print('Warning: More gains than population size passed to parametrization')
                    g = g[:self.N]

            except:
                print('Warning: Values must be passed in a 4 sized list separated by commas.',
           '\n Switching to default behaviour in gain initialization')
                g = np.random.uniform(low = 0.0, high = 1.0, size = self.N)
     
        else:
            g = np.random.uniform(low = 0.0, high = 1.0, size = self.N)  
            
        if self.rho < 0:
            self.rho = 0

        nLR = round(self.N * self.rho)
        nSR = self.N - nLR
        indices = np.random.choice(self.N, size = nSR,replace=False)
        
        behav = np.array(['scout'] * self.N, dtype = '<U7')
        behav[indices] = 'recruit'
        mask = np.ones(self.N, dtype = bool)
        mask[indices] = False
        rec = np.array([False] * self.N)
        
        
        # social feedbacks [LR]
        if self.feedback == 'scout':
            nlisten = round(nLR * self.epsilon) 
            idx_listen = np.random.choice(np.array(list(range(self.N)))[mask], size = nlisten, replace = False)
            
            
        # social feedbacks [LR]    
        elif self.feedback == 'recruit':
            nlisten = round(nSR * self.epsilon) 
            idx_listen = np.random.choice(indices, size = nlisten, replace = False)
    
        # social feedbacks [Both]
        else:
            nlisten = round(nLR * (self.epsilon))
            idx_listen = np.random.choice(np.array(list(range(self.N)))[mask], size = nlisten, replace = False)
            nlisten = round(nSR * (self.epsilon))
            idx_listen = np.append(idx_listen, np.random.choice(indices, size = nlisten, replace = False))
            
        rec[idx_listen] = True
        # print('Number of LR: ', round(nLR * (self.epsilon)), '\n',
        #       'Number of SR: ', round(nSR * (self.epsilon)), '\n',
        #       'Total number of recruits: ', len(set(idx_listen)), flush = True)
            
        self.agents = {}
        if init_position == 'random':
            positions = random.sample(list(self.xy.keys()), self.N)
        else:
            positions = [nest] * self.N
        for i in range((self.N-1), -1, -1):
            self.agents[i] = Ant(i, self, g=g[i], social=rec[i], mot_matrix=self.matrices[behav[i]], behavior = behav[i],
                                 init_position=positions[i])
        
        # QUANTIFY INFORMATION TRANSMISSION
        self.agents[0].informed = True

    def set_default_movement(self, matrix = recruit_mov):
        for i in range(len(self.agents)):
            self.agents[i].mot_matrix = matrix
   
    def init_food(self):
     
        self.food_in_nest = 0
        if self.food_condition == 'det':
            self.init_det()
        # elif self.food_condition == 'dist':
        #     self.init_dist()
        # elif self.food_condition == 'sto_1':
        #     self.init_sto()
        # elif self.food_condition == 'sto_2':
        #     self.init_stoC()
        elif self.food_condition == 'nf':
            self.init_nf()
        else:
            print('No valid food conditions, initing determinist condition by default')
            self.init_det()
            
    def init_det(self):
        self.food_positions = [(6, 33), (6, 34), (7, 34), # patch 1
    (7, 33), (7, 32), (6, 32),
    (6, 11), (6, 12), (7, 12), # patch 2
    (7, 11), (7, 10), (6, 10)]
        self.food_dict = dict.fromkeys(self.food_positions, foodXvertex)  
        food_id = -1
  
        self.food = {}
        for i in self.food_positions:
            self.food[i] = [Food(i)] * foodXvertex
            for x in range(foodXvertex):
                self.grid.place_agent(self.food[i][x], i)
                self.food[i][x].unique_id = food_id
                food_id -= 1
    
    # def init_dist(self):
    #     tolerance = 1.5
    #     food_id = -1
    #     darray = np.array([dist(self.xy[i], self.xy[nest]) for i in self.xy])
    #     idx = np.where((darray > (self.distance - tolerance)) & (darray < (self.distance + tolerance)))[0]

    #     nodes = np.array(list(self.xy.keys()))
    #     food_indices = np.random.choice(idx, size = 12, replace = False)
    #     self.food_positions = [tuple(x) for x in nodes[food_indices]]
    #     self.food_dict = dict.fromkeys(self.food_positions, foodXvertex)
    #     self.food = {}
    #     for i in self.food_dict:
    #         self.food[i] = [Food(i)] * foodXvertex
    #         for x in range(foodXvertex):
    #             self.grid.place_agent(self.food[i][x], i)
    #             self.food[i][x].unique_id = food_id
    #             food_id -= 1
    
    # def init_sto(self):
    #     food_id = -1
  
    #     nodes = np.array(list(self.xy.keys()))
    #     food_indices = np.random.choice(len(self.xy), size = 12, replace = False)
    #     self.food_positions = [tuple(x) for x in nodes[food_indices]]
    #     self.food_dict = dict.fromkeys(self.food_positions, foodXvertex)
    #     self.food = {}
    #     for i in self.food_dict:
    #         self.food[i] = [Food(i)] * foodXvertex
    #         for x in range(foodXvertex):
    #             self.grid.place_agent(self.food[i][x], i)
    #             self.food[i][x].unique_id = food_id
    #             food_id -= 1
    
    # def init_stoC(self):
    #     food_id = -1
  
    #     nodes = np.array(list(filter(lambda a: self.xy[a][1] > 0.5, self.xy)))
    #     food_indices = np.random.choice(len(nodes), size = 2, replace = False)
    #     self.food_positions = [tuple(x) for x in nodes[food_indices]]
    #     bl = [(i, j) for j in range(45, 2, -2) for i in range(1, 12, 2)] + [(i, j) for j in range(44, 1, -2) for i in range(2, 13, 2)]
    #     clusters = []
    #     for i in self.food_positions:
    #         if i in bl:
    #             clusters.extend(fill_hexagon(i))
    #         else:
    #             l = [dist(self.xy[i], self.xy[target]) for target in bl]
    #             idx = np.argmin(l)
    #             clusters.extend(fill_hexagon(bl[idx]))
    
    #     self.food_positions = clusters
    #     self.food_dict = dict.fromkeys(self.food_positions, foodXvertex)
    #     self.food = {}
    #     for i in self.food_dict:
    #         self.food[i] = [Food(i)] * foodXvertex
    #         for x in range(foodXvertex):
    #             self.grid.place_agent(self.food[i][x], i)
    #             self.food[i][x].unique_id = food_id
    #             food_id -= 1
    
    def init_nf(self):
        self.food = dict.fromkeys((), [np.nan])
        self.food_positions = []
        self.food_dict = {}
            
    def run(self, plots = False):

        self.step(tmax = self.tmax)
  
        print('+++ Model successfully run... Collecting results... +++', flush = True)
        if plots:
            self.plot_N()
   
        # self.z = [self.nodes.loc[self.nodes['Node'] == i, 'N'] for i in self.xy]
        self.z = self.nodes['N']
        self.zq = np.unique(self.z, return_inverse = True)[1]
        # self.pos = {'node': self.nodes['Node'], 'x': [x[0] for x in self.nodes['Coords']],
        #                   'y': [x[1] for x in self.nodes['Coords']], 'z': self.zq}
        self.pos = {'node': [str(i) for i in self.nodes['Node']], 'x': [x[0] for x in self.nodes['Coords']],
                    'y': [x[1] for x in self.nodes['Coords']], 'z': self.zq}
        # self.pos = pd.DataFrame({'node': list(self.xy.keys()), 'x': [x[0] for x in self.xy.values()],
        #                   'y': [x[1] for x in self.xy.values()], 'z': self.zq})
        try:
            self.collect_results()
            print('+++ Results collected successfully! +++', flush = True)
        except:
            Exception('Could not collect results')
            print('Could not collect results', flush = True)
            
    def run_exploration(self, plots = False):
        while sum([self.food[i][-1].is_detected for i in self.food]) == 0:
            self.step(tmax = self.time + 1)
  
        print('+++ Model successfully run... Collecting results... +++', flush = True)
        if plots:
            self.plot_N()
   
        self.z = self.nodes['N']
        self.zq = np.unique(self.z, return_inverse = True)[1]
        self.pos = {'node': self.nodes['Node'], 'x': [x[0] for x in self.nodes['Coords']],
                          'y': [x[1] for x in self.nodes['Coords']], 'z': self.zq}

        try:
            self.collect_results()
            print('+++ Results collected successfully! +++', flush = True)
        except:
            Exception('Could not collect results')
            print('Could not collect results', flush = True)

  
    def collect_results(self, fps = 2):
     
 
        # result = pd.DataFrame({'T': self.data['T'], 'N': self.data['N']})
        # result['Frame'] = result['T'] // (1 / fps)
        # df = result.groupby('Frame').agg({'N': 'mean'}).reset_index()

        food = {'node': list(self.food.keys()),
                't': [round(food.detection_time,3) if food.is_detected else np.nan for foodlist in self.food.values() for food in foodlist ],
                'origin': [food.detection_origin if food.is_detected else None for foodlist in self.food.values() for food in foodlist ]}
  
        # self.df = df
        self.food_df = food
  
    # def run_food(self, tmax, plots = False):
    #     n = sum(self.model.food_dict.values())
    #     t = 1
    #     while sum(self.model.food_dict.values()) == n:
    #         self.step(t)
    #         t += 1
    #     self.step(tmax + t)
    #     if plots:
    #         self.plot_N()
    #         self.plot_I()

    def save_results(self, path, filename):
     
        # try:
        #     self.df.to_parquet(path + filename + '.parquet', index=False, compression = 'gzip', engine = 'pyarrow')
        #     print('Saved N', flush = True)
        # except:
        #     Exception('Not saved!')
        #     print('N not saved!', flush = True)
   
        try:
            data = pa.Table.from_pydict(self.data)
            pq.write_table(data, path + filename + '_data.parquet', compression = 'gzip')
            print('Saved data', flush = True)
        except:
            Exception('Not saved!')
            print('Data not saved!', flush = True)
   
        # try:
        #     food = pa.Table.from_pydict(self.food_df)
        #     pq.write_table(food, path + filename + '_food.parquet', compression = 'gzip')
        #     print('Saved food', flush = True)
        # except:
        #     Exception('Not saved!')
        #     print('Food not saved!', flush = True)

        try:
            pos = pa.Table.from_pydict(self.pos)
            pq.write_table(pos, path + filename + '_positions.parquet',compression = 'gzip')
            print('Saved positions', flush = True)
        except:
            Exception('Not saved!')
            print('Positions not saved!', flush = True)

    def plot_lattice(self, z = None, labels = False):
        
        coordsfood = [self.xy[i] for i in self.food]

        if self.food_condition == 'det' or self.food_condition == 'sto_2':

            xyfood = [coordsfood[:6],coordsfood[6:]]
            plt.fill([x[0] for x in xyfood[0]], [x[1] for x in xyfood[0]], c = 'grey')
            plt.fill([x[0] for x in xyfood[1]], [x[1] for x in xyfood[1]], c = 'grey')
   
        elif self.food_condition == 'sto_1' or self.food_condition == 'dist':
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

        coordsfood = [self.xy[i] for i in self.food]
        xyfood = [coordsfood[:6],coordsfood[6:]]
        plt.fill([x[0] for x in xyfood[0]], [x[1] for x in xyfood[0]], c = 'grey')
        plt.fill([x[0] for x in xyfood[1]], [x[1] for x in xyfood[1]], c = 'grey')
  
        xy = [self.xy[i] for i in self.agents[id].path]
        plt.scatter([x[0] for x in xy], [x[1] for x in xy], alpha = 1, c = list(range(len(xy))),cmap = 'viridis', zorder = 2)
  
        e = list(self.g.edges)
        for i in e:
            coords = self.xy[i[0]], self.xy[i[1]]
            x = coords[0][0], coords[1][0]
            y = coords[0][1], coords[1][1]
            plt.plot(x, y, linewidth = 3, c = '#999999', zorder = 1)
   


        plt.scatter(self.xy[nest][0], self.xy[nest][1], marker = '^', s = 50, c = 'black')
        plt.show()
  
    def plot_S(self):
        if not hasattr(self, 'Si_in'):
            self.Si_in = [np.sum([float(j) for j in self.data['Si_in'][i].split(',')]) if len(self.data['Si_in'][i]) else 0 for i in range(len(self.data['Si_in']))]
            self.Si_out = [np.sum([float(j) for j in self.data['Si_out'][i].split(',')]) if len(self.data['Si_out'][i]) else 0 for i in range(len(self.data['Si_out']))]

        Si_in = np.log(self.Si_in)
        Si_out = np.log(self.Si_out)
        t2min = 60
        # t2min = 120
        v = self.data['N']
        t = np.array(self.data['T']) / t2min
        plt.plot(t, v)
        plt.plot(t, Si_in)
        plt.plot(t, Si_out)

        if 0 in list(self.food_dict.values()):

            times = list(filter(lambda i: i[0].is_collected, self.food.values()))

            minv = np.min([i[0].collection_time for i in times]) / t2min
            maxv = np.max([i[0].collection_time for i in times]) / t2min

        else:
            minv = np.nan
            maxv = np.nan

        plt.axvline(x = minv, ymin = 0, ymax = np.max(self.data['N']), color = 'midnightblue', ls = '--')
        plt.axvline(x = maxv, ymin = 0, ymax = np.max(self.data['N']), color = 'midnightblue', ls = '--')
        plt.xlabel('Time (min)')
        plt.legend(['Ocupancy (N)', 'Activity nest (log(S))', 'Activity arena (log(S))'])
        plt.xticks(list(range(0, 185, 15)))
        plt.show()
  
    def plot_N(self):

        t2min = 60
        # t2min = 120
        v = self.data['N']
        t = np.array(self.data['T']) / t2min
        plt.plot(t, v)

        if 0 in list(self.food_dict.values()):

            times = list(filter(lambda i: i[0].is_collected, self.food.values()))

            minv = np.min([i[0].collection_time for i in times]) / t2min
            maxv = np.max([i[0].collection_time for i in times]) / t2min

        else:
            minv = np.nan
            maxv = np.nan

        plt.axvline(x = minv, ymin = 0, ymax = np.max(self.data['N']), color = 'midnightblue', ls = '--')
        plt.axvline(x = maxv, ymin = 0, ymax = np.max(self.data['N']), color = 'midnightblue', ls = '--')
        plt.xlabel('Time (min)')
        plt.ylabel('Number of active ants')
        plt.xticks(list(range(0, 185, 15)))
        plt.show()


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
  
    def init_nodes(self):
        if not hasattr(self, 'nodes'):
   
            self.nodes = {'Node': list(self.xy.keys()), 'Coords': list(self.xy.values()), 'N': [0]*len(self.xy), 'Si': [0.0] * len(self.xy)}

    # def init_nodes(self, chunks_x = 3 ,chunks_y = 2):
    # 	if not hasattr(self, 'nodes'):
    # 		xykeys = list(self.xy.keys())
    # 		keyarray = np.array(xykeys)
    # 		xyvals = list(self.xy.values())
    # 		xyarray = np.array(xyvals)
    # 		maxx = np.max([x[0] for x in xyarray])
    # 		minx = np.min([x[0] for x in xyarray])
    # 		maxy = np.max([x[1] for x in xyarray]) +0.1 # otherwise it does not catch the top vertices
    # 		miny = np.min([x[1] for x in xyarray])
   
    # 		delta_x = (maxx - minx) / chunks_x
    # 		delta_y = (maxy - miny) / chunks_y
    # 		xcoords = [minx + delta_x * i for i in range(chunks_x)]
    # 		ycoords = [miny + delta_y * i for i in range(chunks_y)]
    # 		lims = [((j, i), (j+ delta_x, i + delta_y) ) for i in ycoords for j in xcoords]
   
    # 		nodelist = [(xyarray[::, 0] >= i[0][0]) &
    #               (xyarray[::, 0] < i[1][0]) &
    #               (xyarray[::, 1] >= i[0][1] ) &
    #               (xyarray[::, 1] < i[1][1]) for i in lims]
   
    # 		self.nodes = pd.DataFrame({'Node': [], 'Coords': [], 'Sector': []})
    # 		for i in range(len(nodelist)):
    # 			nds = [tuple(x) for x in xyarray[nodelist[i]]]
    # 			tags = [tuple(x) for x in keyarray[nodelist[i]]]
    # 			self.nodes = pd.concat([self.nodes, 
    #                          pd.DataFrame({'Node': tags, 'Coords': nds, 'Sector': [i+1] * len(nds)})])
    
    # 		self.nodes['N'] = 0
    # 		self.nodes['Si'] = float(0)


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
