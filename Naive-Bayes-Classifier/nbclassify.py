# -*- coding: UTF-8 -*-
#!/usr/bin/env python2
from __future__ import division
import sys
import string
from collections import defaultdict
import math

countNumberOfLines = 0
priorPos = 0
priorNeg = 0
priorFake = 0
priorTrue = 0
wordDictionary = {}
properties = ['pos','neg','true','fake']
valueCount = 0
gradePos = 0
gradeNeg = 0
gradeTrue = 0
gradeFake = 0

def getValuesFromFile():
    global countNumberOfLines, priorNeg, priorPos, priorFake, priorTrue, wordDictionary, properties, valueCount
    with open("nbmodel.txt", 'r') as my_file:
        for line in my_file:
            if countNumberOfLines < 4:
                countNumberOfLines = countNumberOfLines + 1
                line = line.strip('\n').split(" ")
                if line[0] == 'Pos':
                    priorPos = float(line[1])
                if line[0] == 'Neg':
                    priorNeg = float(line[1])
                if line[0] == 'Fake':
                    priorFake = float(line[1])
                if line[0] == 'True':
                    priorTrue = float(line[1])
                #print(line)
            else:
                line = line.strip('\n').split(' ')
                if ((line[0] is '') or line[0].isdigit()):
                    print(line)
                else:
                    values = line[1].split(",")
                    for property in properties:
                        wordDictionary.setdefault(line[0], {})[property] = 0
                        wordDictionary[line[0]][property] = float(values[valueCount])
                        valueCount = valueCount + 1
                    valueCount = 0

def classifyDocument():
    f = open("nboutput.txt",'w')
    global gradePos, gradeFake, gradeNeg, gradeTrue
    with open(sys.argv[1], 'r') as my_file:
        for line in my_file:
            getDocumentID = line.strip('\n').split(' ',1)
            sentence = getDocumentID[1].lower()
            sentence = sentence.translate(None, string.punctuation)
            sentence = sentence.split(" ")
            print(len(wordDictionary))
            for token in sentence:
                if(wordDictionary.has_key(token)):
                    gradePos = gradePos + math.log(wordDictionary[token]['pos'])
                    gradeNeg = gradeNeg + math.log(wordDictionary[token]['neg'])
                    gradeTrue = gradeTrue + math.log(wordDictionary[token]['true'])
                    gradeFake = gradeFake + math.log(wordDictionary[token]['fake'])
            gradePos = gradePos + math.log(priorPos)
            gradeNeg = gradeNeg + math.log(priorNeg)
            gradeTrue = gradeTrue + math.log((priorTrue))
            gradeFake = gradeFake + math.log(priorFake)
            if (gradePos >= gradeNeg):
                posOrNeg = "Pos"
            else:
                posOrNeg = "Neg"
            if (gradeTrue >= gradeFake):
                trueOrFake = "True"
            else:
                trueOrFake = "Fake"
            f.write(getDocumentID[0] + " " + trueOrFake + " " + posOrNeg + "\n")
            gradeFake = gradeTrue = gradeNeg = gradePos = 0





def main():
    getValuesFromFile()
    classifyDocument()


if __name__ == "__main__":
    main()
    #print(priorTrue)
    #print(priorFake)
    #print(priorNeg)
    #print(priorPos)
    #print(wordDictionary)
    #print(gradePos)