import sys
import getopt
from Model import *
Jij = {'0-0': 1,'1-1': 1,'1-0': 1,'0-1': 1}

def argparser(argv = sys.argv[1:]):
		
	opts, args = getopt.getopt(argv, 'n:d:x:f:m:p:g:r:s:i:',
							['nruns=', 'directory=', 'filename=', 
								'food=', 'movement=', 'parameters=',
							'gains=', 'recruitment=', 'social_feedbacks=',
							'init_pos='])

	parameters = {'filename': 'simulation',
			   'runs': 1, 'results_path': '../results/',
			   'food_condition': 'det',
			   'beta': beta, 
				  'Jij': Jij,
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
			
		elif opt in ('-m', '--movement'):
			parameters['default_movement'] = arg
   
		elif opt in ('-r', '--recruitment'):
			parameters['recruitment'] = eval(arg)
   
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

if __name__ == '__main__':
	params = argparser()
	print(params, flush=True)
	m = Model(**params)
	for i in params:
		if hasattr(m, i):
			print(i, getattr(m, i))
		else:
			if hasattr(m.agents[0], i):
				print(i, getattr(m.agents[0], i))
			else:
				print('Model has no attribute', i)
	sys.exit(0)