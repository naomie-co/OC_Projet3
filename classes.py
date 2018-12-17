"""Classes for macgyver's maze game"""

import random
import pygame
from pygame.locals import K_UP, K_DOWN, K_LEFT, K_RIGHT
import const

class Maze:
    """The Maze class is used to import the maze from a txt file, to display
    it in graphic mode, to integrate objects randomly, to move character and
    to check the score. It uses attributes from the Character's class."""
    def __init__(self):
        #Initializes a list type variable for the maze
        self.p_maze = []
        self.open_maze()
        self.window_2 = pygame.display.set_mode((const.WINDOW_WIDTH,\
        const.WINDOW_HEIGTH))
        self.macgyver = Characters("R", const.MACGYVER_PICTURE, self.window_2)
        self.objects = [Characters("E", const.ETHER_PICTURE, self.window_2),\
                        Characters("N", const.NEEDLE_PICTURE, self.window_2),\
                        Characters("T", const.TUBE_PICTURE, self.window_2)]
        self.gardien = Characters("G", const.GUARDIAN_PICTURE, self.window_2)
        self.score = 0
        #Condition for the move_pygame's method: if True, macgyver stops moving
        #The condition is check in the win_lose method
        self.game_over = False

    def open_maze(self):
        """Opens the maze file, reads it, adds line by line in the list type
        attribute self.p_maze, and removes the \n """
        with open("maze.txt", "r") as read_maze:
            self.p_maze.extend(read_maze.readlines())
        for i, elt in enumerate(self.p_maze):
            self.p_maze[i] = self.p_maze[i].strip("\n")

    def position(self, line, column, letter):
        """Prints a character on the maze so it can move on a the floor,
        the guardian and objects """
        if self.p_maze[line][column] in [".", self.macgyver.letter,\
        self.objects[0].letter, self.objects[1].letter, self.objects[2].letter,\
        self.gardien.letter]:
            self.p_maze[line] = self.p_maze[line][:column] + letter +\
            self.p_maze[line][column+1:]
            return True
        else:
            return False

    def object_position(self, line, column, letter):
        """Prints items only on the floor."""
        if self.p_maze[line][column] == ".":
            self.p_maze[line] = self.p_maze[line][:column] + letter +\
            self.p_maze[line][column+1:]
            return True
        else:
            return False

    def random_pos(self):
        """Randomly determines the index of an object. If the position is
        possible (on the floor), using the self.object_position, it continues
        to the next object"""
        temp = 0
        while temp < len(self.objects):
            line = random.randint(0, 14)
            column = random.randint(0, 14)
            if self.object_position(line, column, self.objects[temp].letter):
                temp += 1

    def items(self):
        """Picks up items in the maze and prints it at the bottom line of the
        maze. Returns the player's score"""
        pick_up = list(self.objects)
        y_sprite = (const.SPRITE_HEIGTH - 1) * const.SPRITE_SIZE
        x_sprite = const.SPRITE_SIZE * 3
        self.score = 0
        for elt in self.objects:
            for line in self.p_maze:
                if elt.letter in line:
                    self.score += 1
                    pick_up.remove(elt)
                    break
        for elt in pick_up:
            if elt.letter == "E":
                self.window_2.blit(self.objects[0].picture, (x_sprite,\
                y_sprite))
            elif elt.letter == "N":
                self.window_2.blit(self.objects[1].picture, (x_sprite +\
                const.SPRITE_SIZE, y_sprite))
            elif elt.letter == "T":
                self.window_2.blit(self.objects[2].picture, (x_sprite +\
                2*const.SPRITE_SIZE, y_sprite))
        self.score = len(self.objects) - self.score
        return self.score

    def win_lose(self):
        """Check if the player picked up every item in the maze, when macgyver
        arrives on the guardien. Print a win/lose message. Stop the condition
        for the move_pygame method. Uses as a condition on the loop's game"""
        win = pygame.image.load(const.WIN_PICTURE).convert()
        lose = pygame.image.load(const.LOSE_PICTURE).convert()
        if self.gardien.find_position(self.p_maze) is None:
            if self.score == len(self.objects):
                self.window_2.blit(win, (0, 0))
            else:
            #Stop the condition for the move_pygame methode
                self.window_2.blit(lose, (0, 0))
            self.game_over = True
            return False
        else:
            return True

    def display_maze(self):
        """Prints the maze in graphic mode"""
        wall = pygame.image.load(const.WALL_PICTURE).convert()
        floor = pygame.image.load(const.FLOOR_PICTURE).convert()
        nb_line = 0
        for line in self.p_maze:
            nb_column = 0
            for elt in line:
                x_sprite = nb_column * const.SPRITE_SIZE
                y_sprite = nb_line * const.SPRITE_SIZE
                if elt == "w":
                    self.window_2.blit(wall, (x_sprite, y_sprite))
                elif elt == ".":
                    self.window_2.blit(floor, (x_sprite, y_sprite))
                elif elt == self.macgyver.letter:
                    self.window_2.blit(floor, (x_sprite, y_sprite))
                    self.window_2.blit(self.macgyver.picture, (x_sprite,\
                    y_sprite))
                elif elt == self.gardien.letter:
                    self.window_2.blit(floor, (x_sprite, y_sprite))
                    self.window_2.blit(self.gardien.picture, (x_sprite,\
                    y_sprite))
                elif elt == self.objects[0].letter:
                    self.window_2.blit(floor, (x_sprite, y_sprite))
                    self.window_2.blit(self.objects[0].picture, (x_sprite,\
                    y_sprite))
                elif elt == self.objects[1].letter:
                    self.window_2.blit(floor, (x_sprite, y_sprite))
                    self.window_2.blit(self.objects[1].picture, (x_sprite,\
                    y_sprite))
                elif elt == self.objects[2].letter:
                    self.window_2.blit(floor, (x_sprite, y_sprite))
                    self.window_2.blit(self.objects[2].picture, (x_sprite,\
                    y_sprite))
                nb_column += 1
            nb_line += 1

    def move_pygame(self, key):
        """Moves macgyver whith macgyver stops moving as argument. Depending
        on the key, it defines mac_gaver's new position and modifies the
        previous one. Uses a method of the Character's class to find macgyver's
        position"""
        if self.game_over is not True:
            p_macgyver = self.macgyver.find_position(self.p_maze)
            if key == K_UP:
                if self.position(p_macgyver[0]-1, p_macgyver[1],\
                self.macgyver.letter):
                    self.position(p_macgyver[0], p_macgyver[1], ".")
            elif key == K_DOWN:
                if self.position(p_macgyver[0]+1, p_macgyver[1],\
                self.macgyver.letter):
                    self.position(p_macgyver[0], p_macgyver[1], ".")
            elif key == K_LEFT:
                if self.position(p_macgyver[0], p_macgyver[1]-1,\
                self.macgyver.letter):
                    self.position(p_macgyver[0], p_macgyver[1], ".")
            elif key == K_RIGHT:
                if self.position(p_macgyver[0], p_macgyver[1]+1,\
                self.macgyver.letter):
                    self.position(p_macgyver[0], p_macgyver[1], ".")
            #checks the score
            self.items()
            #checks if the game ends and if the player won or lost
            self.win_lose()


class Characters:
    """Class Characters initializes character or item. Find_position's method
    to identify coordinates of a character/item."""
    def __init__(self, letter, picture, window):
        self.letter = letter
        self.picture = pygame.image.load(picture).convert_alpha()
        self.window = window

    def find_position(self, p_maze):
        """Finds the position of a character, and return a tuple of
        coordinates """
        for i, elt_1 in enumerate(p_maze):
            if self.letter in elt_1:
                nbcolumn = p_maze[i]
                for j, elt_2 in enumerate(nbcolumn):
                    if self.letter in elt_2:
                        return[i, j]
