import sys

import numpy as np

class SelectionPolicy:
    def __init__(self,population):
        self.population = population

class Tournament(SelectionPolicy):
    def select(self):
        population=self.population
        fathers = []
        for i in range(2):
            inds = []
            for j in range(2):
                inds.append(random.randint(0,num_pop-1))
                ind = None
                get_winner = np.random.rand() <= winner_prob
            if population[inds[0]].ofv < population[inds[1]].ofv:
                ind = population[inds[0]]
                if not get_winner:
                    ind = population[inds[1]]
            else:
                ind = population[inds[1]]
                if not get_winner:
                    ind = population[inds[0]]

            fathers.append(ind)
        return fathers

class Roulette(SelectionPolicy):
    def __init__(self,population):
        super().__init__(population)
        ofvs = np.array([ind.ofv for ind in self.population])
        ofvs = 1/(ofvs+1/np.finfo(ofvs.dtype).max)
        self.probabilities = ofvs/np.sum(ofvs)
    def select(self):
        r = np.random.random()
        cumulated = 0
        chosen_ind = None
        for p, ind in zip(self.probabilities,self.population):
            cumulated += p
            if cumulated >= r:
                chosen_ind = ind
                break
        return chosen_ind


class RankRoulette(SelectionPolicy):
    def __init__(self,population):
        super().__init__(population)
        indexes = np.argsort([ind.ofv for ind in self.population])
        i=1
        ranks = np.zeros(len(self.population))
        for index in indexes:
            ranks[index] = i
        self.probabilities = ranks/np.sum(ranks)
    def select(self):
        r = np.random.random()
        cumulated = 0
        chosen_ind = None
        for p, ind in zip(self.probabilities,self.population):
            cumulated += p
            if cumulated >= r:
                chosen_ind = ind
                break
        return chosen_ind
