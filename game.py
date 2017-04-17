# coding: utf-8

from collections import deque, namedtuple
from pool import *
import random
import pygame
import select
from individu import Individu
from Mapping import *


speed=150
BOARD_LENGTH = 32
OFFSET = 16
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
POOL_SIZE = 50


DIRECTIONS = namedtuple('DIRECTIONS',
        ['Up', 'Down', 'Left', 'Right'])(0, 1, 2, 3)




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
    def __init__(self, direction=DIRECTIONS.Right, point=(16, 16, (20,120,80)), color=(20,120,80)):
        self.tailmax = 4
        self.direction = direction 
        self.deque = deque()
        self.deque.append(point)
        self.color = color
        self.nextDir = deque()
        self.indexDirection = 2
        self.individu = Individu()
    
    def __str__(self):
        return str(self.tailmax)

    def get_color(self):
        return (20,120,80)
    
    def setIndividu(self, individuPool):
        self.individu = individuPool

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
        food = random.randrange(BOARD_LENGTH), random.randrange(BOARD_LENGTH)
        if (not (spots[food[0]][food[1]] == 1 or
            spots[food[0]][food[1]] == 2)):
            break
    return food


def end_condition(board, coord):
    if (coord[0] < 0 or coord[0] >= BOARD_LENGTH or coord[1] < 0 or
            coord[1] >= BOARD_LENGTH):
        return True
    if (board[coord[0]][coord[1]] == 1):
        return True
    return False

def make_board():
    spots = [[] for i in range(BOARD_LENGTH)]
    for row in spots:
        for i in range(BOARD_LENGTH):
            row.append(0)
    return spots
    

def update_board(screen, snakes, food):
    rect = pygame.Rect(0, 0, OFFSET, OFFSET)

    spots = [[] for i in range(BOARD_LENGTH)]
    num1 = 0
    num2 = 0
    for row in spots:
        for i in range(BOARD_LENGTH):
            row.append(0)
            temprect = rect.move(num1 * OFFSET, num2 * OFFSET)
            pygame.draw.rect(screen, BLACK, temprect)
            num2 += 1
        num1 += 1
    spots[food[0]][food[1]] = 2
    temprect = rect.move(food[1] * OFFSET, food[0] * OFFSET)
    pygame.draw.rect(screen, rand_color(), temprect)
    for snake in snakes:
        for coord in snake.deque:
            spots[coord[0]][coord[1]] = 1
            temprect = rect.move(coord[1] * OFFSET, coord[0] * OFFSET)
            pygame.draw.rect(screen, coord[2], temprect)
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

def update_board_delta(screen, deltas):
    # accepts a queue of deltas in the form
    # [("d", 13, 30), ("a", 4, 6, "rd")]
    # valid colors: re, wh, bk, bl
    rect = pygame.Rect(0, 0, OFFSET, OFFSET)
    change_list = []
    delqueue = deque()
    addqueue = deque()
    while len(deltas) != 0:
        d = deltas.pop()
        change_list.append(pygame.Rect(d[1], d[2], OFFSET, OFFSET))
        if d[0] == "d":
            delqueue.append((d[1], d[2]))
        elif d[0] == "a":
            addqueue.append((d[1], d[2], get_color(d[3])))
    
    for d_coord in delqueue:
        temprect = rect.move(d_coord[1] * OFFSET, d_coord[0] * OFFSET)
        # TODO generalize background color
        pygame.draw.rect(screen, BLACK, temprect)

    for a_coord in addqueue:
        temprect = rect.move(a_coord[1] * OFFSET, a_coord[0] * OFFSET)
        pygame.draw.rect(screen, a_coord[2], temprect)

    return change_list

# Return 0 to exit the program, 1 for a one-player game
def menu(screen):
    font = pygame.font.Font(None, 30)
    menu_message1 = font.render("Press enter for one-player, t for two-player", True, WHITE)
    menu_message2 = font.render("C'est le PIST de l'ambiance", True, WHITE)

    screen.fill(BLACK)
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

def quit(screen,pool):
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
def play(screen, pool): 
    clock = pygame.time.Clock()
    spots = make_board()
    indexDirection = 0

    #______________________________________ SCRIPT DU BREEDING _____________________________

    snake = Snake()
    snake.setIndividu(pool.breeding())

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

        #____________________________ DECISION-MAKING _____________________________

        inp = mappingBis(spots, snake)
        snake.populate_nextDir(snake.trad_direction(network_nextDir(snake.individu,inp)))

        #____________________________ /DECISION-MAKING _____________________________

        

        # Game logic
        next_head = move(snake)
        if snake.individu.decay():
            print("Snake n°"+str(pool.trained)+" | Size: "+str(snake.individu.size)+" \t| Health = 0  \t|| Fitness = "+str(snake.individu.getFitness())+" \t|| MORT NATURELLE \t\t|| ["+str(pool.min)+";"+str(pool.max)+"] - avg = "+str(pool.moy))
            return snake.tailmax
        if (end_condition(spots, next_head)):
            print("Snake n°"+str(pool.trained)+" | Size: "+str(snake.individu.size)+" \t| Health = "+str(snake.individu.health)+" \t|| Fitness = "+str(snake.individu.getFitness())+" \t|| AFFREUX ACCIDENT \t|| ["+str(pool.min)+";"+str(pool.max)+"] - avg = "+str(pool.moy))
            return snake.tailmax

        if is_food(spots, next_head):
            snake.tailmax += 4
            snake.individu.eat()
            food = find_food(spots)
        pool.updateStatistics()
        snake.deque.append(next_head)

        if len(snake.deque) > snake.tailmax:
            snake.deque.popleft()

        # Draw code
        screen.fill(BLACK)  # makes screen black

        spots = update_board(screen, [snake], food)

        pygame.display.update()

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
    

def encode_deltas(delta_str):
    # delta_str is in the form
    # "(15 23 bk)(22 12 fo)(10 11 rm)"
    deltas = deque()
    state = "open"
    while len(delta_str) != 0:
        if state == "open":
            encoded_delta = ["fx", 0, 0, "fx"]
            delta_str = delta_str[1:]
            on_num = 1
            store_val = ""
            state = "num"
        if state == "num":
            if delta_str[0] == " ":
                delta_str = delta_str[1:]
                encoded_delta[on_num] = int(store_val)
                store_val = ""
                on_num += 1
                if on_num > 2:
                    state = "color"
            else:
                store_val += delta_str[0]
                delta_str = delta_str[1:]
        if state == "color":
            if delta_str[0] == ")":
                if store_val == "rm":
                    encoded_delta[0] = "d"
                elif store_val == "fo":
                    encoded_delta[0] = "a"
                    encoded_delta[3] = "fo"
                else:
                    encoded_delta[0] = "a"
                    encoded_delta[3] = store_val
                delta_str = delta_str[1:]
                state = "open"
                deltas.appendleft(encoded_delta)
            else:
                store_val += delta_str[0]
                delta_str = delta_str[1:]
    return deltas
                

def game_over(screen, eaten):
    message1 = "You ate %d foods" % eaten
    message2 = "Press enter to play again, esc to quit."
    game_over_message1 = pygame.font.Font(None, 30).render(message1, True, BLACK)
    game_over_message2 = pygame.font.Font(None, 30).render(message2, True, BLACK)

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
    pygame.init()
    screen = pygame.display.set_mode([BOARD_LENGTH * OFFSET,
        BOARD_LENGTH * OFFSET])
    pygame.display.set_caption("Snaake")
    thing = pygame.Rect(10, 10, 50, 50)
    pygame.draw.rect(screen,pygame.Color(255,255,255,255),pygame.Rect(50,50,10,10))
    first = True
    playing = True
    i=0
    while playing:
        i+=1
        if first or pick == 3:
            pick = menu(screen)

        options = {0 : quit,
                1 : play}
        now = options[pick](screen,pool)
        if now == False:
            break
        elif pick == 1 or pick == 2:
            eaten = now / 4 - 1
            #playing = game_over(screen, eaten)
            first = False
    pygame.quit()

if __name__ == "__main__":
    main()
