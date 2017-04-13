from collections import deque
import individu

class Pool(object):
    """Population de (n) snakes à tester et à croiser
    
    Attributes:
        n (int): Taille de la population
        population (deque): ensemble des N individus de la populations
    """
    def __init__(self, n):
        super(Pool, self).__init__()
        self.n = n
        self.population = deque()
        for i in range(0,self.n):
            self.population.append(individu())

    def getFitnessMax(self):
        fitnessMax = 0
        for individu in self.population:
            if(fitnessMax<individu.getFitness()):
                fitnessMax = individu.getFitness()
        return fitnessMax

    def getFitnessMoy(self):
        sum = 0.
        for individu in self.population:
            sum+=individu.getFitness()
        return sum/self.n

    def breeding(self):
        return individu()
