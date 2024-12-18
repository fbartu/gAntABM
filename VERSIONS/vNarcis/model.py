from gillespie import GillespieAlgorithm
from agent import *
import json
import numpy as np
import pandas as pd

class Model(GillespieAlgorithm):

    def __init__(self, n_agents, recruitment_strategy, environment, steps, path, filename):

        ants = list(Ant(a, recruitment_strategy) for a in list(range(n_agents)))
        '''
        Experimentation !!
        ants[0].pos = list(environment.food.keys())[0]
        ants[0].r_i = params.omega
        ants[0].state = State.RECRUITING
        ants[0].prev_state = State.RECRUITING
        environment.out_nest[0] = 0
        del environment.waiting_ants[0]
        '''
        super().__init__(ants, environment)

        self.steps = steps
        self.path = path
        self.filename = filename
    
    def run(self):

        print('+++ RUNNING MODEL +++')
        if self.steps == 0:
            i = 0
            while self.T[-1] < 10800:
                i+=1
                if i % 2000 == 0:
                    print('Iteration ', str(i))
                    
                self.step()
        
        else:
            for i in list(range(self.steps)):
                if i % 2000 == 0:
                    print('Iteration ', str(i))
                self.step()
            
        print('Model completed... Saving results !')

        self.save_data()
        print('+++ Results saved +++')

    def time2minutes(self):
        self.T = [t / 60.0 for t in self.T]

    def retrieve_positions(self):
        # result = {'agent': [],'pos': [],'t': [], 'state': [], 'tag': [], 'mia': []}
        result = {'agent': [],'pos': [],'t': [], 'state': []}
        for i in range(len(self.agents)):
            result['agent'].extend([i] * len(self.agents[i].path))
            result['pos'].extend(self.agents[i].path)
            result['t'].extend(list(map(self.T.__getitem__, np.where(self.sample == np.array([i]))[0])))
            if len(self.agents[i].state_history) > 1:
                result['state'].extend(self.agents[i].state_history)
            #result['tag'].extend(self.agents[i].tag)
            #result['mia'].append(self.agents[i].MIA)
        
        return result

    def save_data(self):
        cols = list(self.population.columns)
        try:
            cols.remove('W')
            self.population[State.WAITING] = len(self.agents) - self.population[cols]
        except:
            pass
        
        self.results = [{'Time (s)': self.T,
        # 'Connectivity': self.K,
        'N': self.N,
        'Interactions': self.I,
        'Food in nest': self.F,
        'Exploring from food': self.population[State.EXPLORING_FROM_FOOD],
        #'Informed': self.population[Tag.INFORMED],
        'Waiting': self.population[State.WAITING],
        'Carrying food': self.population[[State.EXPLORING_FOOD, State.RECRUITING_FOOD]].sum(axis = 1),
        'Exploring': self.population[State.EXPLORING],
        'Recruiting': self.population[State.RECRUITING]},
        self.metrics.efficiency(self.tfood),
        self.retrieve_positions()]
        
    def data2json(self, folder = '', filename = 'Run_1', get_pos = False):    
        
        if not hasattr(self, 'results'):
            self.save_data()

        pd.DataFrame(self.results[0]).to_csv(self.path + 'results/' + folder + filename + '_data.csv')

        # with open(self.path + 'results/' + folder + filename + '_data.json', 'w') as f:
        #     json.dump(self.results[0], f)

        with open(self.path + 'results/' + folder + filename + '_food.json', 'w') as f:
            json.dump(self.results[1], f)

        if get_pos:
            
            with open(self.path + 'results/' + folder + filename + '_pos.json', 'w') as f:
                json.dump(self.results[2], f)


