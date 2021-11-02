from numpy.lib.arraypad import pad
import pygame
import numpy as np
from numpy import fliplr
from pygame.locals import *
from constants import *

import random
import time
from colorama import init
from colorama import Fore, Back, Style


init()

class Maze(object):
    def __init__(self):
        self.maze = []

        #do not touch
        self.height = 27 #top path and bottom lines are passes, carve w/o them
        self.width = 14 #starting with left wall
        self.array = np.chararray([NROWS, NCOLS])
        self.array[:] = "."
        self.array[:, 0] = "W"
        self.array[:, 27] = "W"
        self.array[:3, :] = "X"
        self.array[34:, :] = "X"
        self.array[3, :] = "W" #F for frontier, W for wall, p for path, H home area, X for non-game area, G for home perimeter
        self.array[33, :] = "W"
        self.array[4,1:27] = "p"
        self.array[32,1:27] = "p"
        self.gatherMaze()
        # np.savetxt("mapgen.txt", self.array)

    

    #here starts the generation

    ## Functions
    def printMaze(self):
        for i in range(0, self.height):
            for j in range(0, self.width):
                if (self.maze[i][j] == 'u'):
                    print(Fore.WHITE + str(self.maze[i][j]), end=" ")
                elif (self.maze[i][j] == 'p'):
                    print(Fore.GREEN + str(self.maze[i][j]), end=" ")
                else:
                    print(Fore.RED + str(self.maze[i][j]), end=" ")
                
            print('\n')

    # Find number of surrounding cells
    def surroundingCells(self,rand_wall):
        s_cells = 0
        if (self.maze[rand_wall[0]-1][rand_wall[1]] == 'p'):
            s_cells += 1
        if (self.maze[rand_wall[0]+1][rand_wall[1]] == 'p'):
            s_cells += 1
        if (self.maze[rand_wall[0]][rand_wall[1]-1] == 'p'):
            s_cells +=1
        if (self.maze[rand_wall[0]][rand_wall[1]+1] == 'p'):
            s_cells += 1

        return s_cells

    def createLeftMaze(self):
        wall = 'W'
        cell = 'p'
        unvisited = 'u'
        self.height = 27 #top path and bottom lines are passes
        self.width = 14
        self.maze = []

        for i in range(0, self.height):
            line = []
            for j in range(0, self.width):
                line.append(unvisited)
            self.maze.append(line)

        # Randomize starting point and set it a cell
        starting_height = int(random.random()*self.height)
        starting_width = int(random.random()*self.width)
        if (starting_height == 0):
            starting_height += 1
        if (starting_height == self.height-1):
            starting_height -= 1
        if (starting_width == 0):
            starting_width += 1
        if (starting_width == self.width-1):
            starting_width -= 1

        # Mark it as cell(path) and add surrounding walls to the list
        self.maze[starting_height][starting_width] = cell
        walls = []
        walls.append([starting_height - 1, starting_width])
        walls.append([starting_height, starting_width - 1])
        walls.append([starting_height, starting_width + 1])
        walls.append([starting_height + 1, starting_width])

        # Denote walls in maze
        self.maze[starting_height-1][starting_width] = 'W'
        self.maze[starting_height][starting_width - 1] = 'W'
        self.maze[starting_height][starting_width + 1] = 'W'
        self.maze[starting_height + 1][starting_width] = 'W'

        while (walls):
            # Pick a random wall
            rand_wall = walls[int(random.random()*len(walls))-1]

            # Check if it is a left wall
            if (rand_wall[1] != 0):
                if (self.maze[rand_wall[0]][rand_wall[1]-1] == 'u' and self.maze[rand_wall[0]][rand_wall[1]+1] == 'p'):
                    # Find the number of surrounding cells
                    s_cells = self.surroundingCells(rand_wall)

                    if (s_cells < 2):
                        # Denote the new path
                        self.maze[rand_wall[0]][rand_wall[1]] = 'p'

                        # Mark the new walls
                        # Upper cell
                        if (rand_wall[0] != 0):
                            if (self.maze[rand_wall[0]-1][rand_wall[1]] != 'p'):
                                self.maze[rand_wall[0]-1][rand_wall[1]] = 'W'
                            if ([rand_wall[0]-1, rand_wall[1]] not in walls):
                                walls.append([rand_wall[0]-1, rand_wall[1]])


                        # Bottom cell
                        if (rand_wall[0] != self.height-1):
                            if (self.maze[rand_wall[0]+1][rand_wall[1]] != 'p'):
                                self.maze[rand_wall[0]+1][rand_wall[1]] = 'W'
                            if ([rand_wall[0]+1, rand_wall[1]] not in walls):
                                walls.append([rand_wall[0]+1, rand_wall[1]])

                        # Leftmost cell
                        if (rand_wall[1] != 0):	
                            if (self.maze[rand_wall[0]][rand_wall[1]-1] != 'p'):
                                self.maze[rand_wall[0]][rand_wall[1]-1] = 'W'
                            if ([rand_wall[0], rand_wall[1]-1] not in walls):
                                walls.append([rand_wall[0], rand_wall[1]-1])
                    

                    # Delete wall
                    for wall in walls:
                        if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
                            walls.remove(wall)

                    continue

            # Check if it is an upper wall
            if (rand_wall[0] != 0):
                if (self.maze[rand_wall[0]-1][rand_wall[1]] == 'u' and self.maze[rand_wall[0]+1][rand_wall[1]] == 'p'):

                    s_cells = self.surroundingCells(rand_wall)
                    if (s_cells < 2):
                        # Denote the new path
                        self.maze[rand_wall[0]][rand_wall[1]] = 'p'

                        # Mark the new walls
                        # Upper cell
                        if (rand_wall[0] != 0):
                            if (self.maze[rand_wall[0]-1][rand_wall[1]] != 'p'):
                                self.maze[rand_wall[0]-1][rand_wall[1]] = 'W'
                            if ([rand_wall[0]-1, rand_wall[1]] not in walls):
                                walls.append([rand_wall[0]-1, rand_wall[1]])

                        # Leftmost cell
                        if (rand_wall[1] != 0):
                            if (self.maze[rand_wall[0]][rand_wall[1]-1] != 'p'):
                                self.maze[rand_wall[0]][rand_wall[1]-1] = 'W'
                            if ([rand_wall[0], rand_wall[1]-1] not in walls):
                                walls.append([rand_wall[0], rand_wall[1]-1])

                        # Rightmost cell
                        if (rand_wall[1] != self.width-1):
                            if (self.maze[rand_wall[0]][rand_wall[1]+1] != 'p'):
                                self.maze[rand_wall[0]][rand_wall[1]+1] = 'W'
                            if ([rand_wall[0], rand_wall[1]+1] not in walls):
                                walls.append([rand_wall[0], rand_wall[1]+1])

                    # Delete wall
                    for wall in walls:
                        if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
                            walls.remove(wall)

                    continue

            # Check the bottom wall
            if (rand_wall[0] != self.height-1):
                if (self.maze[rand_wall[0]+1][rand_wall[1]] == 'u' and self.maze[rand_wall[0]-1][rand_wall[1]] == 'p'):

                    s_cells = self.surroundingCells(rand_wall)
                    if (s_cells < 2):
                        # Denote the new path
                        self.maze[rand_wall[0]][rand_wall[1]] = 'p'

                        # Mark the new walls
                        if (rand_wall[0] != self.height-1):
                            if (self.maze[rand_wall[0]+1][rand_wall[1]] != 'p'):
                                self.maze[rand_wall[0]+1][rand_wall[1]] = 'W'
                            if ([rand_wall[0]+1, rand_wall[1]] not in walls):
                                walls.append([rand_wall[0]+1, rand_wall[1]])
                        if (rand_wall[1] != 0):
                            if (self.maze[rand_wall[0]][rand_wall[1]-1] != 'p'):
                                self.maze[rand_wall[0]][rand_wall[1]-1] = 'W'
                            if ([rand_wall[0], rand_wall[1]-1] not in walls):
                                walls.append([rand_wall[0], rand_wall[1]-1])
                        if (rand_wall[1] != self.width-1):
                            if (self.maze[rand_wall[0]][rand_wall[1]+1] != 'p'):
                                self.maze[rand_wall[0]][rand_wall[1]+1] = 'W'
                            if ([rand_wall[0], rand_wall[1]+1] not in walls):
                                walls.append([rand_wall[0], rand_wall[1]+1])

                    # Delete wall
                    for wall in walls:
                        if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
                            walls.remove(wall)


                    continue

            # Check the right wall
            if (rand_wall[1] != self.width-1):
                if (self.maze[rand_wall[0]][rand_wall[1]+1] == 'u' and self.maze[rand_wall[0]][rand_wall[1]-1] == 'p'):

                    s_cells = self.surroundingCells(rand_wall)
                    if (s_cells < 2):
                        # Denote the new path
                        self.maze[rand_wall[0]][rand_wall[1]] = 'p'

                        # Mark the new walls
                        if (rand_wall[1] != self.width-1):
                            if (self.maze[rand_wall[0]][rand_wall[1]+1] != 'p'):
                                self.maze[rand_wall[0]][rand_wall[1]+1] = 'W'
                            if ([rand_wall[0], rand_wall[1]+1] not in walls):
                                walls.append([rand_wall[0], rand_wall[1]+1])
                        if (rand_wall[0] != self.height-1):
                            if (self.maze[rand_wall[0]+1][rand_wall[1]] != 'p'):
                                self.maze[rand_wall[0]+1][rand_wall[1]] = 'W'
                            if ([rand_wall[0]+1, rand_wall[1]] not in walls):
                                walls.append([rand_wall[0]+1, rand_wall[1]])
                        if (rand_wall[0] != 0):	
                            if (self.maze[rand_wall[0]-1][rand_wall[1]] != 'p'):
                                self.maze[rand_wall[0]-1][rand_wall[1]] = 'W'
                            if ([rand_wall[0]-1, rand_wall[1]] not in walls):
                                walls.append([rand_wall[0]-1, rand_wall[1]])

                    # Delete wall
                    for wall in walls:
                        if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
                            walls.remove(wall)

                    continue

            # Delete the wall from the list anyway
            for wall in walls:
                if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
                    walls.remove(wall)

        # Mark the remaining unvisited cells as walls
        for i in range(0, self.height):
            for j in range(0, self.width):
                if (self.maze[i][j] == 'u'):
                    self.maze[i][j] = 'W'

        # Set entrance and exit
        for i in range(0, self.width):
            if (self.maze[1][i] == 'p'):
                self.maze[0][i] = 'p'
                break

        for i in range(self.width-1, 0, -1):
            if (self.maze[self.height-2][i] == 'p'):
                self.maze[self.height-1][i] = 'p'
                break

        # Print final maze
        self.printMaze()


    def gatherMaze(self): 
        self.createLeftMaze()
        rightMaze = np.fliplr(self.maze)
        inMaze = np.concatenate((self.maze, rightMaze), axis=1)
        #adding top, bottom lines
        pathLine = np.chararray([1,28])
        pathLine [:] = 'W'
        pathLine[:, 1:27] = 'p'
        inMaze = np.concatenate((pathLine, inMaze), axis=0)
        inMaze = np.concatenate((inMaze, pathLine), axis=0)
        self.maze = inMaze
        
        #slice into array
        self.array[4:33,:] = self.maze
        return self.array

    #printing for human-eye 
    def prin(self):
        with np.printoptions(threshold=np.inf):
            print(self.array)

if __name__ == "__main__":
    GenMaze = Maze()
    GenMaze.prin()
    GenMaze.array.type