from math import *
from collections import deque, namedtuple

DIRECTIONS = namedtuple('DIRECTIONS',
        ['Up', 'Down', 'Left', 'Right'])(0, 1, 2, 3)
BOARD_LENGTH=32


#renvoie un tableau de taille 34*34*4 correspondant aux inputs du rĂŠseau de neurones Ă  partir du board
#parcours de la grille dans le sens de la lecture
def mappingAvecMur(board, snake):
    
    obstacle = [1,0,0,0] 
    vide = [0,1,0,0]
    tete = [0,0,1,0]
    pomme = [0,0,0,1]
    
    input = []
    
    #mur supĂŠrieur
    for i in range(34):
        input+=obstacle
    
    head=[]
    temp = snake.deque.pop()
    head.append(temp[0])
    head.append(temp[1])
    snake.deque.append(temp)
    
    for i in range(32):        
        input += obstacle  #mur de gauche
        for j in range(32):
            if board[i][j] == 0 :
                input += vide
            elif board[i][j] == 1:
                if [i,j] == head:
                    input += tete
                else:                    
                    input += obstacle
            elif board[i][j] == 2:
                input += pomme
        input += obstacle  #mur de droite
    
    #mur infĂŠrieur
    for i in range(34):
        input+=obstacle
        
    return input 

def mappingSansMur(board, snake):
    
    obstacle = [1,0,0,0] 
    vide = [0,1,0,0]
    tete = [0,0,1,0]
    pomme = [0,0,0,1]
    
    input = []
    
    
    head=[]
    temp = snake.deque.pop()
    head.append(temp[0])
    head.append(temp[1])
    snake.deque.append(temp)

    for i in range(32):        
        for j in range(32):
            if board[i][j] == 0 :
                input += vide
            elif board[i][j] == 1:
                if [i,j] == head:
                    input += tete
                else:
                    input += obstacle
            elif board[i][j] == 2:
                input += pomme
        
    return input 

""" Creer une liste de 11 inputs entre 0 et 1 de la maniere suivante
    1:  distance(tete, pomme) selon l'axe des x
    2:  distance(tete, pomme) selon l'axe des y  
    3 a 5:  Si corps sur la gauche : [distance(tete,corps),0,0]
            Si pomme sur la gauche : [0,distance(tete,pomme),0]
            Si mur sur la gauche: [0,0,distance(tete,mur)]
    6 a 8: idem mais devant
    9 a 11: idem mais sur la droite
    distance(tete,X) est calcule de facon à ce que l'input vale 1 si la distance entre la tete et X 
    est nulle et 0 si elle est de 32 pixel : distance(tete,X) = 1-(|X-tete|/BOARD_LENGTH)"""

def mappingBis(board, snake):
    
    input = []
    
    head=[]
    temp = snake.deque.pop()
    head.append(temp[0])
    head.append(temp[1])
    snake.deque.append(temp)
    
    #Cherche les coordonnees de la pomme
    X=0
    Y=0
    for i in range(32): 
        stop = False
        for j in range(32):
            if board[i][j]==2:
                X=i
                Y=j
                stop=True
                break
        if stop:
             break
    
    input.append(1-abs(head[0]-X)/32)  #deltaX
    input.append(1-abs(head[1]-Y)/32)  #deltaY

    currentDirection = snake.direction
    xTete=head[0]
    yTete=head[1]
    x=xTete
    y=yTete
    trouve = False
    
    #Si dirige vers le haut
    if currentDirection == DIRECTIONS.Up:
    
        #A gauche
        while y>=0 and not trouve:
            y-=1
            if board[xTete][y]==1:
                trouve = True
                distance = 1-(abs(y-yTete)/32)
                input+=[distance,0,0]
            elif board[xTete][y]==2:
                trouve = True
                distance = 1-(abs(y-yTete)/32)
                input+=[0,distance,0]
        if not trouve:
            distance = 1-(abs(y-yTete)/32)
            input+=[0,0,distance]
        y=yTete
        trouve=False
        
        #En haut
        while x>=0 and not trouve:
            x-=1
            if board[x][yTete]==1:
                trouve = True
                distance = 1-(abs(x-xTete)/32)
                input+=[distance,0,0]
            elif board[x][yTete]==2:
                trouve = True
                distance = 1-(abs(x-xTete)/32)
                input+=[0,distance,0]
        if not trouve:
            distance = 1-(abs(x-xTete)/32)
            input+=[0,0,distance]
        x=xTete
        trouve=False
                
        #A droite
        while y<BOARD_LENGTH-1 and not trouve:
            y+=1
            if board[xTete][y]==1:
                trouve = True
                distance = 1-(abs(y-yTete)/32)
                input+=[distance,0,0]
            elif board[xTete][y]==2:
                trouve = True
                distance = 1-(abs(y-yTete)/32)
                input+=[0,distance,0]
        if not trouve:
            distance = 1-(abs(y-yTete)/32)
            input+=[0,0,distance]
        y=yTete
        trouve=False
        
    #Si dirige vers la droite
    if currentDirection == DIRECTIONS.Right:
        
        #En haut
        while x>=0 and not trouve:
            x-=1
            if board[x][yTete]==1:
                trouve = True
                distance = 1-(abs(x-xTete)/32)
                input+=[distance,0,0]
            elif board[x][yTete]==2:
                trouve = True
                distance = 1-(abs(x-xTete)/32)
                input+=[0,distance,0]
        if not trouve:
            distance = 1-(abs(x-xTete)/32)
            input+=[0,0,distance]
        x=xTete
        trouve=False
        
        #A droite
        while y<BOARD_LENGTH-1 and not trouve:
            y+=1
            if board[xTete][y]==1:
                trouve = True
                distance = 1-(abs(y-yTete)/32)
                input+=[distance,0,0]
            elif board[xTete][y]==2:
                trouve = True
                distance = 1-(abs(y-yTete)/32)
                input+=[0,distance,0]
        if not trouve:
            distance = 1-(abs(y-yTete)/32)
            input+=[0,0,distance]
        y=yTete
        trouve=False
        
        #En bas
        while x<BOARD_LENGTH-1 and not trouve:
            x+=1
            if board[x][yTete]==1:
                trouve = True
                distance = 1-(abs(x-xTete)/32)
                input+=[distance,0,0]
            elif board[x][yTete]==2:
                trouve = True
                distance = 1-(abs(x-xTete)/32)
                input+=[0,distance,0]
        if not trouve:
            distance = 1-(abs(x-xTete)/32)
            input+=[0,0,distance]
        x=xTete
        trouve=False
        
    #Si dirige vers le bas
    if currentDirection == DIRECTIONS.Down:
        
        #A droite
        while y<BOARD_LENGTH-1 and not trouve:
            y+=1
            if board[xTete][y]==1:
                trouve = True
                distance = 1-(abs(y-yTete)/32)
                input+=[distance,0,0]
            elif board[xTete][y]==2:
                trouve = True
                distance = 1-(abs(y-yTete)/32)
                input+=[0,distance,0]
        if not trouve:
            distance = 1-(abs(y-yTete)/32)
            input+=[0,0,distance]
        y=yTete
        trouve=False
        
        #En bas
        while x<BOARD_LENGTH-1 and not trouve:
            x+=1
            if board[x][yTete]==1:
                trouve = True
                distance = 1-(abs(x-xTete)/32)
                input+=[distance,0,0]
            elif board[x][yTete]==2:
                trouve = True
                distance = 1-(abs(x-xTete)/32)
                input+=[0,distance,0]
        if not trouve:
            distance = 1-(abs(x-xTete)/32)
            input+=[0,0,distance]
        x=xTete
        trouve=False
        
        #A gauche
        while y>=0 and not trouve:
            y-=1
            if board[xTete][y]==1:
                trouve = True
                distance = 1-(abs(y-yTete)/32)
                input+=[distance,0,0]
            elif board[xTete][y]==2:
                trouve = True
                distance = 1-(abs(y-yTete)/32)
                input+=[0,distance,0]
        if not trouve:
            distance = 1-(abs(y-yTete)/32)
            input+=[0,0,distance]
        y=yTete
        trouve=False
        
    #Si dirige vers la gauche
    if currentDirection == DIRECTIONS.Left:
        
         #En bas
        while x<BOARD_LENGTH-1 and not trouve:
            x+=1
            if board[x][yTete]==1:
                trouve = True
                distance = 1-(abs(x-xTete)/32)
                input+=[distance,0,0]
            elif board[x][yTete]==2:
                trouve = True
                distance = 1-(abs(x-xTete)/32)
                input+=[0,distance,0]
        if not trouve:
            distance = 1-(abs(x-xTete)/32)
            input+=[0,0,distance]
        x=xTete
        trouve=False
        
        #A gauche
        while y>=0 and not trouve:
            y-=1
            if board[xTete][y]==1:
                trouve = True
                distance = 1-(abs(y-yTete)/32)
                input+=[distance,0,0]
            elif board[xTete][y]==2:
                trouve = True
                distance = 1-(abs(y-yTete)/32)
                input+=[0,distance,0]
        if not trouve:
            distance = 1-(abs(y-yTete)/32)
            input+=[0,0,distance]
        y=yTete
        trouve=False
        
        #A droite
        while y<BOARD_LENGTH-1 and not trouve:
            y+=1
            if board[xTete][y]==1:
                trouve = True
                distance = 1-(abs(y-yTete)/32)
                input+=[distance,0,0]
            elif board[xTete][y]==2:
                trouve = True
                distance = 1-(abs(y-yTete)/32)
                input+=[0,distance,0]
        if not trouve:
            distance = 1-(abs(y-yTete)/32)
            input+=[0,0,distance]
        y=yTete
        trouve=False
    
    return input
        
    
    
        
        
    
    
