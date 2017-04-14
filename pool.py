class Pool():

    """Population de (n) snakes a tester et a croiser
    
    Attributes:
        n (int): Taille de la population
        population (deque): ensemble des N individus de la populations
    """

    def __init__(self, n):
        self.population = deque()
        self.n = n
        for i in range(self.n):
            self.population.append(Individu())

    def breeding(self):
        return Individu()
        

    
    def getFitnessMax(self):
        fitnessMax = 0
        for individu in self.population:
            if individu.getFitness() > fitnessMax:
                fitnessMax = individu.getFitness()
        return fitnessMax

    def getFitnessMoy(self):
        somme = 0
        for individu in self.population:
            somme += individu.getFitness()
        return somme/self.n
