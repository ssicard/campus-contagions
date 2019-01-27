import unirest
import json
import nltk
import difflib
import time

symptomNames = []  #Pair these with GPS coordinates for the database

#returns a similarity score between two symptoms
def similarityScore(a,b):
    aWords = a.split(' ')
    bWords = b.split(' ')
    
    index = 0
    for word in aWords:
        if word.lower() == "stomach":
            aWords[index] = "abdominal"
        elif word.lower() == "ache":
            aWords[index] = "pain"
        elif word.lower() == "poop":
            aWords[index] = "defacation"
        elif word.lower() == "swollen":
            aWords[index] = "swelling"
        elif word.lower() == "hurts":
            aWords[index] = "pain"
        elif word.lower() == "stinky":
            aWords[index] = "foul smelling"
        elif word.lower() == "decreased":
            aWords[index] = "reduced"
        elif word.lower() == "easily":
            aWords[index] = "foul smelling"
        elif word.lower() == "nasal":
            aWords[index] = "nose"
        elif word.lower() == "congestion":
            aWords[index] = "stuffy"
        elif word.lower() == "tired":
            aWords[index] = "tiredness"
        index += 1

    score = 0
    for itemA in aWords:
        for itemB in bWords:
            itemA = itemA.lower()
            itemB = itemB.lower()
            
            if(len(itemA) < 3 or len(itemB) < 3):
                continue
            
            similarity = difflib.SequenceMatcher(None,itemA,itemB).ratio()
            if (itemA in itemB) or (itemB in itemA):
                if len(bWords) == 1:
                    score += 3
                else:
                    score += 1
            elif similarity > 0.5 and itemA[0] == itemB[0]:
                score += similarity

    return score

#returns info of most likely medical symptom given symptom entry
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

#generates the API string for diagnosis given the symptom IDs, gender, and year of birth
def genApiStr(symptomIDs,gender,YOB):
    apiStr = 'https://priaid-symptom-checker-v1.p.rapidapi.com/diagnosis?symptoms=%5B'
    for id in symptomIDs:
        apiStr += str(id)
        apiStr += '%2C'

    apiStr = apiStr[:-3]
    apiStr += '%5D&gender='
    apiStr += gender.lower()
    apiStr += '&year_of_birth='
    apiStr += str(YOB)
    apiStr += '&language=en-gb'

    return apiStr


def getDiagnosisResults(symptomString, gender, birthYear):
    response = unirest.get("https://priaid-symptom-checker-v1.p.rapidapi.com/symptoms?format=json&language=en-gb",headers={"X-RapidAPI-Key": "5cfd5f6a39mshb4dc4e26d173e45p15e8c7jsnfc8818261be7"})
    json_symptoms = response.body
    
    commaSplit = symptomString.split(',')
    symptoms = []
    for sym in commaSplit:
        symptoms.append(sym.strip())

    resultList = []  #list of ID,name pairs
    symptomIDs = []
    for sym in symptoms:
        resultList.append(getSymptomID(str(sym),json_symptoms))

    for res in resultList:
        #print(res['Name'])
        symptomNames.append(res['Name'])
        symptomIDs.append(res['ID'])

    #retrieve the diagnosis results
    diagnosisResults = unirest.get(genApiStr(symptomIDs,gender,birthYear),
        headers={"X-RapidAPI-Key": "5cfd5f6a39mshb4dc4e26d173e45p15e8c7jsnfc8818261be7"})

    #returns the diagnosis json file
    return diagnosisResults.body
    

def getSymptomList():
    return symptomNames






'''
topHits = getDiagnosisResults('fever,vomiting,diarrhea', 'male', '1984')

for hit in topHits:
    print(hit['Issue']['Name'])
'''
