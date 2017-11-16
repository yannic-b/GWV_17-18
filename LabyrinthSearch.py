"""
GWV-WS1718:
LabyrinthSearch (Python 2.7)
by Thomas Hofmann and Yannic Boysen
"""

# to use end functionallity
from __future__ import print_function
from time import time
from itertools import count
from scipy.spatial.distance import cityblock
import Queue
import numpy as np

'''
Exercise 4.2:
1),2) and 5) implemented in code...
3)  ev5 shows the advantages of bfs, where close goals are found really fast,
    while ev6 shows the advantages of dfs, which can find specific far goals quicker,
    if they are in line with the movement priorities (here: left first).
    [Results may vary because of small mazes]
4)  in ev2 no solution is found, since the goal is not reachable 
'''

# class representing the labyrinth with functions to import, print etc.
class Labyrinth:

    def __init__(self, fileName):
        self.file = fileName
        self.labyrinth = []
        self.start = []
        self.goal = []
        self.portals = {}
        self.importLabyrinth()
        # print(str(self.start), str(self.goal))

    # Blatt 3:
    def importLabyrinth(self):
        # load file with labyrinth information
        environment = open(self.file, "r")
        lab = []
        # iterate through the lab and save 0 for every x and 1 for every free spot / start / end.
        for y, line in enumerate(environment):
            row = []
            for x, character in enumerate(line):
                if character == 'x':
                    row.append(0)
                else:
                    # portal check
                    if character.isdigit():
                        self.portals[str(np.array([y, x]))] = character
                    # save start and goal
                    elif character == 's':
                        startCoords = [y, x]
                    elif character == 'g':
                        goalCoords = [y, x]
                    row.append(1)
            # append whole row to array
            lab.append(row)
        environment.close()
        self.labyrinth = np.array(lab)
        self.start = np.array(startCoords)
        self.goal = np.array(goalCoords)
        # print(self.portals)

    def printLabyrinth(self, path, robot=(0, [0, 0])):
        # iterate through the internal structure (2d array)
        for y, row in enumerate(self.labyrinth):
            for x, c in enumerate(row):
                p = path[1]
                # print different symbols for ASCII representation
                if robot[0] & np.all(robot[1] == [y, x]):   # optional robot
                    print("r", end="")
                elif str(np.array([y, x])) in self.portals.keys():
                    print(self.portals[str(np.array([y, x]))], end="")
                elif np.all(self.start == [y, x]):
                    print("s", end="")
                elif np.all(self.goal == [y, x]):
                    print("g", end="")
                elif path[0] & np.all(p[y][x]):
                    print("*", end="")
                elif c:
                    print(" ", end="")
                else:
                    print("x", end="")
            print("")

    # Blatt 4:

    # generic search function, which can do both bfs and dfs depending on collection type:
    def search(self, searchType):
        visitedNodes = np.array(self.labyrinth * 0)
        dictForNextNode = {}

        maxNodes = 0
        expansionCounter = 1
        # create queue and add start
        if searchType == "bf":
            c = Queue.Queue()
        elif searchType == "df":
            c = Queue.LifoQueue()
        # create mirror of q to be able to use "not in"
        qMirrorSet = set()
        # add start to q and qMirrorSet (using numpy arrays String function as hashable)
        c.put(self.start)
        qMirrorSet.add(str(self.start))
        dictForNextNode[str(self.start)] = (None, None)
        # start search, while q is not empty
        while not c.empty():
            # print(qMirrorSet)
            # remove current node from q and add to front
            front = c.get()
            qMirrorSet.remove(str(front))
            # check if current node is goal
            if np.all(front == self.goal):
                print("Success, goal at:", front, " was found!")
                # print(dictForNextNode)
                print("Path:", self.getPath(front, dictForNextNode))
                print("There were a maximum of", maxNodes, "nodes on the frontier.")
                print(expansionCounter, "expansion operations were performed.")
                break
            # find next valid Nodes
            for (node, vector) in self.getNext(front):
                if np.all(visitedNodes[node[0], node[1]]):
                    continue
                if str(node) not in qMirrorSet:
                        dictForNextNode[str(node)] = (front, vector)
                        c.put(node)
                        expansionCounter += 1
                        if c.qsize() > maxNodes:
                            maxNodes = c.qsize()
                        qMirrorSet.add(str(node))
                visitedNodes[front[0], front[1]] = 1
                # print(node)

    # function to calculate backwards path starting at the goal
    def getPath(self, state, dictForNextNode):
        out = []
        path = []
        while state is not None:
            # print(state)
            row = dictForNextNode[str(state)]
            path.append(state)
            out.append(str(state))
            state = row[0]
        p = self.labyrinth * 0
        for x in path:
            # print(x[0], x[1])
            p[x[0], x[1]] = 1
        self.printLabyrinth((1, p), (0, []))
        # return path in correct orientation
        return out[::-1]

    # function to return valid next Nodes
    def getNext(self, front):
        nextNodes = []
        vectors = []
        # all theoretically possible direction vectors for to lan on next Nodes
        additionVectors = np.array([[0, -1], [-1, 0], [0, 1], [1, 0]])
        # handling portals
        if str(front) in self.portals.keys():
            # print("Portal!:", front)
            portal = self.portals[str(front)]
            for coord in self.portals.keys():
                if (self.portals[coord] == portal) & (coord != str(front)):
                    front = np.fromstring(coord[1:-1], dtype=int, sep=' ')
        # calculating nextNodes
        for vector in additionVectors:
            # check if newNode is valid in labyrinth
            node = (front+vector)
            # print(node)
            if np.all(np.greater(self.labyrinth.shape, np.add(node, 1))):
                if np.any(self.labyrinth[node[0], node[1]]):
                    # print("Tru")
                    nextNodes.append(node)
                    vectors.append(vector)
        out = np.array(zip(nextNodes, vectors))
        # print(out)
        return out

    # generic search function, which can do both bfs and dfs depending on collection type:
    def aSearch(self):
        visitedNodes = np.array(self.labyrinth * 0)
        dictForNextNode = {}

        maxNodes = 0
        expansionCounter = 1
        # create queue and add start
        c = Queue.PriorityQueue()
        # create mirror of q to be able to use "not in"
        qMirrorSet = set()
        # add start to q and qMirrorSet (using numpy arrays String function as hashable)

        qMirrorSet.add(str(self.start))
        dictForNextNode[str(self.start)] = (None, None)

        tiebreaker = count()

        gScore = {}
        gScore[str(self.start)] = 0.0

        fScore = {}
        fScore[str(self.start)] = self.manDis(self.start, self.goal)

        c.put((fScore[str(self.start)], next(tiebreaker), self.start))

        # start search, while q is not empty
        while not c.empty():
            # print(qMirrorSet)
            # remove current node from q and add to front
            front = c.get()[2]
            qMirrorSet.remove(str(front))
            # check if current node is goal
            if np.all(front == self.goal):
                print("Success, goal at:", front, " was found!")
                # print(dictForNextNode)
                print("Path:", self.getPath(front, dictForNextNode))
                print("There were a maximum of", maxNodes, "nodes on the frontier.")
                print(expansionCounter, "expansion operations were performed.")
                return(0)
            # find next valid Nodes
            for (node, vector) in self.getNextA(front):
                if np.all(visitedNodes[node[0], node[1]]):
                    continue
                gScore[str(node)] = gScore[str(front)] + self.manDis(front, node)
                fScore[str(node)] = gScore[str(node)] + self.manDis(node, self.goal)
                if str(node) not in qMirrorSet:
                    dictForNextNode[str(node)] = (front, vector)
                    # print(gScore[str(node)], fScore[str(node)])
                    expansionCounter += 1
                    if c.qsize() > maxNodes:
                        maxNodes = c.qsize()
                    c.put((fScore[str(node)], next(tiebreaker), node))
                    qMirrorSet.add(str(node))
                visitedNodes[front[0], front[1]] = 1
                # print(node)
        print("A* search failed, no goal was found.")
        return(1)


    # function to return valid next Nodes
    def getNextA(self, front):
        nextNodes = []
        vectors = []
        # all theoretically possible direction vectors for to lan on next Nodes
        additionVectors = np.array([[0, -1], [-1, 0], [0, 1], [1, 0]])
        # handling portals
        if str(front) in self.portals.keys():
            # print("Portal!:", front)
            portal = self.portals[str(front)]
            for coord in self.portals.keys():
                portalBetter = self.manDis(front, self.goal) >= self.manDis(np.fromstring(coord[1:-1], dtype=int, sep=' '), self.goal)
                if (self.portals[coord] == portal) & (coord != str(front)) & portalBetter:
                    front = np.fromstring(coord[1:-1], dtype=int, sep=' ')
        # calculating nextNodes
        for vector in additionVectors:
            # check if newNode is valid in labyrinth
            node = (front + vector)
            # print(node)
            if np.all(np.greater(self.labyrinth.shape, np.add(node, 1))):
                if np.any(self.labyrinth[node[0], node[1]]):
                    # print("Tru")
                    nextNodes.append(node)
                    vectors.append(vector)
        out = np.array(zip(nextNodes, vectors))
        # print(out)
        return out

    # function to calculate manhatten distance
    def manDis(self, node1, node2):
        return cityblock(node1, node2)

    # breadth-first-search:
    def bfs(self):
        self.search("bf")

    # depth-first-search:
    def dfs(self):
        self.search("df")


# END CLASS


# testing functionality
labyrinths = ["ev0.txt", "ev1.txt", "ev2.txt", "ev3.txt", "ev4.txt", "ev5.txt", "ev6.txt"]

for lab in labyrinths:
    print("Testing:", lab)
    l = Labyrinth(lab)
    path = l.labyrinth * 0
    #l.printLabyrinth((1, path), (0, [0, 0]))
    start = time()
    l.bfs()
    finish = time()
    print("The search in", lab, "using bfs, took", finish - start, "seconds.\n")
    start = time()
    l.dfs()
    finish = time()
    print("The search in", lab, "using dfs, took", finish-start, "seconds.\n")
    start = time()
    l.aSearch()
    finish = time()
    print("The search in", lab, "using a*, took", finish - start, "seconds.\n")
