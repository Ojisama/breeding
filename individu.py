from dna import DNA
from neuralNet import NeuralNet

HEALTH_MAX = 32*4

class Individu:

    def __init__ (self, dna = "null"):
        self.size = 0
        self.health = HEALTH_MAX
        
        # creation reseau de neuronne de l'individu
        self.reseau = NeuralNet(11,6,6,3)
        
        # creation ADN
        if (dna == "null"):
            self.dna = DNA(self.reseau.sizeTotale())
        else:
            self.dna = dna

        # remplissage des coeff du reseau de neuronne
        self.reseau.load(self.dna.data)

    def getFitness(self):
        return int(100 * self.size + self.health*25/32)

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
        self.heatlh = HEALTH_MAX

    def __str__(self):
        return str(self.size)+" / "+str(self.health)+" | "+str(self.dna)

"""indi = Individu()
#print(indi.dna.data)
print(len(indi.dna.data))"""
