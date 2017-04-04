import numpy as np
import math

def sigmoid(x):
		return 1 / (1 + math.exp(-0.2*x))

class Layer(object):

	"""Layer est une couche de neurones
	@param: nbInput -> nombre d'input de la couche
			nbOutput -> nombre d'output de la couche
			prev -> couche précédente
			name -> nom de la couche (facultatif)
	@return: instance de Layer
	"""

	def __init__(self, nbInput, nbOutput, prev, name="Unnamed"):
		self.size = nbInput*nbOutput
		self.prev = prev
		self.name = name+" ("+str(nbInput)+"x"+str(nbOutput)+")"
		self.output = np.zeros(nbOutput)
		self.coeff = np.ones((nbOutput,nbInput))
		self.coeff[0] *= 2

	"""calc() met à jour les ouput de __self__ en effectuant le produit matriciel input*coeff = output
	@param: 
	@return: void (effet de bord)
	"""
	def calc(self):
		raw_coeff = np.dot(self.coeff,self.prev.output)
		for i in range(len(raw_coeff)):
			self.output[i] = sigmoid(raw_coeff[i])

	"""toString() renvoie une String décrivant explicitement le Layer
	@param: 
	@return: String (sur plusieurs lignes)
	"""
	def toString(self):
		if(self.prev is None):
			return ("-------BEGINNING OF INPUT LAYER: ---------------\nInput Layer, no coeffs.\nNumber of inputs: "+str(len(self.output))+"\n--------------END OF INPUT LAYER-------------")
		return ("-------BEGINNING OF LAYER: "+self.name+" ---------------\nInput \t" + str(self.prev.output) + "\nCoeffs\t" + str(self.coeff) + "\nOutput\t" + str(self.output) + "\n--------------END OF LAYER: "+self.name+"-------------")


