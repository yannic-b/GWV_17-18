import re
import copy
import sys
import argparse

tag_list = []
words_list = []
emission_count = {}
transition_count = {}


#read tag file
tags_file = 'hdt-tagged/hdt-10001-12000-test.tags'
file = open(tags_file, 'r')
tags = file.readlines()
file.close()

#creates the Hidden Markov Model
def createHMM():
    create_counts(tags)
    createProbs(emission_count)
    createProbs(transition_count)

#tags words or sentences
def tag_words(response):
    #first create the Markov Model
    createHMM()
    full_sentence = ""
    #War fuer Kommandozeilen Input gedacht
    #response = raw_input("Geben sie einen Satz ein:")
    #Split sentence into words
    splitted_response = response.split()
    if splitted_response:
        for words in splitted_response:
             full_sentence += (words + "/" + get_most_possible_tag(words) + " ")
    print full_sentence

#help function to get all possible tags for a word
def get_possible_tags(word):
    all_tags = []
    #iterate through the get the possible tags and counts for a word
    for tag, words in emission_count.items():
        for tagged, count in words.items():
            if word == tagged:
                all_tags.append((tag, count))
    return all_tags

#get simply the most used tag for a word
def get_most_possible_tag(word):
    all_possible_tags = get_possible_tags(word)
    tag_most_used= ('', 0)
    for tag, count in all_possible_tags:
        if count > tag_most_used[1]:
            tag_most_used = (tag, count)
    return tag_most_used[0]

# create emission and transition count
def create_counts(tags):
    #because first sentence does not have previous tag
    lasttag = '$.'
    for words in tags:
        #split into word and tag
        if words != '\n':
            word, tag = re.split('\t' , words.strip())

            if words_list.count(word) == 0:
                words_list.append(word)
            if tag_list.count(tag) == 0:
                tag_list.append(tag)

            if lasttag not in transition_count:
                transition_count[lasttag] = {tag : 1}
            elif tag not in transition_count[lasttag]:
                transition_count[lasttag][tag] = 1
            else:
                transition_count[lasttag][tag] += 1

            if tag not in emission_count:
                emission_count[tag] = {word : 1}
            elif word not in emission_count:
                emission_count[tag][word] = 1
            else:
                emission_count[tag][word] += 1

            lasttag = tag

# compute probabilities for the emission and transition
def createProbs(count):
    probability = copy.deepcopy(count)
    for lasttag, tags in count.items():
        counter = 0
        # counting the tags
        for tag, tagcount in tags.items():
            counter += tagcount
        for tag, tagcount in tags.items():
            probability[lasttag][tag] = tagcount / counter
            #print probability
    return probability

#testing stuff
#createHMM()
tag_words("Hallo Der Hund")










