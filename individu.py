from dna import DNA
from neuralNet import NeuralNet

class Individu:

    def __init__ (self, dna = "null"):
        self.size = 1
        self.health = 65
        
        # creation reseau de neuronne de l'individu
        self.reseau = NeuralNet(1936,42,42,3)
        
        # creation ADN
        if (dna == "null"):
            self.dna = DNA(self.reseau.sizeTotale())
        else:
            self.dna = dna

        # remplissage des coeff du reseau de neuronne
        self.reseau.load(self.dna.data)

    def getFitness(self):
        return (100 * self.size + self.health)

    def setFitness(self,nb):
        self.size = nb

    def decay(self):
        if self.health>1:
            self.health-=1
            return False
        else:
            return True

    def eat(self):
        self.size+=1

    def __str__(self):
        return str(self.size)+" / "+str(self.health)+" | "+str(self.dna)

"""indi = Individu()
#print(indi.dna.data)
print(len(indi.dna.data))"""
