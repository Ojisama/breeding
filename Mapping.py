#renvoie un tableau de taille 34*34*4 correspondant aux inputs du réseau de neurones à partir du board
#parcours de la grille dans le sens de la lecture
def mappingAvecMur(board, snake):
    
    obstacle = [1,0,0,0] 
    vide = [0,1,0,0]
    tete = [0,0,1,0]
    pomme = [0,0,0,1]
    
    input = []
    
    #mur supérieur
    for i in range(34):
        input+=obstacle
    
    head = snake.deque.pop()
    snake.append(head)
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
    
    #mur inférieur
    for i in range(34):
        input+=obstacle
        
    return input 

def mappingSansMur(board, snake):
    
    obstacle = [1,0,0,0] 
    vide = [0,1,0,0]
    tete = [0,0,1,0]
    pomme = [0,0,0,1]
    
    input = []
        
    head = snake.deque.pop()
    snake.append(head)
    
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


#renvoie un tableau de taille 3*4 correspondant aux inputs du réseau de neurones à partir de la vision du serpent
def mappingBis(board, snake):
    
    input = []
    