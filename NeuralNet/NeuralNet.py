import numpy as np

class NeuralNet(object):
	"""docstring for NeuralNet"""
	def __init__(self, nbInput1, nbOutput1, nbOutput2):
		super(NeuralNet, self).__init__()
		inp=Layer(nbInput1, nbOutput1, None)
		self.Layers = [inp,Layer(nbOutput1, nbOutput2, inp)]

	def addLayer(nbInput, nbOutput):
		n=len(self.Layers)
		self.Layers.insert((n-1),Layer(nbInput, nbOutput, self.Layers[n-2]))