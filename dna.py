import random


class DNA():

    
    def __init__(self, taille):       
        self.data=[]
        for i in range(taille):
            new_byte = []
            for k in range(8):
                new_byte.append(random.randint(0,1)) 
            self.data.append(new_byte)
    
    

adn = DNA(5)
print(adn.data)
