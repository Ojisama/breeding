import numpy as np

class NeuralNet(object):
	"""docstring for ClassName"""
	def __init__(self, nbInput1, nbOutput1, nbOutput2):
		super(NeuralNet, self).__init__()
		inp=Layer(nbInput1, nbOutput1, none)
		self.Layers = [inp,Layer(nbOutput1, nbOutput2, inp)]

	#Ajoute une layer en avant dernière position
	def addLayer(nbInput, nbOutput):
		n=len(self.Layers)
		self.Layers.insert((n-1),Layer(nbInput, nbOutput, self.Layers[n-2]))


	#Affiche récursivement les layer en partant des inputs et en remontant
	#Necessite un toString des layer 
	def display():
		def rec disp(lay):
			if lay.prev==none :
				print lay.toString()
			else :
				disp(lay.prev)
				print lay.toString()
		n=len(self.Layers)
		disp(self.Layers[n])

