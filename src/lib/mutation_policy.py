import random
class MutationPolicy:
    pass

class UniformRandomSolutionSpace(MutationPolicy):
    def __init__(self,probability,min_value,max_value):
        self.probability = probability
        self.min_value = min_value
        self.max_value = max_value
    
    def mutate(self,ind):
        new_genome = [random.uniform(self.min_value,self.max_value)
                      if self.probability > random.random()
                      else
                      i
                      for i in ind.genome]
        ind.genome = new_genome


class OneGene(MutationPolicy):
    def __init__(self,probability,min_value,max_value):
        self.probability = probability
        self.min_value = min_value
        self.max_value = max_value
    
    def mutate(self,ind):
        if self.probability > random.random():
            i = random.randint(0,len(ind.genome)-1)
            ind.genome[i] = random.uniform(self.min_value,self.max_value)

class InvertBit(MutationPolicy):
    def __init__(self,probability):
        self.probability = probability
    
    def mutate(self,ind):
        new_genome = np.array([not i
                               if self.probability >= random.random()
                               else
                               i
                               for i in ind.genome],dtype=np.bool)
        ind.genome = new_genome

