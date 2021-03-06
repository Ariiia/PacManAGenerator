import pygame
from constants import *
import numpy as np

BASETILEWIDTH = 16
BASETILEHEIGHT = 16

class Spritesheet(object):
    def __init__(self):
        self.sheet = pygame.image.load("beautify/spritesheet.png").convert()
        self.block = pygame.image.load("beautify/block0.png").convert()
        transcolor = self.sheet.get_at((0,0))
        self.sheet.set_colorkey(transcolor)
        widthBlock = int(self.block.get_width() / BASETILEWIDTH * TILEWIDTH)
        heightBlock = int(self.block.get_height() / BASETILEHEIGHT * TILEHEIGHT)
        width = int(self.sheet.get_width() / BASETILEWIDTH * TILEWIDTH)
        height = int(self.sheet.get_height() / BASETILEHEIGHT * TILEHEIGHT)
        self.block = pygame.transform.scale(self.block, (widthBlock, heightBlock))
        self.sheet = pygame.transform.scale(self.sheet, (width, height))
        
    def getImage(self, x, y, width, height):
        x *= TILEWIDTH
        y *= TILEHEIGHT
        self.sheet.set_clip(pygame.Rect(x, y, width, height))
        return self.sheet.subsurface(self.sheet.get_clip())

    def getImageBlock(self, x, y, widthBlock, heightBlock):
        x *= TILEWIDTH
        y *= TILEHEIGHT
        self.block.set_clip(pygame.Rect(x, y, widthBlock, heightBlock))
        return self.block.subsurface(self.block.get_clip())

class LifeSprites(Spritesheet):
    def __init__(self, numlives):
        Spritesheet.__init__(self)
        self.resetLives(numlives)

    def removeImage(self):
        if len(self.images) > 0:
            self.images.pop(0)

    def resetLives(self, numlives):
        self.images = []
        for i in range(numlives):
            self.images.append(self.getImage(0,0))

    def getImage(self, x, y):
        return Spritesheet.getImage(self, x, y, 2*TILEWIDTH, 2*TILEHEIGHT)

class PacmanSprites(Spritesheet):
    def __init__(self, entity):
        Spritesheet.__init__(self)
        self.entity = entity
        self.entity.image = self.getStartImage()       

    def getStartImage(self):
        return self.getImage(8, 0)

    def getImage(self, x, y):
        return Spritesheet.getImage(self, x, y, 2*TILEWIDTH, 2*TILEHEIGHT)

class GhostSprites(Spritesheet):
    def __init__(self, entity):
        Spritesheet.__init__(self)
        self.x = {BLINKY:0, PINKY:2, INKY:4, CLYDE:6}
        self.entity = entity
        self.entity.image = self.getStartImage()
               
    def getStartImage(self):
        return self.getImage(self.x[self.entity.name], 4)

    def getImage(self, x, y):
        return Spritesheet.getImage(self, x, y, 2*TILEWIDTH, 2*TILEHEIGHT)

class FruitSprites(Spritesheet):
    def __init__(self, entity):
        Spritesheet.__init__(self)
        self.entity = entity
        self.entity.image = self.getStartImage()

    def getStartImage(self):
        return self.getImage(16, 8)

    def getImage(self, x, y):
        return Spritesheet.getImage(self, x, y, 2*TILEWIDTH, 2*TILEHEIGHT)

class MazeSprites(Spritesheet):
    def __init__(self, mazefile,spritefile):
        Spritesheet.__init__(self)
        #self.data = self.readMazeFile(mazefile)
        self.data = mazefile

    def getImage(self, x, y):
        return Spritesheet.getImage(self, x, y, TILEWIDTH, TILEHEIGHT)

    def getImageBlock(self, x, y):
        return Spritesheet.getImageBlock(self, x, y, TILEWIDTH, TILEHEIGHT)

    def readMazeFile(self, mazefile):
        return np.loadtxt(mazefile, dtype='<U1')

    def constructBackground(self, background, y):
        for row in list(range(self.data.shape[0])):
            for col in list(range(self.data.shape[1])):
                if self.data[row][col]=='W':
                    #print(0)
                    sprite = self.getImageBlock(0, 0)
                    #rotval = int(self.rotdata[row][col])
                    # sprite = self.rotate(sprite, rotval)
                    background.blit(sprite, (col*TILEWIDTH, row*TILEHEIGHT))
                    #center doors

                # elif self.data[row][col] == '=':
                #     sprite = self.getImage(10, 8)
                #     background.blit(sprite, (col*TILEWIDTH, row*TILEHEIGHT))

        return background
    
    #0 - 0, 1 - 90, 2 - 180, 3 - 270(rotation.txt)
    # def rotate(self, sprite, value):
    #    return pygame.transform.rotate(sprite, value*90)
