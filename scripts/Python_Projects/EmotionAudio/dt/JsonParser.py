#!/usr/bin/env python
# coding=utf-8
import os, sys
import json
import random
import requests
import base64
from gtts import gTTS
from string import punctuation
import Various_Functions

# saved settings
sys.path.append('/opt/QBO/catkin_ws/src/RoboGen-QBO/scripts/Python_Projects/MyQBOSettings')
import SettingsReader

dt_endpoint = 'https://api.jsonstorage.net/v1/json/e7278ae4-8cca-42e7-bba7-5eb3fe91b6f1'
dt_data = {}
intervention_data = {}
sen = SettingsReader.getUserSen()
diab = SettingsReader.getUserDiab()
special_char_map = {ord(u'ä'):u'ae', ord(u'Ä'):u'Ae', ord(u'ü'):u'ue', ord(u'Ü'):u'Ue', ord(u'ö'):u'oe', ord(u'Ö'):u'Oe', ord(u'ß'):u'ss'}

#---------------------------------------------------------------------------------------------
# read in and speak a question from json file
#---------------------------------------------------------------------------------------------
def loadDTData(area):

    if (area == 'EX' or area == 'STR' or area == 'SLE' or area == 'SEN'):
        clearDT()

    with open('/opt/QBO/catkin_ws/src/RoboGen-QBO/scripts/Python_Projects/EmotionAudio/dt/json/robogen_decisiontrees.json', 'r') as dt_file:
        dt_data = json.load(dt_file)
        
        data = {
            "area": area,
            "question": "",
            "answers": [],
            "answer": -1,
            "link": ""
        }

        # Frage
        question = dt_data[0][area]['question']
        question = question.translate(special_char_map)
        data['question'] = question
        print(question)
        
        # Antwortmöglichkeiten
        i = 0
        for entry in dt_data[0][area]['options']:
            if ((entry['condition'] == '') or (entry['condition'] == 'diabetes=true' and diab) or (entry['condition'] == 'diabetes=false' and not diab) or (entry['condition'] == 'age>=60' and sen)):
                answerStr = 'Antwort ' + str(i+1) + ': '
                answerStr2 = entry['question']
                answerStr2 = answerStr2.translate(special_char_map)
                print(answerStr + answerStr2)
                data['answers'].append(answerStr2)
                i = i + 1

        uploadDT(data)

        Various_Functions.qboSpeak(question)
        j=0
        for entry in dt_data[0][area]['options']:
            if ((entry['condition'] == '') or (entry['condition'] == 'diabetes=true' and diab) or (entry['condition'] == 'diabetes=false' and not diab) or (entry['condition'] == 'age>=60' and sen)):
                answerStr = 'Antwort: ' + str(j+1) + '. '
                answerStr2 = entry['question']
                answerStr2 = answerStr2.translate(special_char_map)
                Various_Functions.qboSpeak(answerStr + answerStr2)
                j = j + 1
        
        Various_Functions.qboSpeak('Waehle nun aus')
            
        return i # return number of options

#---------------------------------------------------------------------------------------------
# load intervention data and print
#---------------------------------------------------------------------------------------------
def loadInterventionData(codeInput):
        
    with open('/opt/QBO/catkin_ws/src/RoboGen-QBO/scripts/Python_Projects/EmotionAudio/dt/json/robogen_interventions.json', 'r') as interventions_file:
        intervention_data = json.load(interventions_file)
        
        print('Gesucht wird code: ')
        print(''.join(codeInput))
        
        entries = []
        links = []
        
        for entry in intervention_data:
            #print('text: ' + entry['text'])
            #print('link: ' + entry['link'])
            
            for code in entry['codes']:
                for codeI in codeInput:			
                    if code == codeI:
                        #print('code: ' + code)
                        entries.append(entry['text'])
                        links.append(entry['link'])
        
        if len(entries) > 0:
            idx = random.randint(0,(len(entries)-1))
            intervention = entries[idx]
            intervention = intervention.translate(special_char_map)
            outp = intervention
            link = ""
            if (links[idx] != ""):
                link = links[idx]
                outp = outp + " Zu diesem Thema gibt es weiterfuehrende Links. Du findest diese am Tablet."
            data = {
                "area": "END",
                "question": intervention,
                "answers": [],
                "answer": -1,
                "link": link
            }
            uploadDT(data)
            print(outp)
            Various_Functions.qboSpeak(outp)
                
#---------------------------------------------------------------------------------------------
# load intervention data and print
#---------------------------------------------------------------------------------------------            
def goToNewArea(area, option):

    with open('/opt/QBO/catkin_ws/src/RoboGen-QBO/scripts/Python_Projects/EmotionAudio/dt/json/robogen_decisiontrees.json', 'r') as dt_file:
        dt_data = json.load(dt_file)

        tmp = option
        tmp2 = 0
        tmp3 = 0
        for entry in dt_data[0][area]['options']:
            if ((entry['condition'] == '') or (entry['condition'] == 'diabetes=true' and diab) or (entry['condition'] == 'diabetes=false' and not diab) or (entry['condition'] == 'age>=60' and sen)):
                tmp = tmp - 1
                tmp2 = tmp2 + 1
                if (tmp == 0):
                    tmp3 = tmp2
            else:
                tmp2 = tmp2 + 1

        addAnswerDT(area,tmp3-1)

        if dt_data[0][area]['options'][tmp3-1]['action']['type'] == 'SUBTREE':
            return dt_data[0][area]['options'][tmp3-1]['action']['ref']
        
        elif dt_data[0][area]['options'][tmp3-1]['action']['type'] == 'INTERVENTION':
            loadInterventionData(dt_data[0][area]['options'][tmp3-1]['action']['ref'])
            return 'end'
        
        else:
            return 'end'


# -------------------------------------------------------------------------------------------
# uploadDT
# -------------------------------------------------------------------------------------------
def uploadDT(data):
    
    data_old = json.loads(downloadDT())
    data_old.append(data)
    data_new = data_old
    
    try:
        r = requests.put(dt_endpoint, timeout=5, verify=False, json=data_new)
        headers = {'Content-type': 'application/json'}      
            
        if r.ok:
            print("DT gespeichert")
        else:
            print("--------------------------")
            print("Fehler bei Server-Antwort: " + str(r.status_code))
            print("--------------------------")
                        
    except requests.exceptions.RequestException as e:
        print e
        
# -------------------------------------------------------------------------------------------
# downloadDT
# -------------------------------------------------------------------------------------------
def downloadDT():
    
    try:
        r = requests.get(dt_endpoint, timeout=5, verify=False, json='')
        headers = {'Content-type': 'application/json'}      
            
        if r.ok:
            #print(r.content)
            return r.content
        else:
            print("--------------------------")
            print("Fehler bei Server-Antwort: " + str(r.status_code))
            print("--------------------------")
            return "Error"
                        
    except requests.exceptions.RequestException as e:
        print e

# -------------------------------------------------------------------------------------------
# addAnswerDT
# -------------------------------------------------------------------------------------------
def addAnswerDT(area,answer):
    
    data = json.loads(downloadDT())
    for entry in data:
        if (entry['area']==area):
            entry['answer']=answer
    
    try:
        r = requests.put(dt_endpoint, timeout=5, verify=False, json=data)
        headers = {'Content-type': 'application/json'}      
            
        if r.ok:
            print("DT Antwort hinzugefuegt")
        else:
            print("--------------------------")
            print("Fehler bei Server-Antwort: " + str(r.status_code))
            print("--------------------------")
                        
    except requests.exceptions.RequestException as e:
        print e

# -------------------------------------------------------------------------------------------
# clearDT
# -------------------------------------------------------------------------------------------
def clearDT():
    
    try:
        r = requests.put(dt_endpoint, timeout=5, verify=False, json=[])
        headers = {'Content-type': 'application/json'}      
            
        if r.ok:
            print("DT geleert")
        else:
            print("--------------------------")
            print("Fehler bei Server-Antwort: " + str(r.status_code))
            print("--------------------------")
                        
    except requests.exceptions.RequestException as e:
        print e