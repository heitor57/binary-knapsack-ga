import os
from concurrent.futures import ProcessPoolExecutor
import itertools
import yaml

import numpy as np
import pandas as pd

from lib.constants import *
from lib.utils import *
TOP_N = 15
config = yaml.load(open('config.yaml'), Loader=yaml.FullLoader)
parameters = {k: [v['default']] for k, v in config['parameters'].items()}
to_update = {
    "cross_policy": ['BLXa','BLXab'],
    "elitism": [False,True],
    "num_pop": [25,50,100],
    "num_generations": [25,50,100],
    "cross_rate": [0.6,0.8,1.0],
    "mutation_rate": [0.01,0.05,0.1],
    "eid": list(range(1,NUM_EXECUTIONS+1)),
}
parameters.update(to_update)
parameters_names = list(parameters.keys())
combinations = itertools.product(*list(parameters.values()))
# args = [('python genetic_algorithm.py '+' '.join([f'--{k}={v}' for k,v in zip(parameters_names,combination)]),)
 # for combination in combinations]
result_df = pd.DataFrame(columns=parameters_names)
for i,combination in enumerate(combinations):
    p = {k:v for k,v in zip(parameters_names,combination)}
    name = get_parameters_name(p)
    # print(DIRS['DATA']+name+'.json')
    df = pd.read_json(DIRS['DATA']+name+'.json')
    result_df.loc[i,parameters_names] = combination
    result_df.loc[i,'Best fitness'] = df.iloc[-1]['Best fitness']
    result_df.loc[i,'Mean fitness'] = df.iloc[-1]['Mean fitness']
    result_df.loc[i,'Median fitness'] = df.iloc[-1]['Median fitness']
    # if i == 49:
    #     break
result_df['eid']=pd.to_numeric(result_df['eid'])
print('Top best fitness')
print(result_df.groupby(list(set(result_df.columns)-{'Best fitness','Mean fitness','Median fitness', 'eid'})).\
      agg({i: ['mean','std'] for i in {'Best fitness','Mean fitness','Median fitness', 'eid'}}).\
      sort_values(by=[('Best fitness','mean')],ascending=True).reset_index()[list(set(to_update.keys())-{'eid'})+['Best fitness','Mean fitness','Median fitness']].head(TOP_N))

# print('Top mean fitness')
# print(result_df.groupby(list(set(result_df.columns)-{'Best fitness','Mean fitness', 'eid'})).\
#       agg({i: ['mean','median','std'] for i in {'Best fitness','Mean fitness', 'eid'}}).\
#       sort_values(by=[('Mean fitness','mean')],ascending=True).reset_index()[list(set(to_update.keys())-{'eid'})+['Best fitness','Mean fitness']].head(TOP_N))
