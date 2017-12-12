#!/Applications/anaconda2/bin/python2
# coding=utf-8

"""
GWV-WS1718:
LabyrinthSearch (Python 2.7)
by Thomas Hofmann and Yannic Boysen
"""

import random
# import pickle
# def saveObj(obj, name):
#     with open(name + '.pkl', 'wb') as f:
#         pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
#
#
# def loadObj(name):
#     with open(name + '.pkl', 'rb') as f:
#         return pickle.load(f)


# Markov Generator
class MarkovGenerator:

    def __init__(self, fileName):
        self.file = fileName
        self.words = []
        self.wordMap = {}
        self.importWords()
        self.mapWords()

    # TODO preprocess word list
    # TODO save sentence start and end

    def importWords(self):
        comments = open(self.file, 'r')
        for word in comments:
            self.words.append(word[:-1])

    # Saving and loading the dictionaries is not faster than just calculating them each time
    # def firstImport(self):
    #     comments = open(self.file, 'r')
    #     for word in comments:
    #         self.words.append(word[:-1])
    #     saveObj(self.words, 'words')
    #
    #     self.mapWords()
    #     saveObj(self.wordMap, 'wordMap')
    #
    # def loadState(self):
    #     self.words = loadObj('words')
    #     self.wordMap = loadObj('wordMap')

    def calcProbs(self, wordList):
        numWords = len(wordList)
        counter = {}
        for word in wordList:
            if word in counter:
                counter[word] += 1
            else:
                counter[word] = 1
        for word in counter.keys():
            counter[word] /= float(numWords)
        return counter

    def randomWord(self, wordCount):
        randomValue = random.random()
        cumulative = 0.0
        chosenWord = ""
        for word in wordCount:
            probability = wordCount[word]
            if probability > cumulative:
                cumulative = probability
                chosenWord = word
        return chosenWord

    def mapWords(self):
        pair = (self.words[0], self.words[1])
        for word in self.words:
            if pair in self.wordMap:
                self.wordMap[pair].append(word)
            else:
                self.wordMap[pair] = [word]
            pair = (pair[1], word)
        for word in self.wordMap.keys():
            probability = self.calcProbs(self.wordMap[word])
            self.wordMap[word] = probability

    def newChain(self, length):
        startWord = random.choice(self.words)
        pair = (startWord, self.words[self.words.index(startWord) + 1])
        print pair[0], pair[1],
        for i in range(length):
            word = self.randomWord(self.wordMap[pair])
            print word,
            if word.endswith('.') | word.endswith('!'):
                print "\n"
                break
            pair = (pair[1], word)


mg = MarkovGenerator('comments.txt')
# mg.firstImport() # ONLY RUN ON FIRST PROGRAM START!
# mg.loadState()
# print mg.words[:10]
# print {k: mg.wordMap[k] for k in mg.wordMap.keys()[:10]}
# print mg.wordMap.keys()[:10]

for i in range(10):
    mg.newChain(25)
