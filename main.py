import numpy as np
import math
from layer import Layer
from layer import sigmoid
from neuralNet import NeuralNet

print "-- TEST STRUCTURE et DISPLAY --"
print "\n"
inp = Layer(5,5,None,"Input")
inp.output = np.array([5.0,2.0,3.0,4.0,5.0])
out = Layer(5,2,inp)
out.calc()
test = NeuralNet(5,5,2)
test.display()
print "\n"
print "\n"

print "-- TEST RUN --"
print "\n"
print test.run([1, 0, 0, 0, 0])