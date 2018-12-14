import os
import random
import pygame
from pygame.locals import *
import const
import classes
pygame.init()



#initialize the maze
laby = classes.Maze()
laby.random_pos()

#Refresh the display
pygame.display.flip()

continuer = 1
#loop's game
while continuer:
    laby.display_maze(const.WINDOW)
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == QUIT:
            continuer = 0
        elif event.type == KEYDOWN:
            laby.move_pygame(event.key)       
