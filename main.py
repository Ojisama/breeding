import numpy as np
import math
from layer import Layer
from layer import sigmoid
from neuralNet import NeuralNet

print ("-- TEST STRUCTURE et DISPLAY --")
print ("\n")
prev = Layer(5,5,None, "test")
prev.output = [1, 0, 0, 0, 0]
inp = Layer(5,5,prev,"Input")
out = Layer(5,2,inp)

print ("\n")
print ("\n")

print ("-- TEST RUN --")
print ("\n")

print ("\n")
print ("\n")
test = NeuralNet(300,100,6,3)
test.addLayer(100,30)
test.addLayer(30,10)
test.addLayer(10,6)


print(test.run(300*[1]))
