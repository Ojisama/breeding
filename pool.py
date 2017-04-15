from individu import Individu
from collections import deque
import random

class Pool():

    """Population de (n) snakes a tester et a croiser
    
    Attributes:
        n (int): Taille de la population
        population (deque): ensemble des N individus de la populations
    """

    def __init__(self, n):
        self.population = deque()
        for i in range(n):
            self.population.append(Individu())
        self.mutationcoeff = 1/self.getFitnessMax()
        self.trained = 0

    def breeding(self):
        if self.trained < 10:
            print(self.population[self.trained])
            tmp = self.trained
            self.trained+=1
            return self.population[tmp]
        else:
            # Creation du tableau de croisement
            tab = []
            fitnessMax = self.getFitnessMax()
            self.mutationcoeff = 1/self.getFitnessMax()
            for individu in self.population:
                nb_apparition = int((individu.getFitness() * 100) / fitnessMax)
                for i in range(nb_apparition):
                    tab.append(individu)

            # Choix des deux parents
            index1 = random.randint(0,len(tab)-1)
            index2 = random.randint(0,len(tab)-1)
            
            while(index1 == index2): # eviter d'avoir le meme index
                index2 = random.randint(0,len(tab)-1)
            
            print("index1 " + str(index1))
            print("index2 " + str(index2))
            
            parent1 = tab[index1]
            parent2 = tab[index2]

            # Remplacer l'individu avec le fitness le plus faible par un enfant
            index_pire_indiv = self.getFitnessMin()[1]
            dna_enfant = parent1.dna.crossover(parent2.dna, self.mutationcoeff)
            enfant = Individu(dna_enfant)
            self.population[index_pire_indiv] = enfant

            return enfant
        

    
    def getFitnessMax(self):
        fitnessMax = 0
        for individu in self.population:
            if individu.getFitness() > fitnessMax:
                fitnessMax = individu.getFitness()
        return fitnessMax

    def getFitnessMin(self):
        fitnessMin = 0
        position_individuMin = 0
        for i,individu in enumerate(self.population):
            if individu.getFitness() < fitnessMin:
                fitnessMin = individu.getFitness()
                position_individuMin = i
        return [fitnessMin,i]

    def getFitnessMoy(self):
        somme = 0
        for individu in self.population:
            somme += individu.getFitness()
        return somme/self.n

    def __str__(self):
        string = ""
        for i in range(len(self.population)):
            string+=(str(self.trained)+" : "+str(self.population[i])+"\n")
        return string

    

#Tests

# Test de la creation du tableau dans breeding
a = Pool(2)
a.population[0].size = 11
print(a.getFitnessMax())
print(a.breeding())
