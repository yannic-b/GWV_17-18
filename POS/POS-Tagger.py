#!/Applications/anaconda2/bin/python2
# -*- coding: iso-8859-1 -*-

"""
GWV-WS1718:
POS-Tager (Python 2.7)
by Thomas Hofmann and Yannic Boysen
"""

import io
import re
import copy
import random
import sys
reload(sys)
sys.setdefaultencoding('iso-8859-1')


class POS:

    def __init__(self, fileName):
        self.file = fileName
        # self.words = ['<start>'.encode('iso-8859-1')]
        self.words = []
        self.tags = []
        self.tCount = {}
        self.eCount = {}
        self.tProbs = {}
        self.eProbs = {}
        self.importWords()

    # import words and tags
    def importWords(self):
        comments = io.open(self.file, 'r', encoding='iso-8859-1')

        for line in comments:
            lastTag = '<start>.'
            if line != '\n':
                word, tag = re.split('\t', line.strip())
                self.addWord(tag, word, lastTag)
                lastTag = tag

        self.tProbs = self.calcProbs(self.tCount)
        self.eProbs = self.calcProbs(self.eCount)

        i = 0
        while i < 10:
            i += 1
            print self.words[i]
            # print self.eProbs[self.words[i].encode('iso-8859-1')]
            print self.tags[i]
            # print self.eProbs[self.tags[i].encode('iso-8859-1')]
            # print self.eProbs
            # print self.tProbs.keys()[i]

        # for word in comments:
        #     # self.words.append(word[:-1])
        #     if word in ['<end>'.encode('iso-8859-1'), '<start>'.encode('iso-8859-1')]:
        #         continue
        #     elif word == '\n':
        #         self.words.append('<end>'.encode('iso-8859-1'))
        #         self.words.append('<start>'.encode('iso-8859-1'))
        #     else:
        #         self.words.append(word.encode('iso-8859-1')[:-1])

    # create and add words and tags to specific arrays/ dics
    def addWord(self, tag, word, lastTag):
        if self.tags.count(tag.encode('iso-8859-1')) == 0:
            self.tags.append(tag.encode('iso-8859-1'))
        if self.words.count(word.encode('iso-8859-1')) == 0:
            self.words.append(word.encode('iso-8859-1'))

        if lastTag.encode('iso-8859-1') not in self.tCount:
            self.tCount[lastTag] = {tag.encode('iso-8859-1'): 1}
        elif tag.encode('iso-8859-1') not in self.tCount[lastTag]:
            self.tCount[lastTag][tag.encode('iso-8859-1')] = 1
        else:
            self.tCount[lastTag][tag.encode('iso-8859-1')] += 1

        if tag.encode('iso-8859-1') not in self.eCount:
            self.eCount[tag.encode('iso-8859-1')] = {word.encode('iso-8859-1'): 1}
        elif word.encode('iso-8859-1') not in self.eCount[tag.encode('iso-8859-1')]:
            self.eCount[tag.encode('iso-8859-1')][word.encode('iso-8859-1')] = 1
        else:
            self.eCount[tag.encode('iso-8859-1')][word.encode('iso-8859-1')] += 1

    # calculate Probabilities of tags depending of tags or words
    def calcProbs(self, counts):
        probabilities = copy.deepcopy(counts)
        for lastTag, tags in probabilities.items():
            count = 0
            for tagCount, tag in enumerate(self.tags):
                count += tagCount
            for tagCount, tag in enumerate(self.tags):
                probabilities[lastTag][tag] = tagCount / count
        return probabilities

    # tag a list of input words
    def tagList(self, toTag):
        output = ""
        lastTag = "<start>."
        for word in toTag:
            if word in self.words:
                lastTag = self.findTag(self, word)
                if lastTag is not None:
                    output += (word + '\t' + lastTag + '\n')
        return output

    # find tag for word
    def findTag(self, w, lt):
        tags = self.findTags(w)

        popular = (None, 0)
        for tag, count in tags:
            if count > popular[1]:
                popular = (tag, count)
        return popular[0]

    # find all tags for a word
    def findTags(self, w):
        tags = []
        for t, words in self.eCount.items():
            for tWord, count in words.items():
                if w == tWord:
                    tags.append((t, count))
        return tags

pos = POS("hdt-train.tags")

test1 = ["und", "von", "bei"]
print pos.tagList(test1)