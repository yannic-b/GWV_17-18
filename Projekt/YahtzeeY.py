# -*- coding: iso-8859-1 -*-

"""
Blatt 11: Yahtzee
Thomas Hofmann, Yannic Boysen

Version 1.0 (26.01.18, 18:41):
# Diese Version kann ein komplettes Kniffel Spiel simulieren
# Das Programm überlässt alle Entscheidungen dem Zufall.

"""


import random


# Class that represents a set of 5 dice
class Dice:

    def __init__(self):
        self.dictOfOpt = {}
        self.counts = {}
        self.dice = []
        self.possibleRows = []
        self.roll()
        self.update()

    def update(self):
        # self.ones = self.dice.count(1)
        # self.twos = self.dice.count(2)
        # self.threes = self.dice.count(3)
        # self.fours = self.dice.count(4)
        # self.fives = self.dice.count(5)
        # self.sixes = self.dice.count(6)
        # dict(Counter(self.dice))
        for x in range(1, 7):
            self.counts[x] = self.dice.count(x)
        self.checkAll()
        self.possibleRows = [str(x) for x in range(1, 7)] + ['ch']
        for key in self.dictOfOpt.keys():
            if self.dictOfOpt[key] is True:
                self.possibleRows.append(key)

    def roll(self):
        self.dice = sorted([random.randint(1, 6) for i in range(5)])
        self.update()

    def rollAgain(self, keep):
        # remove = [d for d in self.dice if d not in keep]
        for d in keep:
            if d not in self.dice:
                keep.remove(d)
        self.dice = sorted(keep + [random.randint(1, 6) for _ in range(5 - len(keep))])
        self.update()

    def printOut(self):
        print self.dice

    def countOf(self, digit):
        return self.counts[digit]

    def checkAll(self):
        # dictOfOpt holds all possible Options and their utility (points)
        self.dictOfOpt['3k'] = self.hasThreeOfAKind()
        self.dictOfOpt['4k'] = self.hasFourOfAKind()
        self.dictOfOpt['fh'] = self.hasFullHouse()
        self.dictOfOpt['ss'] = self.hasSmallStraight()
        self.dictOfOpt['ls'] = self.hasLargeStraight()
        self.dictOfOpt['ya'] = self.hasYahtzee()

    def hasThreeOfAKind(self):
        for value in self.counts.itervalues():
            if value > 2: return True
        return False

    def hasFourOfAKind(self):
        for value in self.counts.itervalues():
            if value > 3: return True
        return False

    def hasFullHouse(self):
        triple, double = False, False
        for value in self.counts.itervalues():
            if value == 2:
                double = True
            elif value == 3:
                triple = True
        return triple and double

    def hasSmallStraight(self):
        counters = []
        counter = 0
        for x in range(1, 4):
            for x in range(x, x+4):
                if x in self.dice:
                    counter += 1
            counters.append(counter)
            counter = 0
        return x > 4 in counters

    def hasLargeStraight(self):
        counters = []
        counter = 0
        for x in range(1,6):
            if x in self.dice:
                counter += 1
        counters.append(counter)
        counter = 0
        for x in range(2,7):
            if x in self.dice:
                counter += 1
        counters.append(counter)
        return x > 5 in counters

    def hasYahtzee(self):
        return len(set(self.dice)) == 1


# class representing the Score Sheet
class Score:

    def __init__(self):
        self.sheet = {
            '1': None,
            '2': None,
            '3': None,
            '4': None,
            '5': None,
            '6': None,
            '3k': None,
            '4k': None,
            'fh': None,
            'ss': None,
            'ls': None,
            'ya': None,
            'ch': None
        }
        self.bonusGiven = False
        self.openRows = []
        self.total = 0
        self.update()

    def roomOnSheet(self):
        self.update()
        return not all(self.sheet.values())

    def printOut(self):
        print self.sheet

    def update(self):
        if not self.bonusGiven and sum(self.sheet[x] for x in self.sheet.keys() if x in [str(range(1, 7))]) >= 63:
            self.total += 35
            self.bonusGiven = True
        self.total = sum(x for x in self.sheet.values() if x is not None)
        self.openRows = [key for key in self.sheet.keys() if self.sheet[key] is None]

    def addScore(self, dice, row):
        score = Logic.calcUtility(dice, row)
        print score
        self.sheet[row] = score
        self.update()


# a game instance
class Game:

    def __init__(self, verbose=0):
        self.dice = Dice()
        self.score = Score()
        self.vb = verbose
        self.rollsLeft = 39

    def play(self, untilRound=13):
        print "STARTING GAME..."
        for _ in range(untilRound):
            self.playRound()
        print "\nFINAL SCORE:", self.score.total

    def playRound(self):
        print "\nNext round: "
        print "Rolling dice..."
        self.rollsLeft -= 1  # = 3
        self.dice.roll()
        self.dice.printOut()
        while (self.rollsLeft % 3) != 0:
            keepers = Logic.bestKeepers(self)
            print "Keeping:", keepers
            self.dice.rollAgain(keepers)
            print "Rolling remaining dice..."
            self.dice.printOut()
            self.rollsLeft -= 1
        print "PR:", self.dice.possibleRows  # DEBUGGING
        optimalRow = Logic.findOptimalRow(self)
        print "Adding Score in", optimalRow
        self.score.addScore(self.dice, optimalRow)
        print "Score Sheet State: "
        self.score.printOut()


# helper class to make decisions during game time
class Logic:

    fixedScore = {
        'fh': 25,
        'ss': 30,
        'ls': 40,
        'ya': 50,
    }

    @staticmethod
    def bestKeepers(game):
        return random.sample(game.dice.dice, random.randint(1, 5))

    @staticmethod
    def findOptimalRow(game):
        choices = []
        openRows = game.score.openRows
        possibleRows = game.dice.possibleRows
        for key in game.score.sheet.keys():
            if (key in openRows) and (key in possibleRows):
                choices.append(key)
        choices.sort(key=(lambda x: Logic.calcUtility(game.dice, x)), reverse=True)
        if len(choices) > 0:
            return choices[0]
        else:
            return openRows[0]

    @staticmethod
    def calcProbability(game):
        return

    @staticmethod
    def calcUtility(dice, row):
        if row not in dice.possibleRows:
            score = 0
        elif len(row) == 1:
            score = dice.countOf(int(row)) * int(row)
        elif row in ['3k', '4k', 'ch']:
            score = sum(dice.dice)
        else:
            score = Logic.fixedScore[row]
        return score


gameOfYahtzee = Game()
gameOfYahtzee.play()
