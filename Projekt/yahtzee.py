#!/Applications/anaconda2/bin/python2
# coding=utf-8

"""
Blatt 11: Yahtzee
Thomas Hofmann, Yannic Boysen

"""

import random
# from collections import Counter


class Yahtzee:

    def __init__(self):
        self.game = []
        self.dices = Dices()
        self.score_sheet = ScoreSheet()
        self.dictOfOp = {}

    def simulateGame(self, verbosity=0):
        x = 0
        while x < 5:  # self.score_sheet.isFilled():
            self.dices = Dices()
            self.dices.diceToString()
            keep = random.sample(self.dices.dices, random.randint(1, 5))
            print keep
            self.dices.rollAgain(keep)
            self.dices.diceToString()
            keep = random.sample(self.dices.dices, random.randint(1, 5))
            print keep
            self.dices.rollAgain(keep)
            self.dices.diceToString()
            self.checkAllOpt()
            maxOpt = max(self.dictOfOp, key=self.dictOfOp.get)
            if maxOpt in self.score_sheet.upperScores.keys():
                self.score_sheet.addThrow(self.dices, "upper", maxOpt)
                
            x += 1


    def digitScore(self, digit):
        nr = 0
        for dice in self.dices:
            if dice == digit:
                nr += 1
        return nr * digit

    def checkAllOpt(self):
        # dictOfOpt holds all possible Options and their utility (points)
        self.dictOfOpt.update((self.checkDups()))
        self.dictOfOpt.update(self.checkFullHouse())
        self.dictOfOpt.update(self.checkYahtzee())
        self.dictOfOpt.update(self.checkThreeOfAKind())
        self.dictOfOpt.update(self.checkFourOfAKind())
        self.dictOfOpt.update(self.checkSmallStreet())
        self.dictOfOpt.update(self.checkLargeStreet())

    # Checks for Dups and adds them with their Utility into a dict allDups.
    def checkDups(self):
        allDups = {}
        for key, value in self.dices.counts.iteritems():
            if value > 1 and self.score_sheet.upperScores.values()[key - 1] is None:
                valUtilitiy = key * value
                allDups[key] = valUtilitiy
        return allDups

    def checkFullHouse(self):
        if self.score_sheet.lowerScores['fh'] is None:
            triple = False
            double = False
            for value in self.dices.counts.itervalues():
                if value == 2:
                    double = True
                elif value == 3:
                    triple = True
            if triple and double:
                return {'fh': 25}
            else:
                return {'fh': 0}
        else:
            return {'fh': 0}

    def checkYahtzee(self):
        if self.score_sheet.lowerScores['y'] is None:
            firstNumber = self.dices.dices[0]
            counter = 0
            for number in self.dices.dices:
                if number == firstNumber:
                    counter += 1
            if counter == 5:
                return {'y': 50}
            else:
                return {'y': 0}
        else:
            return {'y': 0}

    def checkThreeOfAKind(self):
        if self.score_sheet.lowerScores['3oak'] is None:
            for value in self.dices.counts.itervalues():
                if value > 2:
                    return {"3oak" : sum(self.dices.dices)}
            return {"3oak": 0}
        else:
            return {"3oak": 0}

    def checkFourOfAKind(self):
        if self.score_sheet.lowerScores['4oak'] is None:
            for value in self.dices.counts.itervalues():
                if value > 3:
                    return {"4oak" : sum(self.dices.dices)}
            return {"4oak": 0}
        else:
            return {"4oak": 0}

    def checkSmallStreet(self):
        if self.score_sheet.lowerScores['sst'] is None:
            counters = []
            counter = 0
            for x in range(1,5):
                if x in self.dices.dices:
                    counter += 1
            counters.append(counter)
            counter = 0
            for x in range(2,6):
                if x in self.dices.dices:
                    counter += 1
            counters.append(counter)
            counter = 0
            for x in range(3,7):
                if x in self.dices.dices:
                    counter += 1
            counters.append(counter)
            if x > 4 in counters:
                return {"sst": 30}
            else:
                return {"sst": 0}
        else:
            return {"sst": 0}

    def checkLargeStreet(self):
        if self.score_sheet.lowerScores['lst'] is None:
            counters = []
            counter = 0
            for x in range(1,6):
                if x in self.dices.dices:
                    counter += 1
            counters.append(counter)
            counter = 0
            for x in range(2,7):
                if x in self.dices.dices:
                    counter += 1
            counters.append(counter)
            if x > 5 in counters:
                return {"lst": 30}
            else:
                return {"lst": 0}
        else:
            return {"lst": 0}


class Dices:

    def __init__(self):
        self.dices = sorted([random.randint(1, 6) for i in range(5)])
        self.update()

    def update(self):
        self.ones = self.dices.count(1)
        self.twos = self.dices.count(2)
        self.threes = self.dices.count(3)
        self.fours = self.dices.count(4)
        self.fives = self.dices.count(5)
        self.sixes = self.dices.count(6)
        self.counts = {}  # dict(Counter(self.dices))
        for x in range(1, 7):
            self.counts[x] = self.dices.count(x)

    def diceToString(self):
        print self.dices

    def rollAgain(self, keep):
        # remove = [d for d in self.dices if d not in keep]
        for d in keep:
            if d not in self.dices:
                keep.remove(d)
        self.dices = sorted(keep + [random.randint(1, 6) for i in range(5 - len(keep))])
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

        self.total_all = 0
        self.total_upper = 0
        self.total_lower = 0
        self.bonus = False

    def isFilled(self):
        board = [self.upperScores.values() + self.lowerScores.values()]
        return all(v is not None for v in board)

    def calcTotal(self):
        for key, value in self.upperScores.iteritems():
            if value is not None:
                self.total_upper += value
            if self.total_upper > 62:
                self.total_upper += 35
                self.bonus = True
        for key, value in self.lowerScores.iteritems():
            if value is not None:
                self.total_lower += value
        self.total_all = self.total_upper + self.total_lower

    def addThrow(self, dices, section, row):
        if section == 'upper':
            self.upperScores[int(row)] = dices.countOf(int(row))
        else:
            return True


y = Yahtzee()
# print y.dices.counts
# y.checkAllOpt()

# s = ScoreSheet()
# s.addThrow(d, 'upper', '5')
# s.calcTotal()
# print s.total

y.simulateGame()
