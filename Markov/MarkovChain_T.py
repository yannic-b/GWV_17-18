import random

# import data
text_file = 'ggcc-one-word-per-line.txt'
f = open(text_file, 'r')
wordset = f.readlines()
f.close()
wordset = [word.strip() for word in wordset]
wordset = [word.strip('.') for word in wordset]
wordset = [word.strip(',') for word in wordset]
wordset = [word.strip('!') for word in wordset]


# operators is number of words observed
# operator = 1 should be a bigram
def createProbabilityDict(words, operator):
    next_occurrence_dict = dict()
    for i in range(0, len(words) - operator):
        if words[i] not in next_occurrence_dict:
            next_occurrence_dict[words[i]] = []

        for o in range(1, operator):
            next_occurrence_dict[words[i]].append(words[i + o])
    return next_occurrence_dict


# generates random sequence with given length and start position
def generateRandomSequence(length, startPosition, wordset):
    startWord = wordset[startPosition - 1]
    sequence = startWord + ' '

    for i in range(0, length):
        nextWord = random.choice(dictionary[startWord]) + ' '
        sequence += nextWord

    return sequence


<<<<<<< HEAD
#for testing purposes
dictionary = createProbabilityDict(wordset, 10)
print(generateRandomSequence(25, 1, wordset))

=======
# for testing purposes
dictionary = createProbabilityDict(wordset, 6)
for i in range(20):
    print(generateRandomSequence(25, 500, wordset))
>>>>>>> origin/master
