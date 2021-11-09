import pygame
from pygame.locals import *
from constants import *
from pacman import Pacman
from nodes import NodeGroup
from fruit import Fruit
from sprites import MazeSprites
import numpy as np
import pprint
from timeit import default_timer as timer
from pellets import Pellet, PelletGroup
from queue import PriorityQueue
from mapgen import Maze



class SearchControl(object):
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREENSIZE, 0, 32)
        #self.background = None
        self.clock = pygame.time.Clock() 
        self.fruit = None
        
        


    

    def search(self, startNode, endNode):
        
        #startUFC = timer()
        ucsPath, ucsExpanded = self.ufc(startNode, endNode)
        lengt = len(ucsPath)
        print("ufc path"+str(lengt))
        print("ufc count of visited nodes"+str(ucsExpanded))
        endUFC = timer()
        #print(str(endUFC - startUFC)+" -- ufc")
        startDFS = timer()
        #self.dfs(startNode, endNode)
        endDFS = timer()
        #print(str(endDFS - startDFS)+" -- dfs")
        startBFS = timer()
        #self.bfs(startNode, endNode)
        endBFS = timer()
        #print(str(endBFS - startBFS)+" -- bfs")
       
        

    def bfs(self, startNode, endNode):
        visited = []
        queue = [(startNode,[startNode])]
        visited.append(startNode)
        while queue:
            current, path = queue.pop(0) 

            for neighbour in self.nodes.nodesLUT[current.position.asTuple()].neighbors:
                if self.nodes.nodesLUT[current.position.asTuple()].neighbors[neighbour] not in visited and self.nodes.nodesLUT[current.position.asTuple()].neighbors[neighbour]:
                    visited.append(self.nodes.nodesLUT[current.position.asTuple()].neighbors[neighbour])
                    queue.append([self.nodes.nodesLUT[current.position.asTuple()].neighbors[neighbour], (path + [self.nodes.nodesLUT[current.position.asTuple()].neighbors[neighbour]])])
                    if self.nodes.nodesLUT[current.position.asTuple()].neighbors[neighbour] == endNode:
                        path.append(endNode)
                        for x in path:
                            print(x.position.__str16__())
                        return path

    def dfs(self, startNode, endNode):
        visited = []
        stack = [(startNode,[startNode])]
        
        visited.append(startNode)


        while stack:
            current, path = stack.pop() 
           
            
            for neighbour in self.nodes.nodesLUT[current.position.asTuple()].neighbors:
                #print(self.nodes.nodesLUT[current.position.asTuple()].neighbors[neighbour]) 
                if self.nodes.nodesLUT[current.position.asTuple()].neighbors[neighbour] not in visited and self.nodes.nodesLUT[current.position.asTuple()].neighbors[neighbour]:
                    visited.append(self.nodes.nodesLUT[current.position.asTuple()].neighbors[neighbour])
                    stack.append([self.nodes.nodesLUT[current.position.asTuple()].neighbors[neighbour], (path + [self.nodes.nodesLUT[current.position.asTuple()].neighbors[neighbour]])])
                    if self.nodes.nodesLUT[current.position.asTuple()].neighbors[neighbour] == endNode:
                        path.append(endNode)
                        for x in path:
                            print(x.position.__str16__())
                        return path
    


    def ufc(self, startNode, endNode):
        visited = []
        ident = 0
        pqueue = PriorityQueue()
        pqueue.put((0, (ident, startNode, [startNode])))  #cost, node, path
        countExp = 0
        while pqueue:

            cost, bunch  = pqueue.get() 
            
            current = bunch[1] 
            path = bunch[2]
            if current not in visited: 
                countExp += 1
                visited.append(current)
            if current == endNode:
                # for x in path:
                #     print(x.position.__str16__())
                return path, countExp
            else:
                for neighbour in self.nodes.nodesLUT[current.position.asTuple()].neighbors:
                    
                    if self.nodes.nodesLUT[current.position.asTuple()].neighbors[neighbour] not in visited and self.nodes.nodesLUT[current.position.asTuple()].neighbors[neighbour]:
                        #check for cost
                        ident+=1
                        newCost = 0
                        for x in self.pellets.pelletList:
                            if x.position == self.nodes.nodesLUT[current.position.asTuple()].neighbors[neighbour].position:
                                #print(self.nodes.nodesLUT[current.position.asTuple()].position.asTuple())
                                objectName = x.name
                            else:
                                objectName = ""
                        if objectName == PELLET:
                            newCost = 30
                        elif objectName == POWERPELLET:
                            newCost = 0
                        else:
                            newCost = 100
                        
                        pqueue.put((cost + newCost, (ident, self.nodes.nodesLUT[current.position.asTuple()].neighbors[neighbour], path + [self.nodes.nodesLUT[current.position.asTuple()].neighbors[neighbour]])))
                    
    

    def update(self, startX,startY, endX, endY, allCoins):
        dt = self.clock.tick(30) / 1000.0 
        #self.pacman.update(dt)
        
        self.checkEvents()
        self.render(startX,startY, endX, endY, allCoins)

    def checkEvents(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            elif event.type == KEYDOWN:
                #add search
                if event.key == K_s:
                    self.pacman.visible = True
                    self.ghosts.hide()


    def checkFruitEvents(self):  
        if self.fruit is None:
            self.fruit = Fruit(self.nodes.getNodeFromTiles(26, 4))
        # if self.fruit is not None:
        #     if self.pacman.collideCheck(self.fruit):
        #         self.fruit = None
        #     elif self.fruit.destroy:
        #         self.fruit = None
    
    def setBackground(self):
            self.background = pygame.surface.Surface(SCREENSIZE).convert()
            self.background.fill(BLACK)
    
    def startGame(self):
        self.setBackground()
        #MAZE SETTING
        self.maze = Maze()
        self.maze.array=self.maze.array.decode("utf-8")
        #self.mazesprites = MazeSprites("maze.txt", "beautify/block0.PNG")
        self.mazesprites = MazeSprites(self.maze.array, "beautify/block0.PNG")
        self.background = self.mazesprites.constructBackground(self.background, 0)

        #self.nodes = NodeGroup("maze.txt")
        self.nodes = NodeGroup(self.maze.array)

        with np.printoptions(threshold=np.inf):
            print(self.maze.array)
        #self.fruit = Fruit(self.nodes.getNodeFromTiles(26, 4))
        #self.pacman = Pacman(self.nodes.getNodeFromTiles(1, 32))#we start here
        #self.pellets = PelletGroup("maze.txt")
        self.pellets = PelletGroup(self.maze.array)

    def render(self, startX,startY, endX, endY, allCoins):
        self.screen.blit(self.background, (0, 0))
        #for skeleton purpose
        #self.nodes.render(self.screen)
        pygame.draw.rect(self.screen, WHITE, pygame.Rect(startX*TILEWIDTH,startY*TILEHEIGHT,TILEWIDTH,TILEHEIGHT))
        pygame.draw.rect(self.screen, RED, pygame.Rect(endX*TILEWIDTH,endY*TILEHEIGHT,TILEWIDTH,TILEHEIGHT))
        for each in allCoins:
            x, y = each
            pygame.draw.rect(self.screen, YELLOW, pygame.Rect(x,y,TILEWIDTH,TILEHEIGHT))

        self.pellets.render(self.screen) 

        if self.fruit is not None:
            self.fruit.render(self.screen)
        # self.pacman.render(self.screen)
        pygame.display.update()

    
    #add A* things like heuristics, tile paint,etcetera, greedy algoritm
    #we have open list
    #closed list
    #put the first tile in open list
    # foreach tile in open list
    #add current tile to closed list
    #add all neighbours to open list
    #way through 4 nodes
    #1. double manhattan(g+h)
    #2. greedy(only nodes left to goal(manhattan))
    #3. sub-optimal (g+h())
    def AStarManhattan(self, startNode, endNode, D):

        
        ident = 0
        ccost = 0 #current cost
        open = PriorityQueue()
        closed = []
        dist = D * self.Manhattan(self.nodes.nodesLUT[endNode.position.asTuple()].position.asInt(), self.nodes.nodesLUT[startNode.position.asTuple()].position.asInt())
        #print(dist)
        #totalcost = manhattan + cost so far
        f = dist + 0
        open.put((f, (ident, ccost, startNode, [startNode])))  #totalcost, cost, node, path
        countExpanded = 0
        while open:

            f, bunch  = open.get() 

            ccost = bunch[1]
            current = bunch[2] 
            path = bunch[3]
            if current not in closed: 
                countExpanded +=1
                closed.append(current)
            if current == endNode:
                # for x in path:
                #print(x.position.__str16__())
                return path, countExpanded
            else:
                for neighbour in self.nodes.nodesLUT[current.position.asTuple()].neighbors:
                    
                    if self.nodes.nodesLUT[current.position.asTuple()].neighbors[neighbour] not in closed and self.nodes.nodesLUT[current.position.asTuple()].neighbors[neighbour]:
                        #check for cost
                        ident+=1
                        newCost = 0 
                        for x in self.pellets.pelletList:
                            if x.position == self.nodes.nodesLUT[current.position.asTuple()].neighbors[neighbour].position:
                                #print(self.nodes.nodesLUT[current.position.asTuple()].position.asTuple())
                                objectName = x.name
                            else:
                                objectName = ""
                        if objectName == PELLET:
                            newCost = 30
                        elif objectName == POWERPELLET:
                            newCost = 0
                        else:
                            newCost = 100

                        g = newCost + ccost
                        dist =D * self.Manhattan(self.nodes.nodesLUT[endNode.position.asTuple()].position.asInt(), self.nodes.nodesLUT[current.position.asTuple()].neighbors[neighbour].position.asInt())
                        f = g + dist
                        open.put((f, (ident, g, self.nodes.nodesLUT[current.position.asTuple()].neighbors[neighbour], path + [self.nodes.nodesLUT[current.position.asTuple()].neighbors[neighbour]])))
        


    def AStarGreedy(self, startNode, endNode,D):

        ident = 0
        #ccost = 0 #current cost
        open = PriorityQueue()
        closed = []
        dist = D * self.Manhattan(self.nodes.nodesLUT[endNode.position.asTuple()].position.asInt(), self.nodes.nodesLUT[startNode.position.asTuple()].position.asInt())
        #print(dist)
        #totalcost = manhattan + cost so far
        f = dist + 0 #always zero
        open.put((f, (ident,  startNode, [startNode])))  #totalcost, cost, node, path
        countExpanded = 0
        while open:
            f, bunch  = open.get() 
            current = bunch[1] 
            path = bunch[2]
            if current not in closed: 
                countExpanded +=1
                closed.append(current)
            if current == endNode:
                # for x in path:
                #     print(x.position.__str16__())
                return path, countExpanded
                
            else:
                for neighbour in self.nodes.nodesLUT[current.position.asTuple()].neighbors:
                    
                    if self.nodes.nodesLUT[current.position.asTuple()].neighbors[neighbour] not in closed and self.nodes.nodesLUT[current.position.asTuple()].neighbors[neighbour]:
                        #check for cost
                        ident+=1
                        dist = D * self.Manhattan(self.nodes.nodesLUT[endNode.position.asTuple()].position.asInt(), self.nodes.nodesLUT[current.position.asTuple()].neighbors[neighbour].position.asInt())
                        f = 0 + dist
                        open.put((f, (ident, self.nodes.nodesLUT[current.position.asTuple()].neighbors[neighbour], path + [self.nodes.nodesLUT[current.position.asTuple()].neighbors[neighbour]])))
        


    def AStarOptimistic(self, startNode, endNode,D):

        
        ident = 0
        ccost = 0 #current cost
        open = PriorityQueue()
        closed = []
        dist = (2*D - 1) * self.Manhattan(self.nodes.nodesLUT[endNode.position.asTuple()].position.asInt(), self.nodes.nodesLUT[startNode.position.asTuple()].position.asInt())
        #print(dist)
        #totalcost = manhattan + cost so far
        f = dist + 0
        #f = g + (2*D-1)
        open.put((f, (ident, ccost, startNode, [startNode])))  #totalcost, cost, node, path
        countExpanded = 0
        while open:

            f, bunch  = open.get() 

            ccost = bunch[1]
            current = bunch[2] 
            path = bunch[3]
            if current not in closed: 
                countExpanded +=1
                closed.append(current)
            if current == endNode:
                # for x in path:
                #print(x.position.__str16__())
                return path, countExpanded
            else:
                for neighbour in self.nodes.nodesLUT[current.position.asTuple()].neighbors:
                    
                    if self.nodes.nodesLUT[current.position.asTuple()].neighbors[neighbour] not in closed and self.nodes.nodesLUT[current.position.asTuple()].neighbors[neighbour]:
                        #check for cost
                        ident+=1
                        newCost = 0 
                        for x in self.pellets.pelletList:
                            if x.position == self.nodes.nodesLUT[current.position.asTuple()].neighbors[neighbour].position:
                                #print(self.nodes.nodesLUT[current.position.asTuple()].position.asTuple())
                                objectName = x.name
                            else:
                                objectName = ""
                        if objectName == PELLET:
                            newCost = 30
                        elif objectName == POWERPELLET:
                            newCost = 0
                        else:
                            newCost = 100

                        g = newCost + ccost
                        dist = (2*D - 1) * self.Manhattan(self.nodes.nodesLUT[endNode.position.asTuple()].position.asInt(), self.nodes.nodesLUT[current.position.asTuple()].neighbors[neighbour].position.asInt())
                        f = g + dist
                        open.put((f, (ident, g, self.nodes.nodesLUT[current.position.asTuple()].neighbors[neighbour], path + [self.nodes.nodesLUT[current.position.asTuple()].neighbors[neighbour]])))


    def Manhattan(self, end, current):
        #D - weight, approx.  difference between two adj nodes
        #counted according to spawn probs:
        #pellet - 60%(cost 30), powerpellet - 5%(cost 0), nothing - 35%(cost 100)
        #http://theory.stanford.edu/~amitp/GameProgramming/Heuristics.html
        

        endX, endY = end
        currentX, currentY = current
        dist = abs(endX/16 - currentX/16) + abs(endY/16 - currentY/16)
        return dist
        

    def AllBigCoins(self,D):

        #get list of pp
        #self.pellets.pelletList
        #self.name = PELLET
        #self.position = Vector2(column*TILEWIDTH, row*TILEHEIGHT)
        coinsList = []
        for inst in self.pellets.pelletList:
            if inst.name == POWERPELLET:
                coinsList.append(inst.position.asInt())
        #print(coinsList)
        # current = coinsList.pop(0)
        # print(current)
        # x = current[0]
        # y = current[1]

        #add first pp location as startnode to look from there
        source = [coinsList[0]]
        print(source)
        coinsList.remove(coinsList[0])
        print(coinsList)

        while(coinsList):
            queueToGo = PriorityQueue()
            ident = 0

            #find greedy-best nodes to connect
            for start in source:
                for end in coinsList:
                    # print(start)
                    # print(end)
                    dist = D * self.Manhattan(end, start)
                    ident += 1
                    queueToGo.put((dist, (ident, start, end)))

            #get start - end node
            d, bunch =queueToGo.get()
            nodeStart = bunch[1]
            nodeEnd = bunch[2]
            # print(nodeStart)
            startNode = game.nodes.nodesLUT[nodeStart]
            endNode = game.nodes.nodesLUT[nodeEnd]
            # GO GREEDY
            curPath, visitedNodes = self.AStarGreedy(startNode, endNode, D)
            print(len(curPath))

            for element in curPath:
                source.append(element.position.asInt())

            

            #
            #
            
            for each in source:
                if each in coinsList:
                    print("+")
                    coinsList.remove(each)

        print("source", source, len(source))
        return source

        
        
        


        





        

        
        
        



    
pygame.display.set_caption('Lady Pacman')    
if __name__ == "__main__":
    game = SearchControl()
    startX, startY = 26, 4
    endX, endY = 1, 32
    game.startGame()      #пофиксить старгейм
                        #пофиксить

    startNode = game.nodes.nodesLUT[(startX * 16, startY * 16)]
    endNode = game.nodes.nodesLUT[(endX * 16, endY * 16)]
    D = 53
    #define start nodes
    # run astar
    


    #A* manhattan
    AStarPath, AStarCountExp = game.AStarManhattan(startNode, endNode, D)
    lenMan = len(AStarPath)
    print("AStar path"+str(lenMan))
    print("AStar count of visited nodes"+str(AStarCountExp))

    #A* Greedy
    AStarGreedyPath, AStarGreedyExp = game.AStarGreedy(startNode, endNode, D)
    lenGreedy = len(AStarGreedyPath)
    print("Greedy path"+str(lenGreedy))
    print("Greedy count of visited nodes"+str(AStarGreedyExp))

    #A* Optimistic(suboptimal)
    subOptPath, NumberVisited = game.AStarOptimistic(startNode, endNode, D)
    lensubOptPath = len(subOptPath)
    print("Optimistic path"+str(lensubOptPath))
    print("Optimistic count of visited nodes"+str(NumberVisited))

    allCoins = game.AllBigCoins(D)
    print(len(allCoins))
    
    


    



    while True:
        game.update(startX,startY, endX, endY, allCoins)
        

    

    
