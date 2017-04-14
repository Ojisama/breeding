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


    
