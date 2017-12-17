import random

# import data
text_file = 'ggcc-one-word-per-line.txt'
f = open (text_file, 'r')
wordset = f.readlines()
f.close()
wordset = [word.strip() for word in wordset]

# operators is number of words observed
# operator = 1 should be a bigram
def createProbabilityDict(words, operator):
    next_occurence_dict = dict()
    for i in range (0, len(words) - operator):
        if (words[i] not in next_occurence_dict):
            next_occurence_dict[words[i]] = []

        for o in range (1, operator):
            next_occurence_dict[words[i]].append(words[i + o])
    return next_occurence_dict


# generates random sequence with given length and start position
def generateRandomSequence(length, startPosition, wordset):
    startWord = wordset[startPosition]
    sequence = startWord + ' '

    for i in range (0, length):
        nextWord = random.choice(dictionary[startWord]) + ' '
        sequence += nextWord

    return sequence


#for testing purposes
dictionary = createProbabilityDict(wordset, 6)
print(generateRandomSequence(25, 500, wordset))

