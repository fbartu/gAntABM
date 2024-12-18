import sys, getopt
import re
import params

def argparse(argv):

    error_msg_rec = 'Recruitment misspecified ! Check possible options in help or params.py'
    error_msg_float = 'Parameter must be a float number !'
    error_msg_int = 'Parameter must be an integer !'
    error_msg_bool = 'Parameter must be a boolean !'
    wrng_msg_1 = 'Leaving default parameter value ...'
    wrng_msg_2 = 'Exiting program ...'

    
    try:

        if '-h' in argv or '--help' in argv:
            if 'summary' in argv or bool(re.findall('e_', ''.join(argv))):
                pass
            else:
                try:
                    idx = argv.index('-h')
                except:
                    idx = argv.index('--help')
                argv.insert(idx + 1, 'NONE')

        opts, args = getopt.getopt(argv, 'p:f:r:n:m:h:x:d:',
         ["params=", "food=", "recruitment=", "nruns=", "mvfood=","help=", "filename=","directory=","foodamount="])

    except getopt.GetoptError:
        print('Something went wrong ! Try typing -h or --help to see possible parameters.')
        print(wrng_msg_2)
        sys.exit(2)

    if '--foodamount' in dict(opts).keys():
        try:
            globals()['params'].foodXvertex = int(dict(opts)['--foodamount'])
        except:
            print(error_msg_int)
            print(wrng_msg_1)

    for opt, arg in opts:

        if opt in ('-p', '--params'):
            paramlist = arg.split(',')
            for param in paramlist:
                param = param.split('=')
                if hasattr(globals()['params'], param[0]):
                    try:
                        setattr(globals()['params'], param[0], float(param[1]))
                    except:
                        print(error_msg_float)
                        print(wrng_msg_1)
                
                else:
                    print('Parameter ' + str(param[0]) + ' not found in params.py')
                    print(wrng_msg_1)
        
        if opt in ('-f', '--food'):
            # find by tuples
            pos = re.findall(r'\[(.*?,.*?)\]', arg)
            pos = [(int(i[0]), int(i[2])) for i in pos]
            globals()['params'].food = dict.fromkeys(pos, globals()['params'].foodXvertex)

        if opt in ('-r', '--recruitment'):

            arg = arg.split(',')
            if len(arg) == 1:
                globals()['params'].recruitment = (''.join(arg), '')
            
            elif len(arg) == 2:
                globals()['params'].recruitment = (''.join(arg[0]), ''.join(arg[1]))

            else:
                print(error_msg_rec)
                print(wrng_msg_1)

        if opt in ('-n', '--nruns'):

            l = arg.split(',')
            try:
                globals()['params'].n_runs = int(l[0])
            
            except:
                print(error_msg_int)
                print(wrng_msg_1)

            if len(l) == 2:

                if l[1] == 'True' or l[1] == '1':
                    globals()['params'].run_parallel = True

                elif l[1] == 'False' or l[1] == '0':
                    globals()['params'].run_parallel = False

                else:
                    print(error_msg_bool)
                    print(wrng_msg_1)

        if opt in ('-m', '--mvfood'):
            l = arg.split(',')
            try:
                l = (int(l[0]), int(l[1]))
                if sum(l) % 2 == 0:
                    fk = globals()['params'].food.keys()
                    food = [(i[0] + l[0], i[1] + l[1]) for i in list(fk)]
                    globals()['params'].food = dict.fromkeys(food, globals()['params'].foodXvertex)
                else:
                    print('Sum of coordinates must be even !')
                    print(wrng_msg_1)
                    
            except:
                print('Parameter must be two integers, whose sum must be even !')
                print(wrng_msg_1)

        if opt in ('-x', '--filename'):
            globals()['params'].file_name = arg

        if opt in ('-d', '--directory'):

            try:

                splt = arg.split('/')
                if len(splt) == 1:
                    globals()['params'].folder = str(params.path) + str(arg)
                    print('Set results directory to: ' + str(params.path) + str(arg))

                else:
                    if splt[-1] == '':
                        splt = splt[:-1]
                    
                    if len(splt) == 1:
                            globals()['params'].folder = str(params.path) + str(arg)
                            print('Set results directory to: ' + str(params.path) + str(arg))
                    else:
                        globals()['params'].folder = '/'.join(splt) + '/'
                        print('Set results directory to: ' + '/'.join(splt) + '/')
            
            except:

                print('Something went wrong !!!')
                print(wrng_msg_1)

        if opt in ('-h', '--help'):
            print('\n')
            print('HELP HAS BEEN SUMMONED !!')

            if arg == 'summary':
                print('The possible options are:')
                print('\n')
                print('-p or --param to change individual or multiple cellular automata parameters')
                print('-f or --food to specify food node positions (as list of coordinates)')
                print('-r or --recruitment to specify recruitment strategy')
                print('-n or --nruns to set the number of runs (replicas) and whether they should be run in parallel')
                print('-m or --mvfood to move food position, relative to the default position')
                print('-x or --filename to set the name to save the output from the model')
                print('-d or --directory to set the folder to which the results will be saved')
                print('--foodamount to set the number of foodpieces per node')

            elif arg.split('_')[0] == 'e':
                arg = arg.split('_')
                for a in arg[1:]:
                    if a in ('p', 'param'):
                        print('-p or --param for parameter change:')
                        print('\t list of parameters that must be typed like parameter1=value,parameter2=value,parameter3=value')
                        print('\t EXAMPLE: eta=0.05,gamma_1=1.2 ; <- this will set parameters eta to 0.05 and gamma_1 to 1.2')
                        print('\t EXAMPLE: mu=1,gamma_1=0.5,gamma_2=1.5,alpha=0 ; <- this will set parameters mu to 1.0, gamma_1 to 0.5, gamma_2 to 1.5 and alpha to 0.0')
                        print('\t if any paramater is misspecified or ignored, parameter value will be left by default.')
                        print('\t notice each pair parameter value is separated by = symbol, whilst pairs are separated by commas. Avoid using spaces !')
                    
                    elif a in ('f', 'food'):
                        print('-f or --food for specifying food positions:')
                        print('\t list of food nodes provided as a set of coordinates. Must be typed like [x1,y1],[x2,y2],[x3,y3]')
                        print('\t the amount of food per node is controlled by --foodamount (or foodXvertex in params.py)')
                        print('\t note that each node position is specified individually')
                        print('\t EXAMPLE: [5,34],[5,35],[6,35],[6,34],[6,33],[5,33]; <- this will set food to be a dictionary with X number of food pieces in each of these nodes.') 
                        

                    elif a in ('r', 'recruitment'):
                        print('-r or --recruitment to specify recruitment type')
                        print('\t list of two elements; the recruitment strategy and whether recruitment is parallel or not')
                        print('\t the options are: ')
                        print('\t parameter 1:')
                        print('\t \t NR: No recruitment')
                        print('\t \t IR: Individual recruitment (a single ant is recruited)')
                        print('\t \t GR: Group recruitment (3 to 5 ants are recruited)')
                        print('\t \t HR: Hybrid recruitment (0 to 5 ants are recruited)')
                        print('\t \t Any other value will set recruitment to "No recruitment" !!!')
                        print('\t parameter 2:')
                        print('\t \t s: Serial recruitment (explotation of food patches does not occur simultaneously)')
                        print('\t \t else: Any other value will lead to default behaviour')
                        print('\t EXAMPLE: GR,s; <- this will set recruitment strategy to Group Recruitment, and "serial behaviour" will be triggered (recruits that do not find food will return to nest)')
                        print('\t EXAMPLE: GR; <- this will set recruitment strategy to Group Recruitment, with default ant behaviour.')
                        print('\t EXAMPLE: GR,whatever; <- this will set recruitment strategy to Group Recruitment, with default ant behaviour.')
                        print('\t EXAMPLE: ,; <- this will set recruitment strategy to No recruitment. Beware !')


                    elif a in ('n', 'nruns'):
                        print('-n or --nruns to specify number of runs (replicas) and whether or not to run in parallel')
                        print('\t list of the kind integer,boolean (1 or 0 will be read as True or False respectively).')
                        print('\t a single run will not be run in parallel in any case.')
                        print('\t EXAMPLE: 100,True; <- This will set 100 runs in parallel')
                        print('\t EXAMPLE: 1,0; <- This will set a single run')
                        print('\t EXAMPLE: 5,False; <- This will set 5 sequential (non-parallel) runs')

                    elif a in ('m', 'mvfood'):
                        print('-m or --mvfood to move the foodpatches across the grid')
                        print('\t a pair of integer values: x,y; whose sum must be even, to displace patches in number of hexagons')
                        print('\t sum must be even to ensure the displacement involves a whole hexagon')
                        print('\t this would be a lazy option to set the foodpatches by counting hexagons, instead of setting manual positions for each node')
                        print('\t before using this option, it is recommended to watch a plot of the grid to fully understand the behaviour of this function')
                        print('\t first coordinate (x) is positive displacement to the left, and negative displacement to the right')
                        print('\t second coordinate (y) is positive displacement up, and negative displacement down')
                        print('\t EXAMPLE: 1,-1; <- This would move all nodes one node to the left (1) and one node down (-1)')
                        print('\t EXAMPLE: -4,7; <- This would move all nodes four nodes to the right (-4) and six nodes up (6)')
                        print('\t EXAMPLE: 1,-4; <- This will not work, as 1-4 = 3, which is not an even number')

                    elif a in ('x', 'filename'):
                        print('-x or --filename to set the name to save the output from the model')
                        print('\t a string that will be used as name for the output file of the model')
                        print('\t the extension must NOT be written; each data file will have the corresponding format appended')
                        print('\t EXAMPLE: distance_experiment; <- this will set "distance_experiment" as file name')
                        print('\t EXAMPLE: distance_experiment.csv; <- this will set "distance_experiment.csv" as file name, but the format will not necessarily .csv (a suitable extension is appended to the filename)')

                    elif a in ('d','directory'):
                        print('-d or --directory to set the folder to which the results will be saved')
                        print('\t a string with the whole path to the folder, or just the folder name')
                        print('\t the default directory to create the folder into is "~/research/AutomatAnts/results/"')
                        print('\t EXAMPLE: distance_experiment; <- this will set the result directory to "~/research/AutomatAnts/results/distance_experiment/"')
                        print('\t EXAMPLE:"~/research/AutomatAnts/results/distance_experiment/"; <- this is equivalent to the previous example')
                        print('\t EXAMPLE: "/home/user1/results/"; <- this will set the result directory to "/home/user1/results/"')

                    elif a == 'foodamount':
                        print('--foodamount to set the number of foodpieces per node in the food dictionary')
                        print('\t an integer is expected') 
                        print('\t EXAMPLE: 5; <- this will set 5 pieces of food to each node present in the food dictionary')
                        print('\t EXAMPLE: 0; <- this will set 0 pieces of food to each node present in the food dictionary')

                    else:
                        print('WARNING !!! Specified parameter "' + str(a) + '" not found !')

                    print('\n')

            else:

                print('For a shorter version, it is possible to call -h summary')
                print('\n')
                print('For examples, you can type -h e_@parameter (i.e -h e_param; -h e_recruitment)')
                print('Both short and long options can be used (alternatives would be -h e_p; -h e_r)')
                print('Multiple examples can be displayed at once (i.e -h e_p_r)')
                print('\n')
                print('\n')
                print('The list of possible parameters to change are:')
                print('\n')
                print('-p or --param for parameter change:')
                print('\t list of parameters that must be typed like parameter1=value,parameter2=value,parameter3=value')
                print('\t if any paramater is misspecified or ignored, parameter value will be left by default.')
                print('\t notice each pair parameter value is separated by "=" symbol, whilst pairs are separated by commas (",").')
                print('\t Avoid using spaces !!! Otherwise it will not work properly.')
                print('\n')
                print('---------------------------------------')
                print('\n')
                print('-f or --food for specifying food positions:')
                print('\t list of food nodes provided as a set of coordinates. Must be typed like [x1,y1],[x2,y2],[x3,y3]')
                print('\t The amount of food per node is controlled by --foodamount (or foodXvertex in params.py)')
                print('\t note that each node position is specified individually')
                print('\n')
                print('---------------------------------------')
                print('\n')
                print('-r or --recruitment to specify recruitment type')
                print('\t list of two elements; the recruitment strategy and whether recruitment is parallel or not')
                print('\t the options are: ')
                print('\t parameter 1:')
                print('\t \t NR: No recruitment')
                print('\t \t IR: Individual recruitment (a single ant is recruited)')
                print('\t \t GR: Group recruitment (3 to 5 ants are recruited)')
                print('\t \t HR: Hybrid recruitment (0 to 5 ants are recruited)')
                print('\t \t Any other value will set recruitment to "No recruitment" !!!')
                print('\t parameter 2:')
                print('\t \t s: Serial recruitment (explotation of food patches does not occur simultaneously)')
                print('\t \t else: Any other value will lead to default behaviour')
                print('\n')
                print('---------------------------------------')
                print('\n')
                print('-n or --nruns to specify number of runs (replicas) and whether or not to run in parallel')
                print('\t list of the kind integer,boolean (1 or 0 will be read as True or False respectively)')
                print('\t a single run will not be run in parallel in any case.')
                print('\n')
                print('---------------------------------------')
                print('\n')
                print('-m or --mvfood to move the foodpatches across the grid')
                print('\t a pair of integer values: x,y; whose sum must be even, to displace patches in number of hexagons')
                print('\t sum must be even to ensure the displacement involves a whole hexagon')
                print('\t this would be a lazy option to set the foodpatches by counting hexagons, instead of setting manual positions for each node')
                print('\t before using this option, it is recommended to watch a plot of the grid to fully understand the behaviour of this function')
                print('\t first coordinate (x) is positive displacement to the left, and negative displacement to the right')
                print('\t second coordinate (y) is positive displacement up, and negative displacement down')
                print('\n')
                print('---------------------------------------')
                print('\n')
                print('-x or --filename to set the name to save the output from the model')
                print('\t a string that will be used as name for the output file of the model')
                print('\t the extension must NOT be written; each data file will have the corresponding format appended')
                print('\n')
                print('---------------------------------------')
                print('\n')
                print('-d or --directory to set the folder to which the results will be saved')
                print('\t a string with the whole path to the folder, or just the folder name')
                print('\t the default directory to create the folder into is "~/research/AutomatAnts/results/"')
                print('\n')
                print('---------------------------------------')
                print('\n')
                print('--foodamount to set the number of foodpieces per node in the food dictionary')
                print('\t an integer is expected') 

            print('\n')
            print('---------------------------------------')
            print('\n')    
            print('\n')
            print('HELP ENDS HERE ... Exiting program.')
            sys.exit(0)