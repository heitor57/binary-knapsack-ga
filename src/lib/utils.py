import os
import multiprocessing
from concurrent.futures import ProcessPoolExecutor

from tqdm import tqdm
import numpy as np

from .constants import *

def dict_to_list_gen(d):
    for k, v in zip(d.keys(), d.values()):
        if v == None:
            continue
        if type(v) == dict: 
            v = '{'+get_parameters_name(v,num_dirs=0)+'}'
        yield [k,v]

def dict_to_list(d):
    return list(dict_to_list_gen(d))

def get_parameters_name(parameters,num_dirs=0):
    # parameters = {k:v for k,v in parameters if v}
    list_parameters=['_'.join(map(str,i)) for i in dict_to_list(parameters)]
    string = '/'.join(list_parameters[:num_dirs]) +\
        ('/' if num_dirs else '')
    string += '_'.join(list_parameters[num_dirs:])
    return string

if __name__ == '__main__':
    print(get_parameters_name({'a':2, 'b':3}))
    print(get_parameters_name({'a':2, 'b':3,'d':{'alpha':1, 'xd':{'s':5}}}))
    pass

def run_parallel(func, args,chunksize = None,use_tqdm=True):
    executor = ProcessPoolExecutor()
    num_args = len(args)
    if not chunksize:
        chunksize = int(num_args/multiprocessing.cpu_count())
    if use_tqdm:
        ff = tqdm
    else:
        ff = lambda x,*y,**z: x 
    results = [i for i in ff(executor.map(func,*list(zip(*args)),chunksize=chunksize),total=num_args)]
    return results

def str2bool(v):
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')
