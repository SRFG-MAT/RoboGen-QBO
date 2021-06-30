#!/usr/bin/env python
# coding=utf-8
import os, sys
import json
import random
from gtts import gTTS
from string import punctuation
import Various_Functions

# saved settings
sys.path.append('/opt/QBO/catkin_ws/src/RoboGen-QBO/scripts/Python_Projects/MyQBOSettings')
import SettingsReader

dt_data = {}
intervention_data = {}
sen = SettingsReader.getUserSen()
diab = SettingsReader.getUserDiab()

#---------------------------------------------------------------------------------------------
# read in and speak a question from json file
#---------------------------------------------------------------------------------------------
def loadDTData(area):
    
    with open('/opt/QBO/catkin_ws/src/RoboGen-QBO/scripts/Python_Projects/EmotionAudio/dt/json/robogen_decisiontrees.json', 'r') as dt_file:
        dt_data = json.load(dt_file)
        
        # Frage
        print(dt_data[0][area]['question'])
        Various_Functions.qboSpeak(dt_data[0][area]['question'])
        
        # Antwortmöglichkeiten
        i = 0
        for entry in dt_data[0][area]['options']:
            if ((entry['condition'] == '') or (entry['condition'] == 'diabetes=true' and diab) or (entry['condition'] == 'diabetes=false' and not diab) or (entry['condition'] == 'age>=60' and sen)):
                answerStr = 'Antwort: ' + str(i+1) + '. '
                print(answerStr + entry['question'])
                Various_Functions.qboSpeak(answerStr + entry['question'])
                i = i + 1
        
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
            outp = entries[idx]
            if (links[idx] != ""):
                #ToDo: push link to reading list and add to android app
                link = links[idx]
                #print('link to save: ' + link)
                outp = outp + "Zu diesem Thema gibt es weiterfuehrende Links. Du findest diese am Tablet."
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

        if dt_data[0][area]['options'][tmp3-1]['action']['type'] == 'SUBTREE':
            return dt_data[0][area]['options'][tmp3-1]['action']['ref']
        
        elif dt_data[0][area]['options'][tmp3-1]['action']['type'] == 'INTERVENTION':
            loadInterventionData(dt_data[0][area]['options'][tmp3-1]['action']['ref'])
            return 'end'
        
        else:
            return 'end'



