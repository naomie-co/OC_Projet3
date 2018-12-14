#constants for macgaver's maze

import os
import random
import pygame
from pygame.locals import *
import const
import classes
pygame.init()

#parameters for the window
SPRITE_SIZE = 40
SPRITE_WIDTH = 15
SPRITE_HEIGTH = 16
WINDOW_WIDTH = SPRITE_SIZE * SPRITE_WIDTH
WINDOW_HEIGTH = SPRITE_SIZE * SPRITE_HEIGTH

#Open Pygame's window
WINDOW = pygame.display.set_mode((const.WINDOW_WIDTH, const.WINDOW_HEIGTH))

#initialize pictures for the game
WALL_PICTURE = "pictures/wall.png"
FLOOR_PICTURE = "pictures/floor.png"
MACGAVER_PICTURE = "pictures/player.png"
GUARDIAN_PICTURE = "pictures/guardian.png"
ETHER_PICTURE = "pictures/ether.png"
NEEDLE_PICTURE = "pictures/needle.png"
TUBE_PICTURE = "pictures/tube.png"
GAGNE_PICTURE = "pictures/gagne.png"
PERDU_PICTURE = "pictures/perdu.png"