import numpy as np
import math

def sigmoid(x):
		return 1 / (1 + math.exp(-0.2*x))

class Layer(object):
	"""docstring for Layer"""
	def __init__(self, nbInput, nbOutput, prev):
		self.size = nbInput*nbOutput
		self.prev = prev
		self.output = np.zeros(nbOutput)
		self.coeff = np.ones((nbOutput,nbInput))
		self.coeff[0] *= 2


	def calc(self):
		raw_coeff = np.dot(self.coeff,self.prev.output)
		for i in range(len(raw_coeff)):
			self.output[i] = sigmoid(raw_coeff[i])

	def toString(self):
		return ("Input \t" + str(self.prev.output) + "\nCoeffs\t" + str(self.coeff) + "\nOutput\t" + str(self.output))



inp = Layer(5,5,None)
inp.output = np.array([5.0,2.0,3.0,4.0,5.0])
out = Layer(5,2,inp)
out.calc()
print(out.toString())
