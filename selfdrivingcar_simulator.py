import sys
import pygame
from pygame.locals import *
import random

pygame.init()

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (210,55,190)
BLUE = (0, 0, 255)
GRID_WIDTH = 50
GRID_HEIGHT = 50

screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption('Self Driving Car Simulator v0.1')
screen.fill(WHITE)
road_map = []

f = open('map.txt', 'r')
for line in f:
    road_map.append([x for x in line.split()])
#print road_map
f.close()

heur = []
f = open('heur.txt','r')
for line in f:
    heur.append([int(x) for x in line.split()])
print heur
f.close()

def make_grid(screen, step, direction = 'vertical'):
    width = screen.get_width()
    height = screen.get_height()
    if(direction == 'vertical'):
        for x in xrange(0, width, step):
            pygame.draw.line(screen, BLACK, (x, 0), (x, height))
    if(direction == 'horizontal'):
        for y in xrange(0, height, step):
            pygame.draw.line(screen, BLACK, (0, y), (width, y))

def make_map(screen, road_map):
    for y in xrange(len(road_map)):
        for x in xrange(len(road_map[0])):
            if(road_map[y][x] == '1'):
                pygame.draw.rect(screen, BLACK, (x*GRID_WIDTH, y*GRID_HEIGHT, GRID_WIDTH, GRID_HEIGHT))
            if(road_map[y][x] == 'G'):
                pygame.draw.rect(screen, RED, (x*GRID_WIDTH, y*GRID_HEIGHT, GRID_WIDTH, GRID_HEIGHT))
            if(road_map[y][x] == 'S'):
                pygame.draw.rect(screen, RED, (x*GRID_WIDTH, y*GRID_HEIGHT, GRID_WIDTH, GRID_HEIGHT))

def generate_layout(screen, road_map):
    make_grid(screen, GRID_WIDTH, 'vertical')
    make_grid(screen, GRID_HEIGHT, 'horizontal')
    make_map(screen, road_map)

xGRID = (screen.get_width()/GRID_WIDTH)-1
yGRID = (screen.get_height()/GRID_HEIGHT)-1

generate_layout(screen, road_map)

visited = []
for i in xrange(len(road_map)):
    temp = []
    for j in xrange(len(road_map[0])):
        temp.append(0)
    visited.append(temp)
#print visited

queue = []
path_len = 0
queue.append((heur[0][0] + path_len,0,0))
visited[0][0] = 1
goal = (7, 11)

pygame.draw.rect(screen, RED, (goal[1]*GRID_WIDTH, goal[0]*GRID_HEIGHT, GRID_WIDTH, GRID_HEIGHT))
found = False
curr_level = 1
next_level = 0

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    
    randx = random.randint(0,xGRID)
    randy = random.randint(0,yGRID)
    if(visited[randy][randx] == 0 and (randy, randx) != goal):
        pygame.draw.rect(screen, BLACK, (randx*GRID_WIDTH, randy*GRID_HEIGHT, GRID_WIDTH, GRID_HEIGHT))
        road_map[randy][randx] = '1'
    #pygame.time.wait(10)

    if(len(queue) != 0 and found == False):
        queue.sort()
        temp = queue.pop(0)
        curr_level -= 1
        
        if(type(temp) == type((0, 0,0))):
            x = temp[1]
            y = temp[2]
            #print type(x)
            #print type(y)
            if(x == goal[0] and y==goal[1]):
                print 'Found Path'
                pygame.draw.rect(screen, BLUE, (y*GRID_WIDTH, x*GRID_HEIGHT, GRID_WIDTH, GRID_HEIGHT))
                found = True
                continue
            if(x+1 < len(road_map) and x+1 >= 0 and y < len(road_map[0]) and y>=0):
                if(road_map[x+1][y] == '0' and visited[x+1][y] == 0):
                    queue.append((heur[x+1][y] + path_len+1, x+1,y))
                    visited[x+1][y] = 1
                    next_level += 1
            if(x < len(road_map) and x>= 0 and y+1 < len(road_map[0]) and y+1 >=0):
                if(road_map[x][y+1] == '0' and visited[x][y+1] == 0):
                    queue.append((heur[x][y+1] + path_len+1, x,y+1))
                    visited[x][y+1] = 1
                    next_level += 1
            if(x-1 < len(road_map) and x-1 >= 0 and y < len(road_map[0]) and y>=0):
                if(road_map[x-1][y] == '0' and visited[x-1][y] == 0):
                    queue.append((heur[x-1][y] + path_len+1, x-1,y))
                    visited[x-1][y] = 1
                    next_level += 1
            if(x < len(road_map) and x >= 0 and y-1 < len(road_map[0]) and y-1 >=0):
                if(road_map[x][y-1] == '0' and visited[x][y-1] == 0):
                    queue.append((heur[x][y-1] + path_len+1, x,y-1))
                    visited[x][y-1] = 1
                    next_level += 1
            pygame.draw.rect(screen, GREEN, (y*GRID_WIDTH, x*GRID_HEIGHT, GRID_WIDTH, GRID_HEIGHT))
            print 'Currently at Path Len', path_len
            if(curr_level == 0):
                curr_level = next_level
                next_level = 0
                path_len += 1
    elif(found == False):
        print 'No Path to the Goal.'

    pygame.time.wait(100)
    pygame.display.update()
