import pygame
from vector import Vector2
from constants import *
import numpy as np
import random, time

class Pellet(object):
    def __init__(self, row, column):
        self.name = PELLET
        self.position = Vector2(column*TILEWIDTH, row*TILEHEIGHT)
        self.color = TEAL
        self.radius = int(2 * TILEWIDTH / 16)
        self.collideRadius = int(2 * TILEWIDTH / 16)
        self.points = 10
        self.visible = True

    def render(self, screen):
        if self.visible:
            adjust = Vector2(TILEWIDTH, TILEHEIGHT) /4
            p = self.position + adjust
            pygame.draw.circle(screen, self.color, p.asInt(), self.radius)

class PowerPellet(Pellet):
    def __init__(self, row, column):
        Pellet.__init__(self, row, column)
        self.name = POWERPELLET
        self.radius = int(6 * TILEWIDTH / 16)
        self.points = 50
        self.flashTime = 0.2
        self.timer= 0
        
    def update(self, dt):
        self.timer += dt
        if self.timer >= self.flashTime:
            self.visible = not self.visible
            self.timer = 0

class PelletGroup(object):
    def __init__(self, pelletfile):
        self.pelletList = []
        self.powerpellets = []
        self.createPelletList(pelletfile)
        self.numEaten = 0

    def update(self, dt):
        for powerpellet in self.powerpellets:
            powerpellet.update(dt)
                
    #REMOVED DOTS     
    #change pellet spawns
    def createPelletList(self, pelletfile):
        #data = self.readPelletfile(pelletfile)        
        data = pelletfile
        for row in range(data.shape[0]):
            for col in range(data.shape[1]):
                pelletYes = random.random()
                if data[row][col] in ['p'] and pelletYes > 0.4:
                    self.pelletList.append(Pellet(row, col))
                elif data[row][col] in ['p'] and pelletYes < 0.05:
                    pp = PowerPellet(row, col)
                    self.pelletList.append(pp)
                # elif data[row][col] in ['P', 'p']:
                #     pp = PowerPellet(row, col)
                #     self.pelletList.append(pp)
                #     self.powerpellets.append(pp)
                    
    def readPelletfile(self, textfile):
        return np.loadtxt(textfile, dtype='<U1')
    
    def isEmpty(self):
        if len(self.pelletList) == 0:
            return True
        return False
    
    def render(self, screen):
        for pellet in self.pelletList:
            pellet.render(screen)