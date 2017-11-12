"""
GWV-WS1718:
LabyrinthSearch (Python 2.7)
by Thomas Hofmann and Yannic Boysen
"""

# to use end functionallity
from __future__ import print_function
from time import time
import Queue
import numpy as np


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
        print(self.portals)

    def printLabyrinth(self, robot=(0, [0, 0])):
        # iterate through the internal structure (2d array)
        for x, row in enumerate(self.labyrinth):
            for y, c in enumerate(row):
                # print different symbols for ASCII representation
                if robot[0] & np.all(robot[1] == [x, y]):   # optional robot
                    print("r", end="")
                elif np.all(self.start == [x, y]):
                    print("s", end="")
                elif np.all(self.goal == [x, y]):
                    print("g", end="")
                elif c:
                    print(" ", end="")
                else:
                    print("x", end="")
            print("")

    # Blatt 4:

    # breadth-first-search:
    def bfs(self):
        visitedNodes = np.array(self.labyrinth * 0)
        dictForNextNode = {}
        # create queue and add start
        q = Queue.Queue()
        # create mirror of q to be able to use "not in"
        qMirrorSet = set()
        # add start to q and qMirrorSet (using numpy arrays String function as hashable)
        q.put(self.start)
        qMirrorSet.add(str(self.start))
        dictForNextNode[str(self.start)] = (None, None)
        # start search, while q is not empty
        while not q.empty():
            # print(qMirrorSet)
            # remove current node from q and add to front
            front = q.get()
            qMirrorSet.remove(str(front))
            # check if current node is goal
            if np.all(front == self.goal):
                print("Success, goal at:", front, " was found!")
                # print(dictForNextNode)
                print("Path:", self.getPath(front, dictForNextNode))
                break
            # find next valid Nodes
            for (node, vector) in self.getNext(front):
                if np.all(visitedNodes[node[0], node[1]]):
                    continue
                if str(node) not in qMirrorSet:
                        dictForNextNode[str(node)] = (front, vector)
                        q.put(node)
                        qMirrorSet.add(str(node))
                visitedNodes[front[0], front[1]] = 1
                # print(node)

    # function to calculate path
    def getPath(self, state, dictForNextNode):
        out = []
        while state is not None:
            # print(state)
            row = dictForNextNode[str(state)]
            if len(row) == 2:
                out.append(str(state))
                state = row[0]
                # vector = row[1]
            else:
                break
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

    # depth-first-search:
    def dfs(self):
        visitedNodes = np.array(self.labyrinth * 0)
        dictForNextNode = {}
        # create queue and add start
        s = Queue.LifoQueue()
        # create mirror of q to be able to use "not in"
        qMirrorSet = set()
        # add start to q and qMirrorSet (using numpy arrays String function as hashable)
        s.put(self.start)
        qMirrorSet.add(str(self.start))
        dictForNextNode[str(self.start)] = (None, None)
        # start search, while q is not empty
        while not s.empty():
            # print(qMirrorSet)
            # remove current node from q and add to front
            front = s.get()
            qMirrorSet.remove(str(front))
            # check if current node is goal
            if np.all(front == self.goal):
                print("Success, goal at:", front, " was found!")
                # print(dictForNextNode)
                print("Path:", self.getPath(front, dictForNextNode))
                break
            # find next valid Nodes
            for (node, vector) in self.getNext(front):
                if np.all(visitedNodes[node[0], node[1]]):
                    continue
                if str(node) not in qMirrorSet:
                    dictForNextNode[str(node)] = (front, vector)
                    s.put(node)
                    qMirrorSet.add(str(node))
                visitedNodes[front[0], front[1]] = 1
                # print(node)


# END CLASS


# testing functionality
labyrinths = ["ev0.txt", "ev1.txt", "ev2.txt", "ev3.txt", "ev4.txt"]

for lab in labyrinths:
    print("Testing:", lab)
    start = time()
    l = Labyrinth(lab)
    l.printLabyrinth()
    l.bfs()
    l.dfs()
    finish = time()
    print("The testing in", lab, "took", finish-start, "seconds.\n")
'''
lab1 = Labyrinth("ev1.txt")
lab1.printLabyrinth()
lab1.bfs()
lab1.dfs()
'''
