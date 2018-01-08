#!/Applications/anaconda2/bin/python2
# -*- coding: iso-8859-1 -*-

"""
GWV-WS1718:
LabyrinthSearch (Python 2.7)
by Thomas Hofmann and Yannic Boysen
"""

import io
import sys
import codecs
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
        self.words = ['<start>'.encode('iso-8859-1')]
        self.wordMap = {}
        self.importWords()
        self.mapWords()

    # imports words from file and adds start and end tokens
    def importWords(self):
        comments = io.open(self.file, 'r', encoding='iso-8859-1')
        for word in comments:
            # self.words.append(word[:-1])
            if word in ['<end>'.encode('iso-8859-1'), '<start>'.encode('iso-8859-1')]:
                continue
            elif word == '\n':
                self.words.append('<end>'.encode('iso-8859-1'))
                self.words.append('<start>'.encode('iso-8859-1'))
            else:
                self.words.append(word.encode('iso-8859-1')[:-1])
                # if word[0] in ['.', '!', '?']:
                #     self.words.append('<end>')
                #     self.words.append('<start>')

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

    # calculates probabilities for each word based on number of occurrences
    def calcProbs(self, wordList, pair):
        numWords = len(wordList)
        counter = 0
        for word in wordList:
            if word == pair:
                counter += 1
        #     if word in counter:
        #         counter[word] += 1
        #     else:
        #         counter[word] = 1
        # for word in counter.keys():
        #     counter[word] /= float(numWords)
        return counter

    # chooses random element from probability distribution
    def randomWord(self, wordProb):
        sumOfProbs = 0.0
        chosenWord = ""
        for word in wordProb:
            probability = wordProb[word]
            if probability > sumOfProbs:
                sumOfProbs += probability
                chosenWord = word
        return chosenWord

    # maps probabilities to all pairs of words
    def mapWords(self):
        pair = (self.words[0], self.words[1])
        for word in self.words:
            if pair in self.wordMap:
                self.wordMap[pair].append(word)
            else:
                self.wordMap[pair] = [word]
            pair = (pair[1], word)
        for word in self.wordMap.keys():
            probability = self.calcProbs(self.wordMap, word)
            self.wordMap[word] = probability

    # creates a new Markov Chain comment, starting with a random word
    def newChain(self, length):
        random.seed()
        startWordIndex = random.choice(list(enumerate(self.words)))[0]
        while self.words[startWordIndex - 1] != '<start>':
            # print self.words[startWordIndex - 1]
            startWordIndex -= 1
        startWord = self.words[startWordIndex]
        pair = (startWord, self.words[self.words.index(startWord) + 1])
        print pair[0], pair[1],
        for i in range(length):
            word = self.randomWord(self.wordMap[pair])
            if word.startswith('<end>'):  # ('.') | word.endswith('!'):
                print "\n"
                break
            print word,
            pair = (pair[1], word)


mg = MarkovGenerator('comments.txt')
# mg.firstImport() # ONLY RUN ON FIRST PROGRAM START!
# mg.loadState()
# print mg.words[:100]
# for word in mg.words[:100]:
#     print unicode(word, 'unicode-escape')
# print {k: mg.wordMap[k] for k in mg.wordMap.keys()[:10]}
# print mg.wordMap.keys()[:10]

for i in range(10):
    mg.newChain(25)
