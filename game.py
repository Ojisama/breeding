# coding: utf-8

from collections import deque, namedtuple
from pool import *
from timeit import default_timer as timer
import random
import pygame
import select
from individu import Individu
from Mapping import *
from IA import *
import csv
import sys
import matplotlib.pyplot as plt

import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

speed=100
BOARD_LENGTH = 32
OFFSET = int(BOARD_LENGTH/2)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
POOL_SIZE = 50
IHM = True
MUR = True
NB_SNAKE_CONCOMITTANTS_LOL = 3
leftSide = True


DIRECTIONS = namedtuple('DIRECTIONS',
        ['Up', 'Down', 'Left', 'Right'])(0, 1, 2, 3)



def rand_start():
    return (random.randrange(BOARD_LENGTH)|1, random.randrange(BOARD_LENGTH)&16|1, rand_color())

def rand_color():
    return (random.randrange(254)|64, random.randrange(254)|64, random.randrange(254)|64)

class Snake(object):
    """Description:
    
    Attributes:
        color (triplet (int,int,int)): couleur du snake
        deque (deque (double-ended queue, à la fois une pile et une file)): corps du snake
        direction (int dans [0,3]): direction du snake (cf variable globale DIRECTIONS)
        indexDirection (int): ???
        nextDir (deque): pile des directions (FIFO) 
        tailmax (int): taille du snake
        individu (individu): instance d'individu associée à l'instance de Snake
    """
    def __init__(self, direction=DIRECTIONS.Right, point=(OFFSET, OFFSET, (20,120,80)), color=(20,120,80)):
        self.tailmax = 1
        self.direction = direction 
        self.deque = deque()
        self.deque.append(point)
        self.color = color
        self.nextDir = deque()
        self.indexDirection = 2
        self.individu = Individu()
        self.hasPackage = 0
    
    def __str__(self):
        return str(self.tailmax)

    def get_color(self):
        return self.color
    
    def setIndividu(self, individuPool):
        self.individu = individuPool

    def pickup(self):
        global leftSide
        if self.hasPackage==0:
            leftSide = False
            self.individu.eat()
            self.hasPackage = 1
            self.color = (100,0,0)

    def deposit(self):
        global leftSide
        if self.hasPackage==1:
            leftSide = True
            self.individu.eat()
            self.hasPackage = 0
            self.color = (20,120,80)


    def trad_direction(self, nv_dir):
        """Traduit la direction demandée (relative, 0:gauche, 1: en face 2:droite) 
        en direction absolue (N S W E)
        Merci Agathe!
        
        Args:
            nv_dir (DIRECTION): direction relative
        
        Returns:
            DIRECTION: absolue
        """
        if (self.direction == DIRECTIONS.Up):
            if nv_dir == 0:
                return DIRECTIONS.Left
            if nv_dir == 1:
                return DIRECTIONS.Up
            else:
                return DIRECTIONS.Right

        elif (self.direction == DIRECTIONS.Right):
            if nv_dir == 0:
                return DIRECTIONS.Up
            if nv_dir == 1:
                return DIRECTIONS.Right
            else:
                return DIRECTIONS.Down

        elif (self.direction == DIRECTIONS.Down):
            if nv_dir == 0:
                return DIRECTIONS.Right
            if nv_dir == 1:
                return DIRECTIONS.Down
            else:
                return DIRECTIONS.Left

        elif (self.direction == DIRECTIONS.Left):
            if nv_dir == 0:
                return DIRECTIONS.Down
            if nv_dir == 1:
                return DIRECTIONS.Left
            else:
                return DIRECTIONS.Up


    def populate_nextDir(self, direction):
        """Ajoute la prochaine direction que doit prendre le snake sur une pile (d'où le appendLeft)
        
        Args:
            direction (???): A DEFINIR

        Returns:
            void: ajoute en haut de pile la direction choisie
        """

        self.nextDir.appendleft(direction)
        self.indexDirection+=1

#______________________________________ SCRIPT DU JEU __________________________________


def find_food(spots):
    while True:
        if leftSide:
            food = random.randrange(BOARD_LENGTH), random.randrange(8)
            if (not (spots[food[0]][food[1]] == 1 or
                spots[food[0]][food[1]] == 2)):
                break
        else:
            food = 16, 28
            if (not (spots[food[0]][food[1]] == 1 or
                spots[food[0]][food[1]] == 2)):
                break
    return food


def end_condition(snake, board, coord, list_next_head):
    if (coord[0] < 0 or coord[0] >= BOARD_LENGTH or coord[1] < 0 or
            coord[1] >= BOARD_LENGTH):
        return True
    if (board[coord[0]][coord[1]] == 1):
        return True
    for (snake_iter,next_head_iter) in list_next_head.items():
        #print(coord)
        #print(next_head_iter)
        if snake != snake_iter and next_head_iter == coord:
            del list_next_head[snake]
            del list_next_head[snake_iter]
            print("Choc effroyable")
            return True
    return False

def make_board():
    return [[0 for i in range(BOARD_LENGTH)] for i in range(BOARD_LENGTH)]
    

def update_board(screen, snakes, food):
    if IHM:
        rect = pygame.Rect(0, 0, OFFSET, OFFSET)
    
        spots = [[] for i in range(BOARD_LENGTH)]
        num1 = 0
        num2 = 0
        for row in spots:
            for i in range(BOARD_LENGTH):
                row.append(0)
                temprect = rect.move(num1 * OFFSET, num2 * OFFSET)
                pygame.draw.rect(screen, (12,35,64), temprect)
                num2 += 1
            num1 += 1
        spots[food[0]][food[1]] = 2
        temprect = rect.move(food[1] * OFFSET, food[0] * OFFSET)
        pygame.draw.rect(screen, (164,210,51), temprect)
        temprect = rect.move(28 * OFFSET, 16 * OFFSET)
        pygame.draw.rect(screen, WHITE, temprect)
        for snake in snakes:
            for coord in snake.deque:
                spots[coord[0]][coord[1]] = 1
                temprect = rect.move(coord[1] * OFFSET, coord[0] * OFFSET)
                pygame.draw.rect(screen, snake.get_color(), temprect)
        if MUR:
            spots[0][0]=1
            temprect = rect.move(0, 0)
            pygame.draw.rect(screen, (255,228,196), temprect)
            for i in range(5,13):
                spots[i][16]=1
                temprect = rect.move(16 * OFFSET, i * OFFSET)
                pygame.draw.rect(screen, RED, temprect)
            for i in range(19,27):
                spots[i][16]=1
                temprect = rect.move(16 * OFFSET, i * OFFSET)
                pygame.draw.rect(screen, RED, temprect)

        # Faire l'affichage des statistiques de la pool
        font = pygame.font.Font(None, 15)
        message_stats = font.render("Nombre de produits ramenées : " + str(snake.individu.size//1), True, WHITE)

        screen.blit(message_stats, (10, 20)) 
 



        return spots
    else:
        spots=make_board()
        spots[food[0]][food[1]] = 2
        for snake in snakes:
            for coord in snake.deque:
                spots[coord[0]][coord[1]] = 1
        if MUR: 
            spots[0][0]=1
            for i in range(5,13):
                spots[i][16]=1
            for i in range(19,27):
                spots[i][16]=1


                     
            
        return spots

def get_color(s):
    if s == "bk":
        return BLACK
    elif s == "wh":
        return WHITE
    elif s == "rd":
        return RED
    elif s == "bl":
        return BLUE
    elif s == "fo":
        return rand_color()
    else:
        print("WHAT", s)
        return BLUE

# Return 0 to exit the program, 1 for a one-player game
def menu(screen):
    font = pygame.font.Font(None, 30)
    menu_message1 = font.render("Press enter for one-player, t for two-player", True, WHITE)
    menu_message2 = font.render("C'est le PIST de l'ambiance", True, WHITE)

    screen.fill((12,35,64))
    screen.blit(menu_message1, (32, 32)) 
    screen.blit(menu_message2, (32, 64))
    pygame.display.update()
    while True: 
        done = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return 1
        if done:
            break
    if done:
        pygame.quit()
        return 0

def quit(screen,pool,list_snakes):
    return False

def move(snake):
    if len(snake.nextDir) != 0:
        next_dir = snake.nextDir.pop()
    else:
        next_dir = snake.direction
    head = snake.deque.pop()
    snake.deque.append(head)
    next_move = head
    if (next_dir == DIRECTIONS.Up):
        if snake.direction != DIRECTIONS.Down:
            next_move =  (head[0] - 1, head[1], snake.get_color())
            snake.direction = next_dir
        else:
            next_move =  (head[0] + 1, head[1], snake.get_color())
    elif (next_dir == DIRECTIONS.Down):
        if snake.direction != DIRECTIONS.Up:
            next_move =  (head[0] + 1, head[1], snake.get_color())
            snake.direction = next_dir
        else:
            next_move =  (head[0] - 1, head[1], snake.get_color())
    elif (next_dir == DIRECTIONS.Left):
        if snake.direction != DIRECTIONS.Right:
            next_move =  (head[0], head[1] - 1, snake.get_color())
            snake.direction = next_dir
        else:
            next_move =  (head[0], head[1] + 1, snake.get_color())
    elif (next_dir == DIRECTIONS.Right):
        if snake.direction != DIRECTIONS.Left:
            next_move =  (head[0], head[1] + 1, snake.get_color())
            snake.direction = next_dir
        else:
            next_move =  (head[0], head[1] - 1, snake.get_color())
    return next_move

def is_food(board, point):
    return board[point[0]][point[1]] == 2


# Return false to quit program, true to go to
# gameover screen
def play(screen, pool, list_snakes): 
    clock = pygame.time.Clock()
    spots = make_board()
    indexDirection = 0
    global leftSide
    #______________________________________ SCRIPT DU BREEDING _____________________________


    #______________________________________ /SCRIPT DU BREEDING ____________________________
    # PUTAING C BO LA SIMPLICITÉ


    # Board set up
    spots[0][0] = 1
    food = find_food(spots)

    while True:
        clock.tick(speed)
        # Event processing
        done = False
        events = pygame.event.get()
        for event in events: 
            if event.type == pygame.QUIT:
                print("Quit given")
                done = True
                break
        if done:
            return False

        while len(list_snakes) < NB_SNAKE_CONCOMITTANTS_LOL: #initialisation
            snake = Snake(point=rand_start())
            snake.setIndividu(pool.breeding())
            list_snakes.append(snake)

        list_next_head = {}
        for snake in list_snakes:

            #____________________________ DECISION-MAKING _____________________________

            inp = encoreUnMapping(spots, snake)
            #inp.append(snake.hasPackage)
            snake.populate_nextDir(snake.trad_direction(network_nextDir(snake.individu,inp))) 

            #____________________________ /DECISION-MAKING _____________________________


            # Game logic
            
            next_head = move(snake)
            list_next_head[snake] = next_head
            if snake.individu.decay():
                logging.debug("Snake n°"+str(pool.trained)+" | Size: "+str(snake.individu.size)+" \t| Health = 0  \t|| Fitness = "+str(snake.individu.getFitness())+" \t|| MORT NATURELLE \t\t|| ["+str(pool.min)+";"+str(pool.max)+"] - avg = "+str(pool.moy))
                list_snakes.remove(snake)
                if snake.hasPackage == 1:
                    leftSide = True
                    food = find_food(spots)
                break

            if end_condition(snake, spots, next_head, list_next_head):
                logging.debug("Snake n°"+str(pool.trained)+" | Size: "+str(snake.individu.size)+" \t| Health = "+str(snake.individu.health)+" \t|| Fitness = "+str(snake.individu.getFitness())+" \t|| AFFREUX ACCIDENT \t|| ["+str(pool.min)+";"+str(pool.max)+"] - avg = "+str(pool.moy))
                list_snakes.remove(snake)
                if snake.hasPackage == 1:
                    leftSide = True
                    food = find_food(spots)
                break
            
            
            
            if is_food(spots, next_head):
                if leftSide:
                    snake.pickup()
                else:
                    snake.deposit()
                
                food = find_food(spots)

                
            pool.updateStatistics()
            snake.deque.append(next_head)

            if len(snake.deque) > snake.tailmax:
                snake.deque.popleft()

        # Draw code
        screen.fill((12,35,64))  # makes screen black

        spots = update_board(screen, list_snakes, food)

        pygame.display.update()
        # à décommenter pour afficher le Snake 
        # MAIS environ 75% plus lent sur mappingBis 5000 itérations

def network_nextDir(indiv,inp):
    output=indiv.reseau.run(inp)
    def maxIndice(liste):
        indice=0
        max=liste[0]
        for i in range(1,len(liste)):
            if liste[i]>max :
                indice=i
                max = liste[i]
        return indice
    return maxIndice(output)

def sauvegarder(pool, fileName):
    with open(fileName,"w") as file:
        writer = csv.writer(file)
        for i in range(pool.getTaille()):
            writer.writerows([pool.population[i].dna.data])
            writer.writerow([pool.population[i].size])
        file.close()

def charger(fileName):
    i=0
    pool=Pool(POOL_SIZE)
    pool.trained=POOL_SIZE
    cr = csv.reader(open(fileName,"rU"))
    for row in cr:       
        if len(row)==1:
            pool.population[i].size=int(row[0])
            i+=1
        elif len(row)>1:
            pool.population[i] = Individu()
            for j in range(pool.population[i].reseau.sizeTotale()):
                pool.population[i].dna.data[j]=float(row[j])

    return pool
    
                

def game_over(screen, eaten):
    message1 = "You ate %d foods" % eaten
    message2 = "Press enter to play again, esc to quit."
    game_over_message1 = pygame.font.Font(None, 30).render(message1, True, (12,35,64))
    game_over_message2 = pygame.font.Font(None, 30).render(message2, True, (12,35,64))

    overlay = pygame.Surface((BOARD_LENGTH * OFFSET, BOARD_LENGTH * OFFSET))
    overlay.fill((84, 84, 84))
    overlay.set_alpha(150)
    screen.blit(overlay, (0,0))

    screen.blit(game_over_message1, (35, 35))
    screen.blit(game_over_message2, (65, 65))
    game_over_message1 = pygame.font.Font(None, 30).render(message1, True, WHITE)
    game_over_message2 = pygame.font.Font(None, 30).render(message2, True, WHITE)
    screen.blit(game_over_message1, (32, 32))
    screen.blit(game_over_message2, (62, 62))
   
    pygame.display.update()

    while True: 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                if event.key == pygame.K_RETURN:
                    return True
#______________________________________ /SCRIPT DU JEU ________________________________


        
    

def main():
    pool = Pool(POOL_SIZE)
    #pool = charger('optimumAmazon88.csv')
    pygame.init()
    screen = pygame.display.set_mode([BOARD_LENGTH * OFFSET,
        BOARD_LENGTH * OFFSET])
    pygame.display.set_caption("Snaake")
    thing = pygame.Rect(10, 10, 50, 50)
    pygame.draw.rect(screen,pygame.Color(255,255,255,255),pygame.Rect(50,50,10,10))
    first = True
    playing = True
    i=0

    list_snakes = []

    start = timer()
    numSnake = []
    avgFitness = []
    maxFitness = []
    while playing:
        
        i+=1
        if first or pick == 3:
            pick = 1

        options = {0 : quit,
                1 : play}
        now = options[pick](screen,pool,list_snakes)
        if now == False:
            break
        elif pick == 1 or pick == 2:
            eaten = now / 4 - 1
            #playing = game_over(screen, eaten)
            first = False
        if pool.trained%10 == 0:
            numSnake.append(i)
            avgFitness.append(pool.getFitnessMoy())
            maxFitness.append(pool.getFitnessMax()[0])

    
    """plt.plot(numSnake, maxFitness, label="Fitness max")
    plt.plot(numSnake, avgFitness, label="Fitness moyen")    
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.ylabel('Fitness')
    plt.xlabel("Nombre de snakes")
    plt.show()"""
#    sauvegarder(pool,'out.csv')
    end = timer()
    time = end-start
    print(str(time))
    print(str(time/i)+" ms par Snake")
    pygame.quit()

if __name__ == "__main__":
    main()
