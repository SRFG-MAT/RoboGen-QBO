#!/usr/bin/env python
# coding=utf-8
import os
import json
from gtts import gTTS
from string import punctuation
import Various_Functions

dt_data = {}
intervention_data = {}

#---------------------------------------------------------------------------------------------
# read in and speak a question from json file
#---------------------------------------------------------------------------------------------
def loadDTData(area):
    
    with open('/home/pi/Documents/RoboGen-QBO/Python_Projects/EmotionAudio/dt/json/robogen_decisiontrees.json', 'r') as dt_file:
        dt_data = json.load(dt_file)
        
        # Frage
        Various_Functions.qboSpeak(dt_data[0][area]['question'])
        
        # Antwortmöglichkeiten
        i = 0
        for entry in dt_data[0][area]['options']:
            answerStr = 'Antwort: ' + str(i+1)
            Various_Functions.qboSpeak(answerStr + entry['question'])
            i = i + 1
            
        return i # return number of options

#---------------------------------------------------------------------------------------------
# load intervention data and print
#---------------------------------------------------------------------------------------------
def loadInterventionData(codeInput):
        
    with open('/home/pi/Documents/RoboGen-QBO/Python_Projects/EmotionAudio/dt/json/robogen_interventions.json', 'r') as interventions_file:
        intervention_data = json.load(interventions_file)
        
        print('Gesucht wird code: ' + codeInput)
        
        for entry in intervention_data:
            #print('text: ' + entry['text'])
            #print('link: ' + entry['link'])
            
            for code in entry['codes']:                 
                if code == codeInput:
                    print('code: ' + code)
                    Various_Functions.qboSpeak(entry['text'])
                
#---------------------------------------------------------------------------------------------
# load intervention data and print
#---------------------------------------------------------------------------------------------            
def goToNewArea(area, option):

    with open('/home/pi/Documents/RoboGen-QBO/Python_Projects/EmotionAudio/dt/json/robogen_decisiontrees.json', 'r') as dt_file:
        dt_data = json.load(dt_file)

        if dt_data[0][area]['options'][option-1]['action']['type'] == 'SUBTREE':
            return dt_data[0][area]['options'][option-1]['action']['ref']
        
        elif dt_data[0][area]['options'][option-1]['action']['type'] == 'INTERVENTION':
            loadInterventionData(dt_data[0][area]['options'][option-1]['action']['ref'][0])
            return 'end'
        
        else:
            return 'end'



