# -*- coding: UTF-8 -*-
#!/usr/bin/env python2
from __future__ import division
import sys
import string
from collections import defaultdict

PNdictionary = {}
TFdictionary = {}
APNdictionary = {}
ATFdictionary = {}
VPNbias = 0
VTFbias = 0
APNbias = 0
ATFbias = 0
val = 0
Aval = 0
fake = 0
true = 0
Afake = 0
Atrue = 0
vanillaDictionary = {}
stringToWrite = ""

def getData(line,n):
    global VPNbias, VTFbias, PNdictionary, TFdictionary
    tokens = line.strip().split(" ")
    if n is 1:
        if (tokens[0] == "##biasVPN##"):
            VPNbias = tokens[1]
        else:
            PNdictionary[tokens[0]] = tokens[1]
    if n is 2:
        if(tokens[0] == "##biasVTF##"):
            VTFbias = tokens[1]
        else:
            TFdictionary[tokens[0]] = tokens[1]


def getDataAveragePerceptron(line,n):
    global APNbias, ATFbias, APNdictionary, ATFdictionary
    tokens = line.strip().split(" ")
    if n is 1:
        if (tokens[0] == "##biasAPN##"):
            APNbias = tokens[1]
        else:
            APNdictionary[tokens[0]] = tokens[1]
    if n is 2:
        if(tokens[0] == "##biasATF##"):
            ATFbias = tokens[1]
        else:
            ATFdictionary[tokens[0]] = tokens[1]



def getDetailsFromFile():
    n=0
    #/Users/parth/Desktop/USC/NLP/a3/vanillamodel.txt
    with open(sys.argv[1], 'r') as my_file:
        for line in my_file:
            if line.startswith("##FOR POS NEG##"):
                n=1
            elif line.startswith("##FOR TRUE FALSE##"):
                n=2
            else:
                getData(line,n)

def getDetailsFromFileAveragePerceptron():
    n=0
    #/Users/parth/Desktop/USC/NLP/a3/averagemodel.txt
    with open(sys.argv[1], 'r') as my_file:
        for line in my_file:
            if line.startswith("##FOR POS NEG##"):
                n=1
            elif line.startswith("##FOR TRUE FALSE##"):
                n=2
            else:
                getDataAveragePerceptron(line,n)

def calculatePN():
    global TFdictionary, PNdictionary,val, true, fake
    f= open("output.txt","w+")
    #/Users/parth/Desktop/USC/NLP/a3/coding-2-data-corpus/dev-text.txt
    with open(sys.argv[2], 'r') as my_file:
        for line in my_file:
            getDocumentID = line.strip('\n').split(' ',1)
            sentence = getDocumentID[1].lower()
            sentence = sentence.translate(None, string.punctuation)
            sentence = sentence.split(" ")
            currentDictionary = {}
            for word in sentence:
                if word in currentDictionary:
                    currentDictionary[word] = currentDictionary[word] + 1
                else:
                    currentDictionary[word] = 1
            for key,value in currentDictionary.iteritems():
                if(key in TFdictionary):
                    val = val + ((value)*(float(TFdictionary[key])))
            val = val + float(VTFbias)
            if(val<=0):
                stringToWrite = str(getDocumentID[0]) + " " + "Fake" + " "
                #print(str(getDocumentID[0]) + " " + "FAKE" + "\n")
                a=0
            else:
                stringToWrite = str(getDocumentID[0]) + " " + "True" + " "
                #print(str(getDocumentID[0]) + " " + "TRUE" + "\n")
                b=0
            val = 0

            #FOR positive Negative
            for key,value in currentDictionary.iteritems():
                if(key in TFdictionary):
                    val = val + ((value)*(float(PNdictionary[key])))
            val = val + float(VPNbias)
            if(val<=0):
                stringToWrite = stringToWrite + "Neg" + "\n"
                #print(str(getDocumentID[0]) + " " + "NEGATIVE" + "\n")
                fake = fake + 1
            else:
                stringToWrite = stringToWrite + "Pos" + "\n"
                #print(str(getDocumentID[0]) + " " + "POSIITIVE" + "\n")
                true = true + 1
            f.write(stringToWrite)
            stringToWrite = ""
            val = 0



def calculatePNAveragePerceptron():
    global ATFdictionary, APNdictionary,Aval, Atrue, Afake
    f= open("output.txt","w+")
    #/Users/parth/Desktop/USC/NLP/a3/coding-2-data-corpus/dev-text.txt
    with open(sys.argv[2], 'r') as my_file:
        for line in my_file:
            getDocumentID = line.strip('\n').split(' ',1)
            sentence = getDocumentID[1].lower()
            sentence = sentence.translate(None, string.punctuation)
            sentence = sentence.split(" ")
            currentDictionary = {}
            for word in sentence:
                if word in currentDictionary:
                    currentDictionary[word] = currentDictionary[word] + 1
                else:
                    currentDictionary[word] = 1
            for key,value in currentDictionary.iteritems():
                if(key in ATFdictionary):
                    Aval = Aval + ((value)*(float(ATFdictionary[key])))
            Aval = Aval + float(ATFbias)
            if(Aval<=0):
                stringToWrite = str(getDocumentID[0]) + " " + "Fake" + " "
                #print(str(getDocumentID[0]) + " " + "FAKE" + "\n")
                a=0
            else:
                stringToWrite = str(getDocumentID[0]) + " " + "True" + " "
                #print(str(getDocumentID[0]) + " " + "TRUE" + "\n")
                b=0
            Aval = 0

            #FOR positive Negative
            for key,value in currentDictionary.iteritems():
                if(key in ATFdictionary):
                    Aval = Aval + ((value)*(float(APNdictionary[key])))
            Aval = Aval + float(APNbias)
            if(Aval<=0):
                stringToWrite = stringToWrite + "Neg" + "\n"
                #print(str(getDocumentID[0]) + " " + "NEGATIVE" + "\n")
                Afake = Afake + 1
            else:
                stringToWrite = stringToWrite + "Pos" + "\n"
                #print(str(getDocumentID[0]) + " " + "POSIITIVE" + "\n")
                Atrue = Atrue + 1
            f.write(stringToWrite)
            stringToWrite = ""
            Aval = 0


def main():
    if 'vanillamodel.txt' in sys.argv[1]:
        getDetailsFromFile()
        calculatePN()
    else:
        getDetailsFromFileAveragePerceptron()
        calculatePNAveragePerceptron()


if __name__ == "__main__":
    main()
    print(fake)
    print(true)
