"""Macgyver's maze game:
MacGyver is in a maze. You must have him picks up 3 objects before presenting
on the guardian. If you have gathered all the objects when you arrive on the
gardian, you win, otherwise, you lose.
Use the arrow keys on your keybord to move MacGyver
"""
import pygame
from pygame.locals import QUIT, KEYDOWN
import classes

pygame.init()

#initializes the maze
maze_game = classes.Maze()
maze_game.random_pos()
game_condition = 1

#loop's game
while game_condition:
    if maze_game.win_lose() is True:
        maze_game.display_maze()
        #Refreshes the display
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == QUIT:
                game_condition = 0
            elif event.type == KEYDOWN:
                maze_game.move_pygame(event.key)
    else:
    	#Refreshes the display
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == QUIT:
                game_condition = 0
