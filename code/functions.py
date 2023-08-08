import numpy as np
import math
from scipy.spatial import distance
import sys, getopt
from parameters import alpha, beta, gamma



""""""""""""""""""
""" FUNCTIONS  """
""""""""""""""""""

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
		last_move = 0
  
	elif np.logical_and(x[2][0] < x[0][0], x[2][1] > x[0][1]):
	 
		if x[2][1] > x[1][1]:
			last_move = 1
		else:
			last_move = -1
	elif np.logical_and(x[2][0] > x[0][0], x[2][1] < x[0][1]):
		if x[2][1] == x[1][1]:
			last_move = -1
		else:
			last_move = 1
	elif np.logical_and(x[2][0] < x[0][0], x[2][1] < x[0][1]):
		if x[2][1] < x[1][1]:
			last_move = -1
		else:
			last_move = 1
	elif np.logical_and(x[2][0] > x[0][0], x[2][1] > x[0][1]):
		if x[2][1] == x[1][1]:
			last_move = 1
		else:
			last_move = -1
  
	else:
		if np.logical_and(x[2][0] == x[0][0], x[2][1] > x[0][1]):
			if x[1][0] > x[2][0]:
				last_move = -1
			else:
				last_move = 1
		elif np.logical_and(x[2][0] == x[0][0], x[2][1] < x[0][1]):
			if x[1][0] > x[2][0]:
				last_move = 1
			else:
				last_move = -1
		else:
			print('Unexpected scenario')
			last_move = np.nan
   
	return last_move

# assumes a bottom-left node is provided; no error handling !!
def fill_hexagon(node):
	mvs = [np.array([1, 0]), np.array([0, -1]), np.array([0, -1]),
			np.array([-1, 0]), np.array([0, +1])]
	result = [node]
	for i in range(len(mvs)):
		result.append(tuple(result[-1] + mvs[i]))

	return result


def argparser(argv = sys.argv[1:]):
    
	opts, args = getopt.getopt(argv, 'n:d:x:f:m:j:p:g:',
							['nruns=', 'directory=', 'filename=', 
								'food=', 'movement=', 'memory=', 'parameters=',
        					'gains='])

	parameters = {'filename': 'simulation',
               'runs': 1, 'results_path': '../results/',
               'food_condition': 'sto_1',
               'alpha': alpha, 'beta': beta, 'gamma': gamma}

	for opt, arg in opts:
		if opt in ('-n', '--nruns'):
			parameters['runs'] = int(arg)
			
		elif opt in ('-d', '--directory'):
			parameters['results_path'] = arg
			
		elif opt in ('-x', '--filename'):
			parameters['filename'] = arg
			
		elif opt in ('-f', '--food'):
			parameters['food_condition'] = arg
			
		elif opt in ('-m', '--movement'):
			parameters['default_movement'] = arg
			
		elif opt in ('-p', '--parameters'):
			plist = arg.split(',')
			for p in plist:
				x = p.split('=')
				if x[0] == 'alpha':
					parameters['alpha'] = float(x[1])
				elif x[0] == 'beta':
					parameters['beta'] = float(x[1])
				elif x[0] == 'gamma':
					parameters['gamma'] = float(x[1])
				else:
					print('Unknown parameter', x[0])
		elif opt in ('-g', '--gains'):
			parameters['g'] = arg
		elif opt in ('-j', '--states'):
			parameters['memory'] = arg
			
	return parameters
