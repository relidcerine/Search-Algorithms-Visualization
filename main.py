import math
from random import randint
import pygame, sys
from button import Button
import random
import time

x = 1
PLAYER = -1

width = 1200
height = 720
white = (255, 255, 255)
green = (95,158,160)
blue = (0, 0, 128)
Gray=(0,0,139)
Red = (255,0,0)


pygame.init()
random.seed(time.time())

SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Search Algorithms")

Background = pygame.image.load("assets/Background.png")

Black=(0,0,0)
Gray=(150,150,150)
Red = (255,160,122)


class Position():
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Node():
    def __init__(self, value, depth, parent, Lchild, Rchild, position, path, radius, color):
        self.value = value
        self.depth = depth
        self.parent = parent
        self.Lchild = Lchild
        self.Rchild = Rchild
        self.position = position
        self.path = path
        self.radius = radius
        self.color = color

    def getLoc(self):
        return self.position.x, self.position.y

    def getColor(self):
        return self.color

    def getRadius(self):
        return self.radius

    def getLeft(self):
        return self.Lchild

    def getRight(self):
        return self.Rchild
    
    def setValue(self, value):
        self.value = value
        
    def setDepth(self, depth):
        self.value = depth     
    
    def setParent(self, parent):
        self.parent = parent

    def setLeft(self, Lchild):
        self.Lchild = Lchild

    def setRight(self, Rchild):
        self.Rchild = Rchild
        
    def setColor(self, color):
        self.color = color
    
def create_nodes(width,levels):
    nodes = []
    finalTot= 2 ** (levels-1)
    diameter = (width // finalTot)/2
    radius = diameter // 2
    for lvl in range(levels):
        totlvl = 2 ** lvl
        
        start = (width // totlvl) / 2
        for node in range(totlvl):
            pos = Position(start+((width//totlvl)*node), (height//levels)*lvl+(height//levels/2))
            nodes.append(Node(None, lvl+1, None, None, None, pos, lvl, radius, white))

    for i in range(len(nodes)):
        if 2*i+1 < len(nodes) and nodes[2*i+1]:
            nodes[i].setLeft(nodes[2*i+1])
            nodes[2*i+1].setParent(nodes[i])
        if 2*i+2 < len(nodes) and nodes[2*i+2]:
            nodes[i].setRight(nodes[2*i+2])
            nodes[2*i+2].setParent(nodes[i])      
    for i in range(len(nodes) - finalTot, len(nodes)):
        number = randint(-5, 20)
        nodes[i].setValue(number)
            
    return nodes

def draw_circles(SCREEN, width, height, levels, nodes):
    font = pygame.font.Font('freesansbold.ttf', 15)
    for node in nodes:
        node_Loc = node.getLoc()
        
        pygame.draw.circle(SCREEN, node.getColor(),  (node_Loc[0] + 50 ,node_Loc[1]), node.getRadius())
        if(node.path == levels -1):
            text = font.render(str(node.value), True, Black, None)
            pos = node.getLoc()
            SCREEN.blit(text, text.get_rect(center = (pos[0]+50, pos[1])))
            
def draw_player(SCREEN, levels, nodes):
    font = pygame.font.Font('freesansbold.ttf', 15)
    tour = PLAYER
    level = 1
    
    for node in nodes:
        pos = node.getLoc()
        if(node.depth == level):
            if(tour == 1):
                text = font.render('Max', True, blue, None)
                SCREEN.blit(text, text.get_rect(center = (30, (pos[1]-5))))
                tour = -tour
                level += 1
            else:
                text = font.render('Min', True, blue, None)
                SCREEN.blit(text, text.get_rect(center = (30, (pos[1]-5))))
                tour = -tour
                level += 1 
            
def draw_lines(SCREEN, nodes):
    for node in nodes:
        if node.getLeft() != None and node.getRight() != None:
            node_Loc = node.getLoc()
            pygame.draw.line(SCREEN, white, (node.getLoc()[0]+50,node.getLoc()[1]), (node.getLeft().getLoc()[0] +50,node.getLeft().getLoc()[1]), 2)
            pygame.draw.line(SCREEN, white, (node.getLoc()[0]+50,node.getLoc()[1]), (node.getRight().getLoc()[0]+50, node.getRight().getLoc()[1]), 2)

def draw(SCREEN, width, levels, nodes):
    draw_lines(SCREEN, nodes)
    draw_circles(SCREEN, width, height, levels, nodes)
    draw_player(SCREEN, levels, nodes)
    pygame.display.update()
    
def minmax(node, player, depth):
    font = pygame.font.Font('freesansbold.ttf', 15)
    global PLAYER
    global x
    global SCREEN
    x = x+1
    if(depth > 1):
        listOfChildren = [node.getLeft(), node.getRight()]
        if(player == 1):
            bestValue = -math.inf
            bestPath = None
            currentPlayer = player
            for child in listOfChildren:
                minmax(child, -currentPlayer, depth-1)
                if child.value > bestValue:
                    bestValue = child.value
                    bestPath = child
                    bestPos = child.getLoc() 
                    
            node.value = bestValue 
            node.path = bestPath  
            pygame.draw.line(SCREEN, Red,(bestPos[0]+50,bestPos[1]),(node.getLoc()[0]+50,node.getLoc()[1]), 2)
            
                    
        else:
            bestValue = math.inf
            bestPath = None
            currentPlayer = player
            for child in listOfChildren:
                minmax(child, -currentPlayer, depth-1)
                if child.value < bestValue:
                    bestValue = child.value
                    bestPath = child
                    bestPos = child.getLoc() 
            node.value = bestValue
            node.path = bestPath
            pygame.draw.line(SCREEN, Red,(bestPos[0]+50,bestPos[1]),(node.getLoc()[0]+50,node.getLoc()[1]), 2)

    if depth == 1 : 
        text = font.render(str(""), True, Black, None)
    else:
        text = font.render(str(node.value), True, Black, None)

    pos = node.getLoc()
    SCREEN.blit(text, text.get_rect(center = (pos[0]+50, pos[1])))
    pygame.display.flip()
    time.sleep(0.4)
    
    for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

    pygame.display.update()
    
def negamax(node, player, depth):
    font = pygame.font.Font('freesansbold.ttf', 15)
    global PLAYER
    global x
    x += 1
    if(depth > 1):
        listOfChildren = [node.getLeft(), node.getRight()]
        if(player == 1):
            bestValue = -math.inf
            bestPath = None
            currentPlayer = player
            for child in listOfChildren:
                negamax(child, -currentPlayer, depth-1)
                if child.value > bestValue:
                    bestValue = child.value
                    bestPath = child
                    bestPos = child.getLoc() 
                    
                    
            node.value = bestValue
            node.path = bestPath
            pygame.draw.line(SCREEN, Red,(bestPos[0]+50,bestPos[1]),(node.getLoc()[0]+50,node.getLoc()[1]), 2)
                    
        else:
            bestValue = math.inf
            bestPath = None
            currentPlayer = player
            for child in listOfChildren:
                negamax(child, -currentPlayer, depth-1)
                if -1 * child.value < bestValue:
                    bestValue =  -1 * child.value
                    bestPath = child
                    bestPos = child.getLoc() 
                    

            node.value = bestValue
            node.path = bestPath
            pygame.draw.line(SCREEN, Red,(bestPos[0]+50,bestPos[1]),(node.getLoc()[0]+50,node.getLoc()[1]), 2)

    if depth == 1 :
        text = font.render(str(""), True, Black, None)
    else:
        text = font.render(str(node.value), True, Black, None)
         
    pos = node.getLoc()
    SCREEN.blit(text, text.get_rect(center = (pos[0]+50, pos[1])))
    pygame.display.flip()
    time.sleep(0.4)
    for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

    pygame.display.update()
    
def min_max(SCREEN, width, height):
    global x
    global PLAYER
    global Background
   
    while True :
        SCREEN.blit(Background,(0,0))
            
        MINMAX_TEXT = get_font(20).render("MINMAX ALGORITHM", True, "blue")
        
        MINMAX_RECT = MINMAX_TEXT.get_rect(center=(640, 30))
        SCREEN.blit(MINMAX_TEXT, MINMAX_RECT)


        
        levels=5
        nodes=create_nodes(width,levels)
        draw(SCREEN, width, levels, nodes)
        time.sleep(0.8)
        
        while x != 6:
            minmax(nodes[0], PLAYER, levels)
            time.sleep(0.8)
            pygame.quit()
            sys.exit()
            
            
        
        
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                

        pygame.display.update()
        
def Negamax(SCREEN, width, height):
    global x
    global PLAYER
    global Background
    while True :
        NEGAMAX_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.blit(Background,(0,0))
        
            
        MINMAX_TEXT = get_font(20).render("NEGAMAX ALGORITHM", True, "blue")
        
        MINMAX_RECT = MINMAX_TEXT.get_rect(center=(640, 30))
        SCREEN.blit(MINMAX_TEXT, MINMAX_RECT)


        
        levels=5
        nodes=create_nodes(width,levels)
        draw(SCREEN, width, levels, nodes)
        time.sleep(0.8)
        
        while x != 6:
            negamax(nodes[0], PLAYER, levels)
            time.sleep(0.8)
            pygame.quit()
            sys.exit()
        
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                

        pygame.display.update()


MINMAX_bool = False
NEGAMAX_bool = False
ALPHABETA_bool = False

def get_font(size): 
    return pygame.font.Font('freesansbold.ttf', size)


def alphabetaAlgorithm(node, player, depth, alpha, beta):
    font = pygame.font.Font('freesansbold.ttf', 15)
    alpha = alpha
    beta = beta
    
    if(depth == 1):
        
        if(player == -1):
                node.value = -node.value
        text = font.render(str(node.value), True, Black, None)
        pos = node.getLoc()
        SCREEN.blit(text, text.get_rect(center = (pos[0]+50, pos[1])))
        pygame.display.flip()
        time.sleep(0.5) 
        
    else:
        font2 =pygame.font.Font('freesansbold.ttf', 8)
        text = font2.render("α = " + str(alpha), True, blue, green)
        pos = node.getLoc()
        SCREEN.blit(text, text.get_rect(center = (pos[0], pos[1]+15))) 
        text = font2.render("β = " + str(beta), True, blue, green)
        pos = node.getLoc()
        SCREEN.blit(text, text.get_rect(center = (pos[0], pos[1]+35)))
        listOfChildren = [node.getLeft(), node.getRight()]
        bestValue = -math.inf
        bestPath = None
        currentPlayer = player
        for child in listOfChildren:
            alphabetaAlgorithm(child, -currentPlayer, depth-1, -beta, -alpha)
            child.value = -child.value
            
            if child.value > bestValue:
                bestValue = child.value
                bestPath = child
                bestPos = child.getLoc() 
            
            if bestValue > alpha:
              alpha = bestValue
            
            
            if beta <= alpha:
              break;    
                
        node.value = bestValue
        node.path = bestPath
        pygame.draw.line(SCREEN, Red,(bestPos[0]+50,bestPos[1]),(node.getLoc()[0]+50,node.getLoc()[1]), 2)          
        text = font.render(str(node.value), True, Black, None)
        pos = node.getLoc()
        SCREEN.blit(text, text.get_rect(center = (pos[0]+50, pos[1])))
        pygame.display.flip()
        time.sleep(0.5)
        
    for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()    

def alphabeta(win, width, height, player, levels):
    global x
    while True :
        NEGAMAX_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.blit(Background,(0,0))
        
            
        MINMAX_TEXT = get_font(20).render("ALPHA-BETA ALGORITHME", True, "blue")
        
        MINMAX_RECT = MINMAX_TEXT.get_rect(center=(640, 30))
        SCREEN.blit(MINMAX_TEXT, MINMAX_RECT)

    
        nodes=create_nodes(width,levels)
        draw(SCREEN, width, levels, nodes)
        time.sleep(0.5)
    
        while x < levels+1:
            alphabetaAlgorithm(nodes[0], player, levels, -math.inf, math.inf)
            time.sleep(2)
            pygame.quit()
            sys.exit()
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                

        pygame.display.update()
        

def MINMAX_MENU():
    global PLAYER
    global NEGAMAX_bool
    global ALPHABETA_bool
    global MINMAX_bool
    global SCREEN
    while True:
        MIN_MOUSE_POS = pygame.mouse.get_pos()
        MAX_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("#000000")

        
            
        MIN_BUTTON = Button(image=pygame.image.load("assets/menu.png"), pos=(300, 400), 
                                text_input="MIN", font=get_font(20), base_color="#d7fcd4", hovering_color="blue")
        MAX_BUTTON = Button(image=pygame.image.load("assets/menu.png"), pos=(1000, 400), 
                                text_input="MAX", font=get_font(20), base_color="#d7fcd4", hovering_color="blue")
        MINMAX_TEXT = get_font(30).render("choisissez entre le Min ou le Max", True, "#4682B4")
        MINMAX_RECT = MINMAX_TEXT.get_rect(center=(640, 200))
        SCREEN.blit(MINMAX_TEXT, MINMAX_RECT)


        MAX_BUTTON.changeColor(MAX_MOUSE_POS)
        MAX_BUTTON.update(SCREEN)
        MIN_BUTTON.changeColor(MIN_MOUSE_POS)
        MIN_BUTTON.update(SCREEN)
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if MAX_BUTTON.checkForInput(MAX_MOUSE_POS):
                        PLAYER = 1
                        if (MINMAX_bool == True):
                            min_max(SCREEN, width, height)

                        if (NEGAMAX_bool == True):
                            Negamax(SCREEN, width, height)
                        if (ALPHABETA_bool == True):
                            alphabeta(SCREEN, width, height,1,5)
                        
                    elif MIN_BUTTON.checkForInput(MAX_MOUSE_POS):
                        PLAYER = - 1
                        if (MINMAX_bool == True):
                            min_max(SCREEN, width, height)

                        if (NEGAMAX_bool == True):
                            Negamax(SCREEN, width, height)
                        if (ALPHABETA_bool == True):
                            alphabeta(SCREEN, width, height,1,5)
                        

        pygame.display.update()


def main_menu():
    global x
    global NEGAMAX_bool
    global ALPHABETA_bool
    global MINMAX_bool
    while True:
        SCREEN.blit(Background, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(80).render("MAIN MENU", True, "#4682B4")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        MINMAX_BUTTON = Button(image=pygame.image.load("assets/menu.png"), pos=(640, 220), 
                            text_input="MinMax", font=get_font(20), base_color="#d7fcd4", hovering_color="blue")
        NEGAMAX_BUTTON = Button(image=pygame.image.load("assets/menu.png"), pos=(640, 360), 
                            text_input="Negamax", font=get_font(20), base_color="#d7fcd4", hovering_color="blue")
        ALPHBETA_BUTTON = Button(image=pygame.image.load("assets/menu.png"), pos=(640, 500), 
                            text_input="Negamax AlphaBeta", font=get_font(18), base_color="#d7fcd4", hovering_color="blue")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/menu.png"), pos=(640, 640), 
                            text_input="QUIT", font=get_font(20), base_color="#d7fcd4", hovering_color="blue")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [MINMAX_BUTTON, NEGAMAX_BUTTON,ALPHBETA_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if MINMAX_BUTTON.checkForInput(MENU_MOUSE_POS):
                    MINMAX_bool = True
                    NEGAMAX_bool = False
                    ALPHABETA_bool = False
                    x =  1
                    MINMAX_MENU()

                if ALPHBETA_BUTTON.checkForInput(MENU_MOUSE_POS):
                    MINMAX_bool = False
                    NEGAMAX_bool = False
                    ALPHABETA_bool = True
                    x =  1
                    MINMAX_MENU()
                    
                if NEGAMAX_BUTTON.checkForInput(MENU_MOUSE_POS):
                    MINMAX_bool = False
                    NEGAMAX_bool = True
                    ALPHABETA_bool = False
                    x =  1
                    MINMAX_MENU()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()