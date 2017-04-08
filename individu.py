from dna import DNA
from neuralNet import NeuralNet

class Individu:

	def __init__ (self, dna = "null"):
		self.size = 1
		self.health = 99
		
		# creation reseau de neuronne de l'individu
		self.reseau = NeuralNet(4624,1156,12,3)
		self.reseau.addLayer(1156,300)
		self.reseau.addLayer(300,70)
		self.reseau.addLayer(70,12)
		
		# creation ADN
		if (dna == "null"):
			self.dna = DNA(self.reseau.sizeTotale())
		else:
			self.dna = dna

		# remplissage des coeff du reseau de neuronne
		self.reseau.load(self.dna.data)



"""indi = Individu()
#print(indi.dna.data)
print(len(indi.dna.data))"""

