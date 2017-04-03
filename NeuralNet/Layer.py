import numpy as np
import math

def sigmoid(x):
		return 1 / (1 + math.exp(-0.2*x))

class Layer(object):
	"""docstring for Layer"""
	def __init__(self, nbInput, nbOutput, prev, name="Unnamed"):
		self.size = nbInput*nbOutput
		self.prev = prev
		self.name = name+" ("+str(nbInput)+"x"+str(nbOutput)+")"
		self.output = np.zeros(nbOutput)
		self.coeff = np.ones((nbOutput,nbInput))
		self.coeff[0] *= 2


	def calc(self):
		raw_coeff = np.dot(self.coeff,self.prev.output)
		for i in range(len(raw_coeff)):
			self.output[i] = sigmoid(raw_coeff[i])

	def toString(self):
		if(self.prev is None):
			return ("-------BEGINNING OF INPUT LAYER: ---------------\nInput Layer, no coeffs.\nNumber of inputs: "+str(len(self.output))+"\n--------------END OF INPUT LAYER-------------")
		return ("-------BEGINNING OF LAYER: "+self.name+" ---------------\nInput \t" + str(self.prev.output) + "\nCoeffs\t" + str(self.coeff) + "\nOutput\t" + str(self.output) + "\n--------------END OF LAYER: "+self.name+"-------------")



inp = Layer(5,5,None,"Input")
inp.output = np.array([5.0,2.0,3.0,4.0,5.0])
out = Layer(5,2,inp)
out.calc()
print(inp.toString())
print(out.toString())
