# coding: utf-8
import numpy as np
import pandas as pd
import yaml

import math
import random
import argparse
import collections
import sys
from pathlib import Path
import os

from lib import *


parser = argparse.ArgumentParser()
config = yaml.load(open('config.yaml'), Loader=yaml.FullLoader)
config['cross_policy'] = collections.defaultdict(dict,config['cross_policy'])
parameters = config['parameters']

for k, v in parameters.items():
    parser.add_argument('--'+k,default=v['default'],
                        type=str2bool if type(v['default']) == bool else type(v['default']))

args = parser.parse_args()
for k,v in vars(args).items():
    locals()[k] = v
    parameters[k]['value'] = v
    
num_cross = int((cross_rate * num_pop)/2)
num_no_cross = num_pop-2*num_cross

# information to catch from algorithm
binary_knapsack = BinaryKnapsack()
binary_knapsack.load(DIRS['INPUT']+parameters['instance_name']['value'])
objective = BinaryKnapsackObjective(binary_knapsack)
cross_policy = eval(parameters['cross_policy']['value'])(**config['cross_policy'][parameters['cross_policy']['value']])
mutation_policy = eval(parameters['mutation_policy']['value'])(mutation_rate)

population = []
for i in range(num_pop):
    ind = Individual()
    ind.rand_genome_bool(len(binary_knapsack.weights))
    population.append(ind)
    objective.compute(ind)

columns = ['#Generation','Best fitness','Mean fitness', 'Median fitness', 'Worst fitness']
df = pd.DataFrame([],columns = columns)
df = df.set_index(columns[0])

best_ind = population[np.argmax([ind.ofv if binary_knapsack.is_viable(ind.genome) else np.finfo(ind.ofv.dtype).min  for ind in population ])]
ofvs = [ind.ofv for ind in population]
df.loc[1] = [f'{best_ind.ofv:.4f}',f'{np.mean(ofvs):.4f}',f'{np.median(ofvs):.4f}',f'{np.min(ofvs):.4f}']
for i in range(2,num_generations+1):

    new_population = []
    # Cross
    selection_policy=eval(parameters['selection_policy']['value'])(population)
    for j in range(num_cross):
        ind1=selection_policy.select()
        ind2=selection_policy.select()
        nind1, nind2 = cross_policy.cross(ind1,ind2)
        new_population.append(nind1)
        new_population.append(nind2)
    # Select the rest left of individuals if the cross rate is not 100%
    new_population.extend([population[i].__copy__()
                           for i in random.sample(list(range(len(population))),num_no_cross)])

    # Mutate these new individuals - Mutation
    for j in range(num_pop):
        mutation_policy.mutate(new_population[j])

    # Select best individual from previous population - Elitism
    if elitism:
        new_population[random.randint(0,len(new_population)-1)]=best_ind.__copy__()
    population = new_population

    for ind in population:
        objective.compute(ind)
        
    best_ind = population[np.argmax([ind.ofv if binary_knapsack.is_viable(ind.genome) else np.finfo(ind.ofv.dtype).min  for ind in population ])]
    ofvs = [ind.ofv for ind in population]
    df.loc[i] = [f'{best_ind.ofv:.4f}',f'{np.mean(ofvs):.4f}',f'{np.median(ofvs):.4f}',f'{np.min(ofvs):.4f}']
df = df.reset_index()

if config['general']['print_table']:
    # PRINT TABLE BLOCK
    parameters_print = {key: val
                        for key, val
                        in zip([i['pretty_name'] for i in parameters.values()],
                            [i['value'] for i in parameters.values()])}
    column_names_size = []
    max_size = max(map(len,parameters_print.keys()))
    max_size_val = max(map(len,map(str,parameters_print.values())))

    print(Colors.DARK,end='')

    for key, value in parameters_print.items():
        print(Colors.Backgrounds.MAGENTA+key+' '*(max_size-len(key)),
            Colors.Backgrounds.BLUE+str(value)+' '*(max_size_val-len(str(value)))+Colors.RESET_BACKGROUND)
    SPACED_STR = '   '
    for i, col in enumerate(columns):
        col =SPACED_STR + col + SPACED_STR
        print(COLORS[i],end='')
        if i != 0:
            print(col,end='')
        else:
            print(col,end='')
        print(Colors.RESET_BACKGROUND,end='')
        column_names_size.append(len(col))
    print()
    for index, row in df.iterrows():
        print(Colors.Backgrounds.WHITE,end='')
        for j, item in enumerate(row.T.to_list()):
            item = str(item)
            print(item,end='')
            size = len(item)
            print(" "*(len(columns[j]+SPACED_STR*2)-size),end='')

        print(Colors.RESET_BACKGROUND)

    print(Colors.RESET,end='')


string=get_parameters_name({k: v['value'] for k,v in parameters.items()})
Path(os.path.dirname(DIRS['RESULT']+string)).mkdir(parents=True, exist_ok=True)

fout = open(DIRS['RESULT']+string+'.json','w')
fout.write(df.to_json(orient='records',lines=False))
fout.close()

print(f"Optimal solution OFV is {objective.compute(Individual(genome=binary_knapsack.optimal_solution)):.2f}")
