"""
GWV-WS1718:
LabyrinthSearch (Python 2.7)
by Thomas Hofmann and Yannic Boysen
"""

# to use end functionallity
from __future__ import print_function
# for future exercises
from Queue import Queue
import numpy as np


# class representing the labyrinth with functions to import, print etc.
class Labyrinth:

    def __init__(self, fileName):
        self.file = fileName
        self.labyrinth = []
        self.start = []
        self.goal = []
        self.importLabyrinth()

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
                    # save start and goal
                    if character == 's':
                        startCoords = [x + 1, y + 1]
                    elif character == 'g':
                        goalCoords = [x + 1, y + 1]
                    row.append(1)
            # append whole row to array
            lab.append(row)
        environment.close()
        self.labyrinth = np.array(lab)
        self.start = np.array(startCoords)
        self.goal = np.array(goalCoords)

    def printLabyrinth(self, robot=(0, [0, 0])):
        # iterate through the internal structure (2d array)
        for y, row in enumerate(self.labyrinth):
            for x, c in enumerate(row):
                # print different symbols for ASCII representation
                if robot[0] & np.all(robot[1] == [x+1, y+1]):   # optional robot
                    print("r", end="")
                elif np.all(self.start == [x+1, y+1]):
                    print("s", end="")
                elif np.all(self.goal == [x+1, y+1]):
                    print("g", end="")
                elif c:
                    print(" ", end="")
                else:
                    print("x", end="")
            print("")

    # Blatt 4: WIP
    def bfs(self):
        q = Queue()
        q.put(self.start)
        while q:
            front = q.get()
            if np.all(front == self.goal):
                return q
            for node in self.getNext(front):
                print(node)

    def getNext(self, front):
        nextNodes = []
        additionTuples = np.array([[0, -1], [-1, 0], [0, 1], [1, 0]])
        for t in additionTuples:
            if np.all(self.labyrinth[front+t]):
                nextNodes.append(self.labyrinth[front+t])
        print(nextNodes)

# END CLASS


# testing functionality
lab1 = Labyrinth("ev1.txt")
lab1.printLabyrinth()
#lab1.bfs()
