# -*- coding: utf-8 -*-

import numpy as np
import math
from layer import Layer
from neuralNet import sigmoid
from neuralNet import NeuralNet

""" Crée et initialise un réseau de neurones à 3 Hidden Layers
@param : coeff1 -> matrice des coefficients de la couche d'Input
		 coeff2 -> matrice des coefficients de la première Hidden Layer
		 coeff3 -> matrice des coefficients de la deuxième Hidden Layer
		 coeff4 -> matrice des coefficients de la troisième Hidden Layer
		 coeff5 -> matrice des coefficients de la couche d'Output
@return : un NeuralNet prêt à être utilisé
"""
def initialize(coeff1, coeff2, coeff3, coeff4, coeff5):
	network = NeuralNet(4624,1156,12,3)
	network.Layers[0].coeff=coeff1
	network.Layers[1].coeff=coeff5
	network.addLayer(1156,300, coeff2)
	network.addLayer(300,70,coeff3)
	network.addLayer(70,12,coeff4)
	return network



test=initialize(np.ones((1156,4624)),np.ones((300,1156)),np.ones((70,300)),np.ones((12,70)),np.ones((3,12)))

tableauInputs = 4624*[1]

tableauOutputs = test.run(tableauInputs)


test.run(4624*[1])
test.display()
