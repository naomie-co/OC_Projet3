import os
import random
import pygame
from pygame.locals import *
import const

pygame.init()

os.chdir("C:/Users/firef_000/Documents/Openclassrooms/Projets/Projet_3")

class Maze:
    """The Maze class is used to import the maze from a txt file, to display it in graphic mode, to integrate objects randomly, to
    move character and to chek the score. It uses some attributes from the Character's class."""
    def __init__(self):
        self.p_maze = []
        self.open_maze()
        self.macgaver = Characters("R", const.MACGAVER_PICTURE, self.p_maze)
        self.objects = [Characters("E",const.ETHER_PICTURE, self.p_maze), Characters("N", const.NEEDLE_PICTURE, self.p_maze),
        Characters("T", const.TUBE_PICTURE, self.p_maze)]
        self.score = 0
        self.gardien = Characters("G", const.GUARDIAN_PICTURE, self.p_maze)
        self.game_over = False #about  the main loop of the game

    def open_maze(self):
        """Opens the maze file, reads it, add line by line on the list attribute self.p_maze, and removes the "\n" """
        with open("maze.txt", "r") as read_maze:
            self.p_maze.extend(read_maze.readlines())
        for i, elt in enumerate(self.p_maze):
            self.p_maze[i] = self.p_maze[i].strip("\n")

    def position(self, line, column, letter):
        """Prints a character on the maze who can be on the maze,so it can move on a object """
        if self.p_maze[line][column] in [".", self.macgaver.letter, self.objects[0].letter,self.objects[1].letter, self.objects[2].letter, self.gardien.letter]:
            self.p_maze[line] = self.p_maze[line][:column] + letter + self.p_maze[line][column+1:]
            return True
        else:
            return False

    def object_position(self, line, column, letter):
        """Prints an items only on the floor. "." represents the floor"""
        if self.p_maze[line][column] == ".": 
            self.p_maze[line] = self.p_maze[line][:column] + letter + self.p_maze[line][column+1:]
            return True
        else:
            return False
        
    def random_pos(self): 
        """Randomly determines the index of an object. If the position is possible, by using the self.object_position, 
        it continues to the next object"""
        temp = 0
        while temp < len(self.objects):
            line = random.randint(0, 14)
            column = random.randint(0, 14)
            if self.object_position(line, column, self.objects[temp].letter):
                temp += 1
    
    def items(self, WINDOW):
        """Picks up the items in the maze and prints it at the bottom of the maze. Returns the player's score"""
        objets_collectes = list(self.objects)
        y = (const.SPRITE_HEIGTH - 1) * const.SPRITE_SIZE
        x = const.SPRITE_SIZE * 3
        self.score = 0
        for elt in self.objects:
            for line in self.p_maze:
                if elt.letter in line:
                    self.score += 1
                    objets_collectes.remove(elt)
                    break
        for elt in objets_collectes:
            if elt.letter == "E":
                WINDOW.blit(self.objects[0].image, (x, y))
            elif elt.letter == "N":
                WINDOW.blit(self.objects[1].image, (x + const.SPRITE_SIZE, y))
            elif elt.letter == "T":
                WINDOW.blit(self.objects[2].image, (x + 2*const.SPRITE_SIZE, y))
        self.score = len(self.objects) - self.score
        return self.score
             
    def gagne(self, WINDOW):
        """check if the player picked up every items in the maze, when macgaver arrives on the guardien. Print a won/lost message. 
        Allows to finish the game"""
        y = (const.SPRITE_HEIGTH - 1) * const.SPRITE_SIZE
        x = const.SPRITE_SIZE * 7
        gagne = pygame.image.load(const.GAGNE_PICTURE).convert()
        perdu = pygame.image.load(const.PERDU_PICTURE).convert()
        if self.gardien.find_position(self.p_maze) == None:
            if self.score == len(self.objects):
                WINDOW.blit(gagne, (x, y))

            else:
                WINDOW.blit(perdu, (x, y))
            self.game_over = True #end of the main loop of the game
            return False
        else:
            return True
        
    def display_maze(self, WINDOW):
        """Prints the maze in graphic mode""" 
        wall = pygame.image.load(const.WALL_PICTURE).convert()
        floor = pygame.image.load(const.FLOOR_PICTURE).convert()
        nb_line = 0
        for line in self.p_maze:
            nb_column = 0
            for elt in line:
                x = nb_column * const.SPRITE_SIZE
                y = nb_line * const.SPRITE_SIZE
                if elt == "w":
                    WINDOW.blit(wall, (x, y))
                elif elt == ".":
                    WINDOW.blit(floor, (x, y))
                elif elt == self.macgaver.letter:
                    WINDOW.blit(floor, (x, y))
                    WINDOW.blit(self.macgaver.image, (x, y))
                elif elt == self.gardien.letter:
                    WINDOW.blit(floor, (x, y))
                    WINDOW.blit(self.gardien.image, (x, y))
                elif elt == self.objects[0].letter:
                    WINDOW.blit(floor, (x, y))
                    WINDOW.blit(self.objects[0].image, (x, y))
                elif elt == self.objects[1].letter:
                    WINDOW.blit(floor, (x, y))
                    WINDOW.blit(self.objects[1].image, (x, y))
                elif elt == self.objects[2].letter:
                    WINDOW.blit(floor, (x, y))
                    WINDOW.blit(self.objects[2].image, (x, y))
                nb_column += 1
            nb_line += 1

    def move_pygame(self, key):
        """Moves macgaver: takes a key as argument. Depending on the key, it defines mac_gaver's new position and modifies the old one.
Uses a methode and an attribute of the Character's class to find macgaver's position"""
        
        if self.game_over == False:
            p_macgaver = self.macgaver.find_position(self.p_maze) 
            if key == K_UP:
                if self.position(p_macgaver[0]-1, p_macgaver[1], self.macgaver.letter):
                    self.position(p_macgaver[0], p_macgaver[1], ".")
            elif key == K_DOWN:
                if self.position(p_macgaver[0]+1, p_macgaver[1], self.macgaver.letter):
                    self.position(p_macgaver[0], p_macgaver[1], ".")
            elif key == K_LEFT:
                if self.position(p_macgaver[0], p_macgaver[1]-1, self.macgaver.letter):
                    self.position(p_macgaver[0], p_macgaver[1], ".")
            elif key == K_RIGHT:
                if self.position(p_macgaver[0], p_macgaver[1]+1, self.macgaver.letter):
                    self.position(p_macgaver[0], p_macgaver[1], ".")
            self.items(const.WINDOW) #check the score
            self.gagne(const.WINDOW) #check if the game ends and if the player wins or loses    

class Characters:
    """Class Characters initialize a character or item and allows with an attribute. Methode find position to identify the coordinates of a
    character """
    def __init__(self, letter, image, p_maze):
        self.letter = letter
        self.image = pygame.image.load(image).convert_alpha()
        self.position = self.find_position(p_maze)

    def find_position(self, p_maze):
        """Finds the position of a character, and return a tuple of coordinates """
        for i, elt in enumerate(p_maze):
            if self.letter in elt:
                iline = i
                nbcolumn = p_maze[iline]
                for i, elt in enumerate(nbcolumn):
                    if self.letter in elt:
                        icolumn = i
                        return[iline, icolumn]



