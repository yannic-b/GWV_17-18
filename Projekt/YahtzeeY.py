# -*- coding: iso-8859-1 -*-

"""
Blatt 11: Yahtzee
Thomas Hofmann, Yannic Boysen

Version 1.0 (26.01.18, 18:41):
# Diese Version kann ein komplettes Kniffel Spiel simulieren
# Das Programm überlässt alle Entscheidungen dem Zufall.

"""

import random

# used to turn on and off detailed output for each game
verbose = 0
if verbose:
    def verbosePrint(*args):
        # Print each argument separately so caller doesn't need to
        # stuff everything to be printed into a single string
        for arg in args:
            print arg,
        print
else:
    def verbosePrint(*args):
        None


# Class that represents a set of 5 dice
class Dice:

    def __init__(self):
        self.dictOfOpt = {}
        self.counts = {}
        self.dice = []
        self.possibleRows = []
        self.roll()
        self.update()

    # function to update all fields after a dice roll
    def update(self):
        # self.ones = self.dice.count(1)
        # self.twos = self.dice.count(2)
        # self.threes = self.dice.count(3)
        # self.fours = self.dice.count(4)
        # self.fives = self.dice.count(5)
        # self.sixes = self.dice.count(6)
        # dict(Counter(self.dice))
        for x in range(1, 7):
            self.counts[str(x)] = self.dice.count(x)
        self.checkAll()
        self.possibleRows = [str(x) for x in range(1, 7)] + ['ch']
        for key in self.dictOfOpt.keys():
            if self.dictOfOpt[key] is True:
                self.possibleRows.append(key)

    # initialize set of dice
    def roll(self):
        self.dice = sorted([random.randint(1, 6) for _ in range(5)])
        self.update()

    # second or third roll
    def rollAgain(self, keep):
        # remove = [d for d in self.dice if d not in keep]
        for d in keep:
            if d not in self.dice:
                keep.remove(d)
        self.dice = sorted(keep + [random.randint(1, 6) for _ in range(5 - len(keep))])
        self.update()

    def printOut(self):
        verbosePrint(self.dice)

    def countOf(self, digit):
        return self.counts[digit]

    # all following functions are there to check presence of the different score requirements
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
        for i in range(1, 4):
            for x in range(i, i + 4):
                if x in self.dice:
                    counter += 1
            counters.append(counter)
            counter = 0
        return x > 4 in counters

    def hasLargeStraight(self):
        counters = []
        counter = 0
        for x in range(1, 6):
            if x in self.dice:
                counter += 1
        counters.append(counter)
        counter = 0
        for x in range(2, 7):
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
        verbosePrint(self.sheet, "-> Bonus:", "Yes." if self.bonusGiven else "No.")

    # update total after score is added
    def update(self):
        self.total = 0
        upperKeys = [key for key in self.sheet.keys() if len(key) == 1]
        if not self.bonusGiven and sum(self.sheet[x] for x in upperKeys if self.sheet[x] is not None) >= 63:
            self.total += 35
            self.bonusGiven = True
        self.total += sum(x for x in self.sheet.values() if x is not None)
        self.openRows = [key for key in self.sheet.keys() if self.sheet[key] is None]

    # add score in specific row
    def addScore(self, dice, row):
        score = Logic.calcUtility(dice, row)
        # verboseprint score
        self.sheet[row] = score
        # self.openRows.remove(row)
        self.update()


# a game instance
class Game:

    def __init__(self):
        self.dice = Dice()
        self.score = Score()
        self.rollsLeft = 39

    def play(self, untilRound=13):
        verbosePrint("STARTING GAME...")
        for _ in range(untilRound):
            self.playRound()
        print "\nFINAL SCORE:", self.score.total
        print self.score.sheet, self.score.bonusGiven

    def playRound(self):
        verbosePrint("\nNext round: ")
        verbosePrint("Rolling dice...")
        self.rollsLeft -= 1  # = 3
        self.dice.roll()
        self.dice.printOut()
        while (self.rollsLeft % 3) != 0:
            keepers = Logic.bestKeepers(self)
            verbosePrint("Keeping:", keepers)
            verbosePrint("PR:", self.dice.possibleRows)
            self.dice.rollAgain(keepers)
            verbosePrint("Rolling remaining dice...")
            self.dice.printOut()
            self.rollsLeft -= 1
        verbosePrint("PR:", self.dice.possibleRows)  # DEBUGGING
        optimalRow = Logic.findOptimalRow(self)
        verbosePrint("Adding Score in", optimalRow)
        self.score.addScore(self.dice, optimalRow)
        verbosePrint("Score Sheet State: ")
        self.score.printOut()


# helper class to make decisions during game time
class Logic:

    fixedScore = {
        'fh': 25,
        'ss': 30,
        'ls': 40,
        'ya': 50,
    }

    # return best dice to keep between rolls for current game state
    @staticmethod
    def bestKeepers(game):
        keep = []
        optimalRow = Logic.findOptimalRow(game)
        verbosePrint(optimalRow)
        if optimalRow in ['ya', 'ch', '3k', '4k', 'fh']:
            keep = game.dice.dice
        elif optimalRow == 'ss':
            if all(x in sorted(game.dice.dice) for x in [1, 2, 3, 4]): keep = [1, 2, 3, 4]
            if all(x in sorted(game.dice.dice) for x in [2, 3, 4, 5]): keep = [2, 3, 4, 5]
            if all(x in sorted(game.dice.dice) for x in [3, 4, 5, 6]): keep = [3, 4, 5, 6]
        elif optimalRow == 'ls':
            if sorted(game.dice.dice) == [1, 2, 3, 4, 5]: keep = [1, 2, 3, 4, 5]
            if sorted(game.dice.dice) == [2, 3, 4, 5, 6]: keep = [2, 3, 4, 5, 6]
        elif int(optimalRow) in range(1, 7):
            countOfOR = game.dice.countOf(optimalRow)
            while countOfOR > 0:
                keep.append(int(optimalRow))
                countOfOR -= 1
        return keep
        # return random.sample(game.dice.dice, random.randint(1, 5))

    # find the optimal row to score in
    @staticmethod
    def findOptimalRow(game):
        choices = []
        openRows = game.score.openRows
        possibleRows = game.dice.possibleRows
        for key in game.score.sheet.keys():
            if (key in openRows) and (key in possibleRows):
                choices.append(key)
        choices.sort(key=(lambda x: Logic.expectedUtility(game, x)), reverse=True)
        if len(choices) > 0:
            return choices[0]
        else:
            return openRows[0]

    # calculating the expected utility (at this point only for the upper section
    @staticmethod
    def expectedUtility(game, row):
        rollsLeft = game.rollsLeft % 3
        if len(row) == 1:
            countOfRow = game.dice.countOf(row)
            diceLeft = 5 - countOfRow
            eU = Logic.calcUtility(game.dice, row)
            for x in range(diceLeft + 1):
                probability = Logic.calcDigitProbability(diceLeft, rollsLeft, x)
                normalUtility = int(row) * probability
                bonusUtility = ((x + countOfRow) - 3) * 35 * ((float(row)*3) / 63) * probability
                # print bonusUtility
                eU += (normalUtility + bonusUtility)
            return eU
        # elif row == "ya":
        #     countOfRow = max(game.dice.counts.values())
        #     diceLeft = 5 - countOfRow
        #     return 50 * Logic.calcDigitProbability(diceLeft, rollsLeft, diceLeft)
        else:
            return Logic.calcUtility(game.dice, row)

    @staticmethod
    def calcProbability(dice, row):
        return

    # Magic function to calculate the probability to get exactly x specific digits with y dice and z rolls left.
    @staticmethod
    def calcDigitProbability(diceLeft, rollsLeft, digitsLeftToGet=1):
        # print "in"
        diceLeft, rollsLeft = float(diceLeft), float(rollsLeft)
        if rollsLeft == 0:
            return 0
        elif digitsLeftToGet == 0:
            return 1
        else:
            P = 0
            for x in range(digitsLeftToGet+1):
                # print x
                tempP = diceLeft * (1.0/6.0)**(digitsLeftToGet - x) * (5.0/6.0)**(diceLeft-(digitsLeftToGet-x))
                # print P
                if x > 0:
                    # print "if"
                    tempP *= Logic.calcDigitProbability(diceLeft-(digitsLeftToGet-x), rollsLeft - 1, x)
                P += tempP
                # print P
            return 1 if P > 1 else P

    # calculating the utility for the different score rows (=score)
    @staticmethod
    def calcUtility(dice, row):
        if row not in dice.possibleRows:
            score = 0
        elif len(row) == 1:
            score = dice.countOf(row) * int(row)
        elif row in ['3k', '4k', 'ch']:
            score = sum(dice.dice)
        else:
            score = Logic.fixedScore[row]
        return score


# Run the game a specific amount of times and calculate stats
totals = []
runs = 133
for _ in range(runs):
    gameOfYahtzee = Game()
    gameOfYahtzee.play()
    totals.append(gameOfYahtzee.score.total)
print "\nPlayed", runs, "games, with following results:"
print "Highest:", max(totals), "| Lowest:",min(totals), "| Average Score:", sum(totals) / len(totals)


### TESTING ###
# for i in range(5):
#     print Logic.calcDigitProbability(3, 2, i), "\n"
#
# print Logic.calcDigitProbability(3, 1, 1)

# g = Game()
# g.dice = Dice()
# g.rollsLeft = 2
# g.dice.printOut()
# print Logic.expectedUtility(g, "3")
