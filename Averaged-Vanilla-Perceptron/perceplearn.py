# -*- coding: UTF-8 -*-
#!/usr/bin/env python2
from __future__ import division
import sys
import string
from collections import defaultdict

stopWords = set()
mainDictionary = {} # contains docID:{word frequency}
documentIDList = [] #contains list of all docuemntID in sequence
TFPNDictionary = {}
tempDictionary = {}
weightDictionaryVTF = {}
weightDictionaryVPN = {}
weightDictionaryAPN = {}
weightDictionaryATF = {}
updatedWeightDictionaryAPN = {}
updatedWeightDictionaryATF = {}
finalWeightDictionary = {}
finalWeightDictionaryPN = {}
globalDictionary = {}
biasVTF=0
biasVPN = 0
biasATF = 0
biasAPN = 0
finalBiasATF = 0.0
finalBiasAPN = 0
updatedBiasATF = 0
updatedBiasAPN = 0
weightPN = 0
z=0
k=0
count = 0

# getting a list of stop words
def returnStopWords():
    with open('stopwords.txt') as f:
        lines = f.readlines()
        for line in lines:
            stopWords.add(line.strip('\n'))
    #print(len(stopWords))
    #print(stopWords)

def vanillaPerceptron():
    global documentIDList,biasVTF,weightDictionaryVTF,biasVPN
    #for True / False
    for i in range(0,30):
        for j in range(0,len(documentIDList)):
            currentDocumentID = documentIDList[j]
            activation = 0
            activationPN = 0
            currentTrueOrFalse = TFPNDictionary[currentDocumentID]['TorF']
            currentPosorNeg = TFPNDictionary[currentDocumentID]['PorN']
            for key,value in mainDictionary[currentDocumentID].iteritems():
                if key not in weightDictionaryVTF:
                    weight = 0
                    weightDictionaryVTF[key] = 0
                else:
                    weight = weightDictionaryVTF[key]
                activation = activation + ((weight) * value)
            activation = activation + biasVTF
            if (((currentTrueOrFalse) * activation) <= 0):
                for key,value in mainDictionary[currentDocumentID].iteritems():
                    weightDictionaryVTF[key] = weightDictionaryVTF[key] + ((currentTrueOrFalse)*(mainDictionary[currentDocumentID][key]))
                biasVTF = biasVTF + currentTrueOrFalse

            # Positive Negative Calculation
            for key,value in mainDictionary[currentDocumentID].iteritems():
                if key not in weightDictionaryVPN:
                    weightPN = 0
                    weightDictionaryVPN[key] = 0
                else:
                    weightPN = weightDictionaryVPN[key]
                activationPN = activationPN + ((weightPN) * value)
            activationPN = activationPN + biasVPN
            if(((currentPosorNeg) * activationPN) <= 0):
                for key,value in mainDictionary[currentDocumentID].iteritems():
                    weightDictionaryVPN[key] = weightDictionaryVPN[key] + ((currentPosorNeg)*mainDictionary[currentDocumentID][key])
                biasVPN = biasVPN + currentPosorNeg

            weightPN = weight = 0
    #print Weight values to file VPN
    with open("vanillamodel.txt","w") as f:
        f.write("##FOR POS NEG##" + "\n")
        f.write("##biasVPN##" + " " + str(biasVPN) + "\n")
        for key,value in weightDictionaryVPN.iteritems():
            f.write(key + " " + str(value) + "\n")
        f.write("##FOR TRUE FALSE##" + "\n")
        f.write("##biasVTF##" + " " + str(biasVTF) + "\n")
        for key,value in weightDictionaryVTF.iteritems():
            f.write(key + " " + str(value) + "\n")

#average Perceptron Implementaion
def averagePerceptron():
    global documentIDList,biasATF,weightDictionaryATF,biasAPN, updatedBiasATF,count,finalBiasATF,weightDictionaryAPN,updatedWeightDictionaryATF,updatedWeightDictionaryAPN, updatedBiasATF, updatedBiasAPN, finalBiasAPN, finalWeightDictionaryPN
    #for True / False
    count = 1
    for i in range(0,100):
        for j in range(0,len(documentIDList)):
            currentDocumentID = documentIDList[j]
            activation = 0
            activationPN = 0
            currentTrueOrFalse = TFPNDictionary[currentDocumentID]['TorF']
            currentPosorNeg = TFPNDictionary[currentDocumentID]['PorN']
            for key,value in mainDictionary[currentDocumentID].iteritems():
                if key not in weightDictionaryATF:
                    weight = 0
                    weightDictionaryATF[key] = 0
                else:
                    weight = weightDictionaryATF[key]
                activation = activation + ((weight) * value)
            activation = activation + biasATF
            if (((currentTrueOrFalse) * activation) <= 0):
                for key,value in mainDictionary[currentDocumentID].iteritems():
                    weightDictionaryATF[key] = weightDictionaryATF[key] + ((currentTrueOrFalse)*(mainDictionary[currentDocumentID][key]))
                biasATF = biasATF + currentTrueOrFalse

                for key,value in weightDictionaryATF.iteritems():
                    if key not in updatedWeightDictionaryATF:
                        updatedWeightDictionaryATF[key] = 0

                for key,value in mainDictionary[currentDocumentID].iteritems():
                    updatedWeightDictionaryATF[key] = updatedWeightDictionaryATF[key] + ((currentTrueOrFalse)*(mainDictionary[currentDocumentID][key])*(count))
                updatedBiasATF = updatedBiasATF + ((currentTrueOrFalse)*(count))
            count = count + 1
            # Positive Negative Calculation

            for key,value in mainDictionary[currentDocumentID].iteritems():
                if key not in weightDictionaryAPN:
                    weight = 0
                    weightDictionaryAPN[key] = 0
                else:
                    weight = weightDictionaryAPN[key]
                activationPN = activationPN + ((weight) * value)
            activation = activation + biasATF
            if (((currentTrueOrFalse) * activationPN) <= 0):
                for key,value in mainDictionary[currentDocumentID].iteritems():
                    weightDictionaryAPN[key] = weightDictionaryAPN[key] + ((currentTrueOrFalse)*(mainDictionary[currentDocumentID][key]))
                biasAPN = biasAPN + currentTrueOrFalse

                for key,value in weightDictionaryAPN.iteritems():
                    if key not in updatedWeightDictionaryAPN:
                        updatedWeightDictionaryAPN[key] = 0

                for key,value in mainDictionary[currentDocumentID].iteritems():
                    updatedWeightDictionaryAPN[key] = updatedWeightDictionaryAPN[key] + ((currentTrueOrFalse)*(mainDictionary[currentDocumentID][key])*(count))
                updatedBiasAPN = updatedBiasAPN + ((currentTrueOrFalse)*(count))
            count = count + 1

            weightPN = weight = 0

    for key,value in updatedWeightDictionaryATF.iteritems():
        finalWeightDictionary[key] = weightDictionaryATF[key] - ((updatedWeightDictionaryATF[key])/count)
    finalBiasATF = biasATF - ((updatedBiasATF)/count)
    #print(biasATF)
    #print(updatedBiasATF)
    #print(((updatedBiasATF)/count))
    for key,value in updatedWeightDictionaryAPN.iteritems():
        finalWeightDictionaryPN[key] = weightDictionaryAPN[key] - ((updatedWeightDictionaryAPN[key])/count)
    finalBiasAPN = biasAPN - ((updatedBiasAPN)/count)

    #print Weight values to file APN
    with open("averagemodel.txt","w") as f:
        f.write("##FOR POS NEG##" + "\n")
        f.write("##biasAPN##" + " " + str(finalBiasAPN) + "\n")
        for key,value in finalWeightDictionaryPN.iteritems():
            f.write(key + " " + str(value) + "\n")
        f.write("##FOR TRUE FALSE##" + "\n")
        f.write("##biasATF##" + " " + str(finalBiasATF) + "\n")
        for key,value in finalWeightDictionary.iteritems():
            f.write(key + " " + str(value) + "\n")




def main():
    global mainDictionary
    returnStopWords()
    with open(sys.argv[1], 'r') as my_file:
        for line in my_file:
            getLineDetails = line.split(' ',3)
            # get value of y. If true y=1, if false y= -1
            documentID = getLineDetails[0]
            documentIDList.append(documentID)
            if getLineDetails[1] == "True":
                Yvalue = 1
            else:
                Yvalue = -1
            # get value of z. If true z=1, if false z= -1
            if getLineDetails[2] == "Pos":
                Zvalue = 1
            else:
                Zvalue = -1
            #sentence manipulation
            tempDictionary['TorF'] = Yvalue
            tempDictionary['PorN'] = Zvalue
            TFPNDictionary[documentID] = tempDictionary.copy()
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
                    #if word in globalDictionary:
                        #globalDictionary[word] = globalDictionary[word] + 1
                    #else:
                        #globalDictionary[word] = 1
            mainDictionary[documentID] = currentDictionary.copy()
            currentDictionary.clear()
    vanillaPerceptron()
    averagePerceptron()



if __name__ == "__main__":
    main()
    #print(TFPNDictionary)
    #print(len(globalDictionary))
    #print(mainDictionary)
    #print(biasVTF)
    #print(biasVPN)
    #print(finalWeightDictionary)
    print(finalBiasATF)
    print(finalBiasAPN)
    #print(len(updatedWeightDictionaryATF))
    #print(len(weightDictionaryATF))
    #print(count)
