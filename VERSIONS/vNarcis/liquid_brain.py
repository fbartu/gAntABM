""" RELATED PAPERS """
"""
R.V. Solé, O.Miramontes and B.C.Goodwin. J. Theor. Biol.
161 (1993) 343.

R.V. So1é, O. Miramontes and B.C. Goodwin, Emergent
Behaviour in Insect Societies: Global Oscillations, Chaos and
Computation, in: Interdisciplinary Approaches to Nonlinear
Complex Systems, eds. H. Haken and A. Mikhailov, Springer
Series in Synergetics, Vol. 62 (Springer, 1993) p. 77.

O. Miramontes, R.V. Solé and B.C. Goodwin, Physica D 63
(1993) 145. 
LINK: https://www.sciencedirect.com/science/article/pii/016727899390152Q?via%3Dihub


O. Miramontes, R.V. Solé and B.C. Goodwin, Antichaos in
Ants: the Excitability Metaphor at Two Hierarchical Levels,
in: Selforganization and Life (MIT Press, 1993) p. 790.

D.J. Amit, Modelling Brain Function (Cambridge University
Press, 1989).

"""

''' INFORMATION AT THE EDGE OF CHAOS IN FLUID NEURAL NETWORKS (Solé & Miramontes, 1993)'''
import math
import numpy as np
import random


""" PARAMETERS """
L = 10 # lattice grid
N = 60 # number of automata
rho = N / L**2 # agent density
g = 0.05 # gain (sensitivity) parameter
theta = 10**-16 # threshold of activity (inactive if Activity < theta) 
Sa = 0.01 # spontaneous activation activity
Pa = 0.01 # probability of spontaneous activation
# Coupling coefficients (Jij, intensity of interaction?) are 1


# Si_t = [] # state of the ith automata at time t
# Phi = [] # sigmoid function describing the state of the neuron or automata (D.J. Amit, Modelling Brain Function; Cambridge University Press, 1989)
# Theta = 0 # threshold of activation, set to Theta = 0 for simplicity (says the paper). Virtually, Theta = theta (10**-16)
# this spontaneous activation brings S_i to Sa, with some probability Pa
# B = [] # boundary. The state of the ith automaton is the sum of the states of the eight neighbours plus its state
# states available
# Active = [] # moves to one of the eight nearest cells, if able to
# Inactive = []


# Si_t+1 = tanh { g [ sum(Jij * Sj_t-1) + Jii * Si_t-1 ] }

# Si_t1 = Phi * ( g * ( Jii * Si_t + np.sum( Jij * Sj_t - Theta_i ) ) ) # // STATE FUNCTION

# Initial positions and activity (-1, 1) chosen randomly

class Agent:
    def __init__(self, pos):
        self.pos = pos
        self.prev_pos = pos

        self.Si = random.uniform(-1.0, 1.0) # activity
        self.Ai = self.Si
        
        self.check_state()
        
    def update_activity(self):
        self.Si = self.Ai
        
    def check_state(self):
        if self.Si < theta:
            self.state = 0 # inactive
            
        else:
            self.state = 1 # active
            
    def action(self, grid):
        
        self.check_state()
        self.compute_activity(grid)
        
        if self.state == 0:
            
            # chance of spontaneous activity
            if random.random() < Pa:
                # self.Si = Sa
                self.Ai = Sa
                self.state = 1
                
            grid.grid[self.pos] = self.Si
                

                
        else:
            self.move(grid)
        
    def move(self, grid):

        m = grid.get_real_positions(self.pos)
        m = [tuple(x) for x in m]
        i = 0
        
        # try to move at random to an empty positions (capped at six attempts)
        while i < 6:
            pos = random.choice(m)
            if grid.grid[pos] != 0:
                i += 1

            else:
                i = 6
                grid.grid[pos] = self.Si
                grid.grid[self.pos] = 0
                self.pos = pos
        
        
    def compute_activity(self, grid):
        
        z = grid.get_activity(self.pos)
        z = (np.sum(z)) + self.Si
        self.Ai = math.tanh(g * z)
        

class Lattice:
    
    def __init__(self):
        
        self.grid = np.zeros((L, L), dtype = float)
        self.neighborhood = [(-1, 1), (0, 1), (1, 1), (-1, 0),
             (1, 0), (-1, -1), (0,-1), (1,-1)]
        i = np.indices((L, L))
        x = np.concatenate(i[0]).ravel().tolist()
        y = np.concatenate(i[1]).ravel().tolist()
        self.coords = list(zip(x, y))
        
    def get_real_positions(self, pos):
        new_positions = np.array(pos) + self.neighborhood
        
        # filter to eliminate non-existing coordinates
        idx = np.sum((new_positions > -1) & (new_positions < L), axis = 1)
        new_positions = new_positions[np.where(idx == 2)]
        
        return new_positions
    
    def get_neighbors(self, pos):
        positions = self.get_real_positions(pos)
        pos = tuple(positions.T.tolist())
        
        return pos
    
    def get_activity(self, pos):
        
        xy = self.get_neighbors(pos)
        
        return self.grid[xy]
        
        
class Model:
    def __init__(self):
        self.grid = Lattice()
        self.agents = []
        for i in range(N):
            pos = random.choice(list(zip(*np.where(self.grid.grid == 0))))
            self.agents.append(Agent(pos = pos))
            self.grid.grid[pos] = self.agents[-1].Si
        
    def update_agents(self):
        
        for a in self.agents:
            a.update_activity()
            self.grid.grid[a.pos] = a.Si

    def run(self, iters):
        
        self.results = []
        for i in range(iters):
            
            act = 0
            
            for a in self.agents:
                a.action(self.grid)
                act += a.state

            self.update_agents()
            self.results.append(act)
            
        self.results = {'Time': list(range(iters)), 'Activity': self.results}
       
       
""" FOR FAST SIMULATIONS AND RESULT VISUALIZATION """
import matplotlib.pyplot as plt
def model_run(iters):
    m = Model()
    m.run(iters)
    plt.plot(m.results['Time'], m.results['Activity'])
    plt.ylabel('Active Objects')
    plt.title(rho)
    plt.show()
    
    return m