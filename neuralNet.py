# -*- coding: utf-8 -*-

import numpy as np
import math
from layer import Layer


def sigmoid(x):
		return 1 / (1 + math.exp(-0.2*x))


class NeuralNet(object):

	"""NeuralNet est un réseau de neurones, c'est aussi un tableau
	de couches de neurones (layer)
	@param: nbInput1  -> nombre d'input de la couche d'input
			nbOutput1 -> nombre d'outputs de la couche d'input
			nbInput2  -> nombre d'input de la couche d'output
			nbOutput2 -> nombre d'outputs de la couche d'output
	@return: instance de Layer
	"""
	def __init__(self, nbInput1, nbOutput1, nbInput2, nbOutput2):
		inp=Layer(nbInput1, nbOutput1, None, "Input")
		self.Layers = [inp,Layer(nbInput2, nbOutput2, inp, "Output")]


	"""Ajoute une layer en avant derniere position
	@param:  nbInput -> nombre d'input de la couche à rajouter
			 nOutput -> nombre d'output de la couche à rajouter
	@return: Void
	"""
	def addLayer(self,nbInput, nbOutput, coeff):
		n=len(self.Layers)
		add=Layer(nbInput, nbOutput, self.Layers[n-2])
		add.coeff=coeff
		self.Layers[n-1].prev=add
		self.Layers.insert((n-1),add)


	"""Affiche recursivement les layer en partant des inputs et en remontant
	Necessite un toString des layer 
	@param: //

	@return: Void
	"""
	def display(self):
		def disp(lay):
			if lay.prev==None :
				print (lay.toString())
			else :
				disp(lay.prev)
				print (lay.toString())
		n=len(self.Layers)
		disp(self.Layers[n-1])


	""" Execute le réseau de neurones avec un tableau d'inputs en entrée
	@param : inp -> tableau des inputs

	@return : tableau des outputs ainsi calculé
	"""
	def run(self,inp):
		n=len(self.Layers)

		"""Premiere couche"""
		raw_coeff = np.dot(self.Layers[0].coeff,inp)
		for i in range(len(raw_coeff)):
			self.Layers[0].output[i] = raw_coeff[i]

		"""Pour les autres"""
		for i in range(1,n):
			self.Layers[i].calc()

		self.Layers[n-1].output=[sigmoid(x) for x in self.Layers[n-1].output]
		return self.Layers[n-1].output

