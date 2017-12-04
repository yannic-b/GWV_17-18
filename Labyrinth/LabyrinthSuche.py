""" GWV Tutorial 3: Searching

Exercise 3.1 .)
	
	1: Lowest Cost First Search

	2: 	Als erstes baut man sich einen Baum aller möglichen Pfade mit der Anzahl an Tickets 
		auf. Und beschriftet die Kanten mit der jeweiligen Distanz in cm, die zurück gelegt wird.
		Dann könnte man mit einem umgekehrten Lowest Cost First Algorithmus den Weg mit der höchsten Distanz festlegen.

"""

# GWV Exercise 3.2


# to use end functionallity
from __future__ import print_function

def importLabyrinth(file):
	#load file with labyrinth information
	labfile = open(file, "r")
	labyrinth = []
	#iterate through the lab and save 0 for every x and 1 for every free spot / start / end.
	for y, row in enumerate(labfile):
		l = []
		for x, column in enumerate(row):
			if column == 'x':
				l.append(0)
			else:
				l.append(1)
				if column == 's':
					start = (x + 1, y + 1)
				if column == 'g':
					end = (x + 1, y + 1)
		# append whole row as a tuple
		labyrinth.append(l)
	labfile.close()
	return labyrinth, start, end

def printLabyrinth(labyrinth):
	# iterate through the internal structure, building the lab without start and end
	for row in labyrinth:
		for column in row:
			if column == 1:
				print (" ", end = " ")
			else:
				print ("x", end = " ")
		print ("\n")

#printing the lab
lab1 = importLabyrinth("ev1.txt")
printLabyrinth(lab1[0])


