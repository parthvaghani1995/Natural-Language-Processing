# -*- coding: UTF-8 -*-
#!/usr/bin/env python2
from __future__ import division
import sys
import string
from collections import defaultdict


stopWords = set()
numberOfPositive = 0
numberOfNegative = 0
numberOfFake = 0
numberOfTrue = 0
currentTF = -1
currentPN = -1
countDictionary = {}
totalPropertyValue = 0
finalCountDictionary = {}
vocabularyLength = 0
totalNumberOfPos = 0
totalNumberOfNeg = 0
totalNumberOfTrue = 0
totalNumberOfFake = 0
countedProbability = 0.0
stringToPrint = ""
properties = ['pos','neg','true','fake']

# getting a list of stop words
def returnStopWords():
    with open('sw.txt') as f:
        lines = f.readlines()
        for line in lines:
            stopWords.add(line.strip('\n'))
    print(len(stopWords))

def main():
    returnStopWords()
    global numberOfTrue, numberOfFake, numberOfNegative, numberOfPositive, currentPN, currentTF, countDictionary, totalPropertyValue, finalCountDictionary,totalNumberOfTrue, totalNumberOfFake, totalNumberOfNeg, totalNumberOfPos, stringToPrint, countedProbability
    with open(sys.argv[1], 'r') as my_file:
        for line in my_file:
            getLineDetails = line.split(' ',3)
            #number of true and false
            if getLineDetails[1] == "True":
                numberOfTrue = numberOfTrue + 1
                currentTF = 'true'
            else:
                numberOfFake = numberOfFake + 1
                currentTF = 'fake'
            #number of postive and negative
            if getLineDetails[2] == "Pos":
                numberOfPositive = numberOfPositive + 1
                currentPN = 'pos'
            else:
                numberOfNegative = numberOfNegative + 1
                currentPN = 'neg'

            sentence = getLineDetails[3].strip('\n')
            sentence = sentence.lower()
            sentence = sentence.translate(None, string.punctuation)
            sentence = sentence.split(" ")
            currentDictionary = {}
            for word in sentence:
                if ((word not in stopWords) and (word != '')):
                    if word in currentDictionary:
                        currentDictionary[word] = currentDictionary[word] + 1
                    else:
                        currentDictionary[word] = 1

            #print(currentDictionary)
            #print(getLineDetails)
            #Count number of parameters for each word
            if currentTF == 'true':
                for word in currentDictionary:
                    if currentTF not in countDictionary.get(word, {}):
                        countDictionary.setdefault(word, {})['true'] = 0

                    if word in countDictionary:
                        countDictionary[word][currentTF] = int(countDictionary[word][currentTF]) + int(currentDictionary[word])
                    else:
                        countDictionary[word][currentTF] = int(currentDictionary[word])
            else:
                #print("herer")
                for word in currentDictionary:
                    if currentTF not in countDictionary.get(word, {}):
                        countDictionary.setdefault(word, {})['fake'] = 0
                    if word in countDictionary:
                        countDictionary[word][currentTF] = int(countDictionary[word][currentTF]) + int(currentDictionary[word])
                    else:
                        countDictionary[word][currentTF] = int(currentDictionary[word])

            if currentPN == 'pos':
                for word in currentDictionary:
                    if currentPN not in countDictionary.get(word, {}):
                        countDictionary.setdefault(word, {})['pos'] = 0

                    if word in countDictionary:
                        countDictionary[word][currentPN] = int(countDictionary[word][currentPN]) + int(currentDictionary[word])
                    else:
                        countDictionary[word][currentPN] = int(currentDictionary[word])
            else:
                for word in currentDictionary:
                    if currentPN not in countDictionary.get(word, {}):
                        countDictionary.setdefault(word, {})['neg'] = 0

                    if word in countDictionary:
                        countDictionary[word][currentPN] = int(countDictionary[word][currentPN]) + int(currentDictionary[word])
                    else:
                        countDictionary[word][currentPN] = int(currentDictionary[word])

        finalCountDictionary = countDictionary.copy()
        for word in countDictionary:
            #print(word)
            for property in countDictionary[word]:
                totalPropertyValue = totalPropertyValue + countDictionary[word][property]
            if ((totalPropertyValue <= 2) or (word.isspace()) or (word.isdigit())):
                del finalCountDictionary[word]
            totalPropertyValue = 0

        vocabularyLength = len(finalCountDictionary)

        #Count total number of positive, negative, fake and true
        for word in finalCountDictionary:
            for property in finalCountDictionary[word]:
                if property == 'pos':
                    totalNumberOfPos = totalNumberOfPos + finalCountDictionary[word][property]
                if property == 'neg':
                    totalNumberOfNeg = totalNumberOfNeg + finalCountDictionary[word][property]
                if property == 'fake':
                    totalNumberOfFake = totalNumberOfFake + finalCountDictionary[word][property]
                if property == 'true':
                    totalNumberOfTrue = totalNumberOfTrue + finalCountDictionary[word][property]

        #open file

        with open("nbmodel.txt","w") as f:

            #prior probability calculation

            priorPos = ((numberOfPositive)/(numberOfPositive + numberOfNegative))
            priorNeg = ((numberOfNegative) / (numberOfPositive + numberOfNegative))
            priorTrue = ((numberOfTrue) / (numberOfTrue + numberOfFake))
            priorFake = ((numberOfFake) / (numberOfTrue + numberOfFake))

            f.write("Pos" + " " + str(priorPos) + "\n")
            f.write("Neg" + " " + str(priorNeg) + "\n")
            f.write("Fake" + " " + str(priorFake) + "\n")
            f.write("True" + " " + str(priorTrue) + "\n")
            #Probability Calculation

            for word in finalCountDictionary:
                for property in properties:
                    if property not in finalCountDictionary[word]:
                        val = 0
                    else:
                        val = finalCountDictionary[word][property]
                    if property == 'true':
                        totalNumber = totalNumberOfTrue
                    if property == 'fake':
                        totalNumber = totalNumberOfFake
                    if property == 'pos':
                        totalNumber = totalNumberOfPos
                    if property == 'neg':
                        totalNumber = totalNumberOfNeg
                    countedProbability = ((val + 1)/(totalNumber + vocabularyLength))
                    stringToPrint = stringToPrint + str(countedProbability) + ","
                stringToPrint = stringToPrint[:-1]
                f.write(str(word) + " " + str(stringToPrint) + "\n")
                stringToPrint = ""





if __name__ == "__main__":
    main()
    #print(numberOfFake)
    #print(numberOfTrue)
    #print(numberOfNegative)
    #print(numberOfPositive)
    #print(countDictionary)
    #print(finalCountDictionary)
