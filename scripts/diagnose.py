import unirest
import json
import nltk
import difflib
import time
from nltk.corpus import wordnet

'''
response = unirest.get("https://priaid-symptom-checker-v1.p.rapidapi.com/symptoms?format=json&language=en-gb",headers={"X-RapidAPI-Key": "5cfd5f6a39mshb4dc4e26d173e45p15e8c7jsnfc8818261be7"})
json_symptoms = response.body


for sym in json_symptoms:
    print(sym['Name'])
'''

synonyms = []
other = []

for syn in wordnet.synsets("vomiting"):
    for l in syn.lemmas():
        synonyms.append(l.name())
start = time.time()
for syn in wordnet.synsets("vomiting"):
    for l in syn.lemmas():
        synonyms.append(l.name())
finish = time.time()
print((finish - start))

def similarityScore(a,b):   #returns a similarity score between two symptoms
    aWords = a.split(' ')
    bWords = b.split(' ')

    score = 0
    for itemA in aWords:
        for itemB in bWords:
            itemA = itemA.lower()
            itemB = itemB.lower()
            
            if(len(itemA) < 3 or len(itemB) < 3):
                continue
            
            similarity = difflib.SequenceMatcher(None,itemA,itemB).ratio()
            if (itemA in itemB) or (itemB in itemA):
                score += 1
            elif similarity > 0.5 and itemA[0] == itemB[0]:
                score += similarity
    return score

def getSymptomID(symptom,symptomList):
    bestSimilarity = 0
    bestName = ''
    bestID = ''
    for sym in symptomList:
        similarity = similarityScore(symptom,sym['Name'])
        if similarity > bestSimilarity:
            bestSimilarity = similarity
            bestName = sym['Name']
            bestID = sym['ID']
    return {"ID":bestID,"Name":bestName}


'''
while True:
    input = raw_input(">>")
    if input == "q":
        break
    else:
        result = getSymptomID(input,json_symptoms)
        print(result["Name"] + ", ID = " + str(result["ID"]))
'''
