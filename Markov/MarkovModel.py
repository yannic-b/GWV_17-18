import random

# import data
text_file = 'ggcc-one-word-per-line.txt'
f = open (text_file, 'r', encoding='utf-8')
words = f.readlines()
f.close()
words = [word.strip() for word in words]

# operators is number of words observed
def createProbabilityDict(words, operator):
    next_occurence_dict = dict()
    for i in range (0, len(words) - 1):
        if (words[i] not in next_occurence_dict):
            next_occurence_dict[words[i]] = []

        for o in range (1, operator):
            next_occurence_dict[words[i]].append(words[i + o])
    return next_occurence_dict


# generates random sequence with given length and start position
def generateRandomSequence(length, startPosition, words):
    startWord = words[startPosition]
    wordSequence = startWord + ' '

    for i in range (0, length):
        nextWord = random.choice(probabilityDictionary[startWord]) + ' '
        wordSequence += nextWord

    return wordSequence


#for testing purposes
probabilityDictionary = createProbabilityDict(words, 3)
print(generateRandomSequence(16, 1, words))

