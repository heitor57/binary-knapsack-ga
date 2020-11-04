import numpy as np
from .Individual import *

class CrossPolicy:
    pass

class BLXa(CrossPolicy):
    def __init__(self,min_value,max_value,alpha):
        self.alpha=alpha
        self.min_value=min_value
        self.max_value=max_value
    def cross(self,ind1,ind2):
        nind1= Individual(genome=[0]*len(ind1.genome))
        nind2= Individual(genome=[0]*len(ind1.genome))
        i = 0
        for gene1, gene2 in zip(ind1.genome,ind2.genome):
            d= abs(gene1-gene2)
            min_value = min(gene1,gene2)
            max_value = max(gene1,gene2)
            nind1.genome[i] = min(max(random.uniform(min_value-self.alpha*d,max_value+self.alpha*d),self.min_value),self.max_value)
            nind2.genome[i] = min(max(random.uniform(min_value-self.alpha*d,max_value+self.alpha*d),self.min_value),self.max_value)
            i+=1

        return nind1, nind2

class BLXab(CrossPolicy):
    def __init__(self,min_value,max_value,alpha,beta):
        self.alpha=alpha
        self.beta=beta
        self.min_value=min_value
        self.max_value=max_value

    def cross(self,ind1,ind2):
        nind1= Individual(genome=[0]*len(ind1.genome))
        nind2= Individual(genome=[0]*len(ind1.genome))
        if ind1.ofv > ind2.ofv:
            ind1, ind2 = ind2, ind1

        i = 0
        for gene1, gene2 in zip(ind1.genome,ind2.genome):
            d= abs(gene1-gene2)
            if gene1 <= gene2:
                nind1.genome[i]=min(max(random.uniform(gene1-self.alpha*d,gene2+self.beta*d),self.min_value),self.max_value)
                nind2.genome[i]=min(max(random.uniform(gene1-self.alpha*d,gene2+self.beta*d),self.min_value),self.max_value)
            else:
                nind1.genome[i]=min(max(random.uniform(gene2-self.beta*d,gene1+self.alpha*d),self.min_value),self.max_value)
                nind2.genome[i]=min(max(random.uniform(gene2-self.beta*d,gene1+self.alpha*d),self.min_value),self.max_value)
            i+=1

        return nind1, nind2


class CrossPoint(CrossPolicy):
    def __init__(self):
        pass

    def cross(self,ind1,ind2):
        nind1= Individual(genome=np.zeros(len(ind1.genome),type=np.bool))
        nind2= Individual(genome=np.zeros(len(ind1.genome),type=np.bool))
        idx = random.randint(1,len(ind1.genome)-2)

        new_genome = ind1.genome[:idx]
        new_genome.append(ind2.genome[idx:])
        nind1 = Individual(new_genome)

        new_genome = ind1.genome[idx:]
        new_genome.append(ind2.genome[:idx])
        nind2 = Individual(new_genome)
        return nind1, nind2
