"""
GWV-WS1718:
LabyrinthSearch
by Thomas Hofmann and Yannic Boysen
"""

from __future__ import print_function

###Blatt 3:
def importLabyrinth(file):
    environment = open(file, "r")
    labyrinth = []
    for y, line in enumerate(environment):
        l = []
        for x, c in enumerate(line):
            if c == 'x':
                l.append(0)
            else:
                l.append(1)
                if c == 's':
                    startCoords = (x+1,y+1)
                else:
                    goalCoords = (x + 1, y + 1)
        labyrinth.append(l)
    environment.close()
    return (labyrinth, startCoords, goalCoords)

def printLabyrinth(labyrinth):
    for row in labyrinth:
        for c in row:
            if c:
                print(" ", end=" ")
            else:
                print("x", end=" ")
        print("\n")

lab1 = importLabyrinth("ev1.txt")
printLabyrinth(lab1[0])