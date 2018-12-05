import os
import random
import pygame
import const
from pygame.locals import *

pygame.init()

os.chdir("C:/Users/firef_000/Documents/Openclassrooms/Projets/Projet_3")

class Maze:
    """Maze permet de créer le labyrinthe (dans un fichier indépendant)
    Elle possède comme attributs:
    et comme méthode:
    -open_maze: ouvre le fichier maze et l'assigne à une variable read_maze
    -print_maze: pour imprimer le fichier maze et l'assigner à la variable
    p_maze
    -position:
    -find_position:
    -move:
    -object_position:
    -random_pos:
    -items:
    -gagne:
    -display_maze:
    move_pygame:
    """
    def __init__(self):
        self.p_maze = []
        self.open_maze()
        self.macgaver = Characters("R", const.MACGAVER_PICTURE, self.p_maze)
        self.objects = [Characters("E",const.ETHER_PICTURE, self.p_maze), Characters("N", const.NEEDLE_PICTURE, self.p_maze),
        Characters("T", const.TUBE_PICTURE, self.p_maze)]
        self.score = 0
        self.gardien = Characters("G", const.GUARDIAN_PICTURE, self.p_maze)

    def open_maze(self):
    	"""opens the maze file, adds it to the variable self.p_maze and removes the "\n" at the end of each line
    	"""
        with open("maze.txt", "r") as read_maze:
            self.p_maze.extend(read_maze.readlines())
        for i, elt in enumerate(self.p_maze):
            self.p_maze[i] = self.p_maze[i].strip("\n")

    def position(self, line, column, letter):

    	#"." represents the floor
        if self.p_maze[line][column] in [".", self.macgaver.letter, self.objects[0].letter,self.objects[1].letter, self.objects[2].letter,
        self.gardien.letter]:
            self.p_maze[line] = self.p_maze[line][:column] + letter + self.p_maze[line][column+1:]
            return True
        else:
            return False



    def object_position(self, line, column, letter):

    	#"." represents the floor
        if self.p_maze[line][column] == ".": 
            self.p_maze[line] = self.p_maze[line][:column] + letter + self.p_maze[line][column+1:]
            return True
        else:
            return False
        
    def random_pos(self):
    	"""Randomly determines the index of an object. If tbe position is possible, using the self.object_position, it continues
    	to the next object
    	"""
        temp = 0
        while temp < len(self.objects):
            line = random.randint(0, 14)
            column = random.randint(0, 14)
            if self.object_position(line, column, self.objects[temp].letter):
                temp += 1
    
    def items(self):
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
        print("score : ", self.score)
        return self.score
             
    def gagne(self):
        if self.gardien.find_position(self.p_maze) == None:
            if self.score == len(self.objects):
                print("Gagné!")
            else:
                print("Perdu!")
            return False
        else:
            return True
        
    def display_maze(self, WINDOW):
        """Prints the maze in graphic mode
        """ 
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
    	Uses a methode and an attribute of the Character's class to find macgaver's position
    	"""
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
        self.items() #chek the score
        self.gagne() #chek if the game ends and if the player wins or loses    

class Characters:
    def __init__(self, letter, image, p_maze):
        self.letter = letter
        self.image = pygame.image.load(image).convert_alpha()
        self.position = self.find_position(p_maze)

    def find_position(self, p_maze):
        for i, elt in enumerate(p_maze):
            if self.letter in elt:
                iline = i
                nbcolumn = p_maze[iline]
                for i, elt in enumerate(nbcolumn):
                    if self.letter in elt:
                        icolumn = i
                        return[iline, icolumn]



#Ouverture de la fenêtre Pygame
WINDOW = pygame.display.set_mode((const.WINDOW_WIDTH, const.WINDOW_HEIGTH))
laby = Maze()
laby.macgaver.position
laby.random_pos()
#Rafraîchissement de l'écran
pygame.display.flip()

continuer = 1
while continuer:
    laby.display_maze(WINDOW)
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == QUIT:
            continuer = 0
        elif event.type == KEYDOWN:
            laby.move_pygame(event.key)       
