#!/Applications/anaconda2/bin/python

"""
Blatt 07: Constraint Satisfaction
Thomas Hofmann, Yannic Boysen

Implementation des Arc Consistency Algorithms
Da das Debugging dieses Algorithmus sehr aufwaendig ist,
konnten wir die Implementation aus Zeitgruenden nicht korrekt fertigstellen.
"""
import csv
import numpy as np
from scipy.spatial.distance import cityblock

# Arc Consistency Algorithm
class ACA:
    def __init__(self, filename):
        self.words, self.charsAtPos, self.variables, self.domains, self.unaryConstraints = [], [], [], [], []
        self.readFile(filename)
        self.determineCharsAtPos()
        self.input()

    # Word list input:
    def readFile(self, file):
        words = []
        with open(file, 'rb') as csvfile:
            wordreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in wordreader:
                for word in row:
                    words.append(word.strip())
                    # print ', '.join(row)
        self.words = words

    def printStuff(self):
        print self.charsAtPos, '\n', self.domains, '\n', self.variables, '\n', self.unaryConstraints

    def determineCharsAtPos(self):
        charsAtPos = []
        for x in range(0, 3):
            chars = []
            for word in self.words:
                if word[x] not in chars:
                    chars.append(word[x])
            charsAtPos.append(sorted(chars))
        self.charsAtPos = charsAtPos

    def input(self):
        domain = set()
        for pos in self.charsAtPos:
            for char in pos:
                domain.add(char)
        vars = np.chararray((len(self.words[0]), len(self.words[0]), len(domain)))
        variables = vars[:, :, 1].tolist()
        domains = [[list(domain) for x in range(len(variables))] for y in range(len(variables))]
        unaryConstraints = set()
        for elem in range(len(variables)):
            for y in range(len(variables)):
                const = lambda c: (c in self.charsAtPos[elem]) | (c in self.charsAtPos[y])
                unaryConstraints.add(const)
        # map(list, zip(*l)) # list transposing
        # ternaryConstraints = set()
        # for i in xrange(len(variables)):
        #     row = lambda word1, word2, word3: "".join(list(word1, word2, word3)) in words
        # def ternaryConstraint(c1, c2, c3):
        #     if
        self.variables, self.domains, self.unaryConstraints = variables, domains, unaryConstraints  # , ternaryConstraint

    def isFollowing(self, char):
        out = set()
        for word in self.words:
            for cnr in range(len(word) - 1):
                if word[cnr] == char:
                    out.add(word[cnr + 1])
        print 'isFollowing:', out
        return out

    def isWord(self, chars):
        return "".join(chars[0], chars[1], chars[2]) in self.words

    def pairFromArray(self, coords):
        return self.domains[coords[0][0]][coords[0][1]], self.domains[coords[1][0]][coords[1][1]]

    def fittingCoord(self, coord):
        coords = [(x, y) for x in range(len(self.variables)) for y in range(len(self.variables))]
        for c in coords:
            if cityblock(coord, c) == 1:
                return c

    def arcConsistency(self):
        for row in self.domains:
            for domain in row:
                removing = []
                for char in domain:
                    remove = 0
                    for uCons in self.unaryConstraints:
                        if not uCons(char):
                            remove = 1
                    if remove:
                        removing.append(char)
                print 'removing:', removing
                for c in removing:
                    domain.remove(c)
        print self.domains
        todo = [[(0, 0), (0, 1)]]
        # coords1 = [(x, y) for x in range(len(self.variables)) for y in range(len(self.variables))]
        # coords2 = list(coord1)
        # coords = zip(coord1, coord2)
        print 'todo:', todo
        loopNR = 0
        while 1:
            loopNR += 1
            print 'loopNR:', loopNR
            coords = todo.pop()
            tuple = self.pairFromArray(coords)
            if self.arcReduce(tuple):
                if len(tuple[0]) == 0:
                    return 'No solution was found :('
                else:
                    todo.append([coords[0], self.fittingCoord(coords[0])])
                    print 'happening'
            print todo
            if len(todo) == 0:
                print 'stopped'
                break
        print self.domains

    def arcReduce(self, tuple):
        change = 0
        (xs, ys) = tuple
        print 'xs, ys', xs, ys
        remx = []
        valid = 0
        for x in xs:
            for y in ys:
                if y in self.isFollowing(x):
                    valid = 1
            if not valid:
                remx.append(x)
                change = 1
        print 'remx:', remx
        for x in remx:
            xs.remove(x)
        return change

aca = ACA('words.txt')
print aca.printStuff()
aca.arcConsistency()
