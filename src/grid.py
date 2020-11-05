import os
from concurrent.futures import ProcessPoolExecutor
import itertools

import numpy as np

from lib.constants import *
from lib.utils import *

parameters = {
    "elitism": [False,True],
    "num_generations": [25,50,100],
    "num_pop": [25,50,100],
    "cross_rate": [0.6,0.8,1.0],
    "mutation_rate": [0.01,0.05,0.1],
    "instance_name": ["p01","p02","p03","p03","p04","p05","p06","p07","p08"],
    "eid": list(range(1,NUM_EXECUTIONS+1)),
}
parameters_names = list(parameters.keys())
combinations = itertools.product(*list(parameters.values()))
args = [('python genetic_algorithm.py '+' '.join([f'--{k}={v}' for k,v in zip(parameters_names,combination)]),)
 for combination in combinations]
run_parallel(os.system,args,chunksize=20)
