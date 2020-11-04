import numpy as np
class BinaryKnapsack:
    def __init__(self, capacity=0, weights=[], utilities=[], optimal_solution=[]):
        self.capacity = capacity
        self.weights = weights
        self.utilities = utilities
        self.optimal_solution = optimal_solution
    def load(self, instance_name):
        self.capacity=int(open(instance_name+"_c.txt").read())
        for line in open(instance_name+"_w.txt"):
            self.weights.append(int(line))
        for line in open(instance_name+"_p.txt"):
            self.utilities.append(int(line))
        for line in open(instance_name+"_s.txt"):
            self.optimal_solution.append(bool(int(line)))
        self.optimal_solution=np.array(self.optimal_solution)
        self.utilities=np.array(self.utilities)
        self.weights=np.array(self.weights)
    def is_viable(self,solution):
        return True if np.sum(self.weights[solution])<=self.capacity else False
        
    def __str__(self):
        return f"""{self.capacity}
w={self.weights}
u={self.utilities}
optimal={self.optimal_solution}"""
