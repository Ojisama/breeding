import random


class DNA():

    
    def __init__(self, taille, rand=True):       
        self.data=[]
	if rand:
		for i in range(taille):
		    self.data.append(random.random())
	else:
		for i in range(taille):
                self.data.append(0)

    def crossover(self, ADN2, mutationcoeff):
		new_adn = []
		for i in range(len(self.data)):
			if (i%2 == 0):
				newcoeff = self.data[i]
			else:
				newcoeff = ADN2[i]
		
			if (random.random() < mutationcoeff):
				print("mutation au rang " + str(i))
			
				hasard = random.randint(0,1)
				changement = newcoeff*0.15

				if hasard == 0:
					if (newcoeff + changement) > 1:
						newcoeff = 1
					else:
						newcoeff += changement
				else:
					if (newcoeff - changement) < 0:
						newcoeff = 0
					else:
						newcoeff -= changement

			new_adn.append(newcoeff)
			
		return(new_adn)


adn1 = DNA(5)
adn2 = DNA(5)
print(adn1.data)
print(adn2.data)
print(adn1.crossover(adn2.data,0.3))
