"""
GWV-WS1718:
LabyrinthSearch (Python 2.7)
by Thomas Hofmann and Yannic Boysen
"""

# to use end functionallity
from __future__ import print_function
# for future exercises
import Queue
import numpy as np

# Blatt 3:
def importLabyrinth(file):
    # load file with labyrinth information
    environment = open(file, "r")
    labyrinth = []
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
        labyrinth.append(row)
    environment.close()
    return labyrinth, startCoords, goalCoords

def printLabyrinth(lab, robot = (0, [0, 0])):
    labyrinth, start, goal = lab
    # iterate through the internal structure (2d array)
    for y, row in enumerate(labyrinth):
        for x, c in enumerate(row):
            #print different symbols for ASCII representation
            if robot[0] & (robot[1] == [x+1, y+1]):   # optional robot
                print("r", end=" ")
            elif (start == [x+1, y+1]):
                print("s", end=" ")
            elif (goal == [x+1, y+1]):
                print("g", end=" ")
            elif c:
                print(" ", end=" ")
            else:
                print("x", end=" ")
        print("\n")

# testing functionality
lab1 = importLabyrinth("ev1.txt")
printLabyrinth(lab1)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Blatt 4: WIP
def bfs(lab):
    labyrinth, start, goal = lab
    q = Queue()
    q.enqueue(start)
    while q:
        front = q.dequeue()
        if front == goal:
            return q
        for node in getNext(front):
            print()

def getNext(front):
    nextNodes = []
    additionTuples = np.array([[0,-1], [-1,0], [0,1], [1,0]])
    for t in additionTuples:
        print()