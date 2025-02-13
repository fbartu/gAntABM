import numpy as np
import math
from scipy.spatial import distance
import sys, getopt
from parameters import beta, Jij, Theta
import json
import pandas as pd
from itertools import compress


""""""""""""""""""
""" FUNCTIONS  """
""""""""""""""""""

# for appending values in a data frame
def concatenate_values(series):
    return '; '.join(map(str, series))

def check_pos(x):
    xlist = x.split('; ')
    return (lambda y: any('nest' not in element for element in y))(xlist)

def parse_nodestring(nodes):
    nodes = [eval(n)[1] for n in nodes.split('; ')]
    return nodes

def norm_range(x, a = 0, b = 1, as_array = True):
    x = np.array(x)
    min_x = np.min(x)
    max_x = np.max(x)
    result = (b - a) * (x - min_x) / (max_x - min_x) + a
    if not as_array:
        result = list(result)
    return result

def dist(origin, target):
    return distance.euclidean(origin, target)

def get_cos(a, b):
    cosA = (a[0]*b[0] + a[1]*b[1]) / (math.sqrt((a[0]**2 + a[1]**2))*math.sqrt((b[0]**2 + b[1]**2)))
    return cosA

def get_cos_180(a, b):
    cosA = (a[0]*b[0] + a[1]*b[1]) / (math.sqrt((a[0]**2 + a[1]**2))*math.sqrt((b[0]**2 + b[1]**2)))
    return -cosA

def rotate(x, y, theta = math.pi / 2):
    x1 = round(x * math.cos(theta) - y * math.sin(theta), 2)
    y1 = round(x * math.sin(theta) + y * math.cos(theta), 2)
    return x1, y1

def discretize_time(x, t, solve = -1):
    
    x = np.array(x)
    t = np.array(t)
    result = []
    for i in range(int(round(max(t)))):
        idx = np.where((t > (i-1)) & (t <= i))
        if len(idx[0]):

            result.append(np.mean(x[idx]))
        else:
      
            if solve == -1:
                if i > 0:
                    result.append(result[-1])
                else:
                    result.append(0)
     
            else:
                result.append(0)
        
    return result

def moving_average(x, t, overlap = 0, tvec = None):
    
    slide = t // 2
    if overlap > slide:
        overlap = slide
    
    if tvec is None:
            
        x0 = slide
        xn = len(x) - slide - 1
        sq = range(x0, xn, (slide - overlap + 1))
    
        v = [np.mean(x[(i - slide):(i+slide)]) for i in sq]
    
        if overlap == slide:
            return np.concatenate([x[:slide], v, x[xn:len(x)]])
        else:
            return v

    else:
        if len(tvec) != len(x):
            raise ValueError('tvec must have the same length as x')
        
        x = np.array(x)
        tvec = np.array(tvec)

        v = []
        for i in range(np.min(tvec), np.max(tvec), (slide - overlap + 1)):
            idx = np.where((tvec > (i - slide)) & (tvec <= (i + slide)))
            if len(idx[0]):
                v.append(np.mean(x[idx]))
            else:
                v.append(0)
    
        return v

def direction(x):
    x = np.round(np.array(x), 5)
    if np.all(x[2] == x[0]):
        last_move = 'b'
  
    elif np.logical_and(x[2][0] < x[0][0], x[2][1] > x[0][1]):
     
        if x[2][1] > x[1][1]:
            last_move = 'r'
        else:
            last_move = 'l'
    elif np.logical_and(x[2][0] > x[0][0], x[2][1] < x[0][1]):
        if x[2][1] == x[1][1]:
            last_move = 'l'
        else:
            last_move = 'r'
    elif np.logical_and(x[2][0] < x[0][0], x[2][1] < x[0][1]):
        if x[2][1] < x[1][1]:
            last_move = 'l'
        else:
            last_move = 'r'
    elif np.logical_and(x[2][0] > x[0][0], x[2][1] > x[0][1]):
        if x[2][1] == x[1][1]:
            last_move = 'r'
        else:
            last_move = 'l'
  
    else:
        if np.logical_and(x[2][0] == x[0][0], x[2][1] > x[0][1]):
            if x[1][0] > x[2][0]:
                last_move = 'l'
            else:
                last_move = 'r'
        elif np.logical_and(x[2][0] == x[0][0], x[2][1] < x[0][1]):
            if x[1][0] > x[2][0]:
                last_move = 'r'
            else:
                last_move = 'l'
        else:
            print('Unexpected scenario')
            last_move = np.nan
   
    return last_move

def connectivity(grid, nodes):
    nodes = list(filter(lambda n: n != 'nest', list(set(nodes))))
    l = len(nodes)
    clusters = []
    
    while sum(clusters) < l:
        nodes2check = grid.get_neighbors(
        nodes[0],
        include_center = False)
        current_branch = [nodes.pop(0)]
        check = [n in nodes for n in nodes2check]
        while sum(check):
            nodes_in_branch = list(compress(nodes, check))
            current_branch += nodes_in_branch
            nodes = list(filter(lambda n: not n in nodes_in_branch, nodes))
            nodes2check = []
            for n in nodes_in_branch:
                nodes2check += grid.get_neighbors(n, include_center = False)
                
            check = [n in nodes for n in nodes2check]
        clusters += [len(current_branch)]

    return clusters

# assumes a bottom-left node is provided; no error handling !!
def fill_hexagon(node):
    mvs = [np.array([1, 0]), np.array([0, -1]), np.array([0, -1]),
            np.array([-1, 0]), np.array([0, +1])]
    result = [node]
    for i in range(len(mvs)):
        result.append(tuple(result[-1] + mvs[i]))

    return result

def plot_arena(model, data = None, path = None):
    if data is None:
        if path is None:
            print('WARNING: Either path or data is needed; plotting no data...')
            model.plot_lattice()
        else:
            f = open(path)
            data = json.load(f)
   
    df = pd.DataFrame(data)
    a = df['pos'].value_counts().reset_index()
    a.columns = ['pos', 'N']
    a['pos'] = [tuple(i) for i in a['pos']]

    z = [a.loc[a['pos'] == i, 'N'] for i in model.xy]
    zq = np.unique(z, return_inverse = True)[1]
    model.plot_lattice(zq)

def argparser(argv = sys.argv[1:]):
        
    opts, args = getopt.getopt(argv, 'n:d:x:f:p:g:s:i:',
                            ['nruns=', 'directory=', 'filename=', 
                                'food=', 'parameters=',
                            'gains=', 'social_feedbacks=',
                            'init_pos='])

    parameters = {'filename': 'simulation',
               'runs': 1, 'results_path': '../results/',
               'food_condition': 'nf',
               'beta': beta, 'Jij': Jij,
                 'Theta': Theta}

    for opt, arg in opts:
        if opt in ('-n', '--nruns'):
            parameters['runs'] = int(arg)
            
        elif opt in ('-d', '--directory'):
            parameters['results_path'] = arg
            
        elif opt in ('-x', '--filename'):
            parameters['filename'] = arg
            
        elif opt in ('-i', '--init_pos'):
            parameters['init_position'] = arg
            
        elif opt in ('-f', '--food'):
            splarg = arg.split(',')
            parameters['food_condition'] = splarg[0]
            if len(splarg) == 2:
                parameters['d'] = splarg[1]
   
        if opt in ('-s', '--social_feedbacks'):
                parameters['feedback'] = arg
       
        elif opt in ('-p', '--parameters'):
            plist = arg.split(';')
            for p in plist:
                x = p.split('=')
                if x[0] == 'alpha':
                    parameters['alpha'] = eval(x[1])
                elif x[0] == 'beta':
                    parameters['beta'] = eval(x[1])
                elif x[0] == 'gamma':
                    parameters['gamma'] = eval(x[1])
                elif x[0] == 'Jij':
                    j = eval(x[1])
                    if type(j) == dict:
                        if j.keys() == Jij.keys():
                            parameters['Jij'] = j
                elif x[0] == 'Theta':
                    parameters['Theta'] = eval(x[1])
                elif x[0] == 'g':
                    parameters['g'] = arg
                elif x[0] == 'rho':
                    parameters['rho'] = eval(x[1])
                elif x[0] == 'epsilon':
                    parameters['epsilon'] = eval(x[1])
                elif x[0] == 'init_position':
                    parameters['init_position'] = str(x[1])
                else:
                    print('Unknown parameter', x[0], flush= True)
                    try:
                        parameters[x[0]] = eval(x[1])
                    except:
                        print('Could not add parameter', x[0], flush = True)
        elif opt in ('-g', '--gains'):
            parameters['g'] = arg
            
    return parameters
