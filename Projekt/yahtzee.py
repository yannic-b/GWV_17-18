#!/Applications/anaconda2/bin/python2
# coding=utf-8

"""
Blatt 11: Yahtzee
Thomas Hofmann, Yannic Boysen

"""

import random
from collections import Counter


class Yahtzee:

    def __init__(self):
        self.game = []
        self.dices = Dices()
        self.score_sheet = ScoreSheet()


    def digitScore(self, digit):
        nr = 0
        for dice in self.dices:
            if dice == digit:
                nr += 1
        return nr * digit

    def checkAllOpt(self):
        # dictOfOpt holds all possible Options and their utility (points)
        dictOfOpt = {}
        dictOfOpt.update((self.checkDups()))
        print dictOfOpt

    # Checks for Dups and adds them with their Utility into a dict allDups.
    def checkDups(self):
        allDups = {}
        for key, value in self.dices.counts.iteritems():
            if value > 1 and self.score_sheet.upperScores.values()[key - 1] == None:
                valUtilitiy = key * value
                allDups[key] = valUtilitiy
        return allDups



class Dices:

    def __init__(self):
        self.dices = [random.randint(1, 6) for i in range(5)]
        self.update()

    def update(self):
        self.ones = self.dices.count(1)
        self.twos = self.dices.count(2)
        self.threes = self.dices.count(3)
        self.fours = self.dices.count(4)
        self.fives = self.dices.count(5)
        self.sixes = self.dices.count(6)
        self.counts = {}  # dict(Counter(self.dices))
        for x in range(1,7):
            self.counts[x] = self.dices.count(x)

    def diceToString(self):
        print self.dices

    def rollAgain(self, keep):
        self.dices = keep + [random.randint(1, 6) for i in range(5 - len(keep))]
        self.update()

    def countOf(self, digit):
        return self.counts[digit]

    # def hasStreet


class ScoreSheet:

    def __init__(self):
        self.upperScores = {
            1: None,
            2: None,
            3: None,
            4: None,
            5: None,
            6: None
        }

        self.lowerScores = {
            '3oak': None,
            '4oak': None,
            'fh': None,
            'sst': None,
            'lst': None,
            'y': None,
            'c': None
        }
        self.total = 0

    def calcTotal(self):
        for key, value in self.upperScores.iteritems():
            if value is not None:
                self.total += value
            if self.total > 62:
                self.total += 35
        for key, value in self.lowerScores.iteritems():
            if value is not None:
                self.total += value

    def addThrow(self, dices, section, row):
        if section == 'upper':
            self.upperScores[int(row)] = dices.countOf(int(row))
        else:
            return True








#d = Dices()
y = Yahtzee()
y.checkAllOpt()

#s = ScoreSheet()
#s.addThrow(d, 'upper', '5')
#s.calcTotal()
#print s.total
