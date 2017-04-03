import numpy as np
import math
from layer import Layer
from layer import sigmoid

class NeuralNet(object):
	"""docstring for ClassName"""
	def __init__(self, nbInput1, nbOutput1, nbOutput2):
		inp=Layer(nbInput1, nbOutput1, None, "Input")
		self.Layers = [inp,Layer(nbOutput1, nbOutput2, inp, "Output")]

	"""Ajoute une layer en avant derniere position"""
	def addLayer(self,nbInput, nbOutput):
		n=len(self.Layers)
		self.Layers.insert((n-1),Layer(nbInput, nbOutput, self.Layers[n-2]))


	"""Affiche recursivement les layer en partant des inputs et en remontant
	Necessite un toString des layer """
	def display(self):
		def disp(lay):
			if lay.prev==None :
				print lay.toString()
			else :
				disp(lay.prev)
				print lay.toString()
		n=len(self.Layers)
		disp(self.Layers[n-1])

	"""prend un double[] inp en entree et ressort un int[] de la size des outputs
	 Version 1.0 """
	
	def run(self,inp):
		n=len(self.Layers)

		"""Premiere couche"""
		raw_coeff = np.dot(self.Layers[0].coeff,inp)
		for i in range(len(raw_coeff)):
			self.Layers[0].output[i] = sigmoid(raw_coeff[i])

		"""Pour les autres"""
		for i in range(1,n):
			self.Layers[i].calc()

		return self.Layers[n-1].output

