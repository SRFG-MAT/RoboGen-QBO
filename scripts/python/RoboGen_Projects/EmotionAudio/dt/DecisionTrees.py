#!/usr/bin/env python
# coding=utf-8
import os, sys
import JsonParser
import Processing_Audio
import Various_Functions

area = 'UNKNOWN'

#---------------------------------------------------------------------------------------------
# helper function to wait for wake word and tree selection
#---------------------------------------------------------------------------------------------
def startDecisionTree(skip):
    
    global area # tell Python interpreter variable area is global
    
    if (not skip):
        Various_Functions.qboSpeak('Du hast den Dialog gestartet! Waehle nun Sport, Stress, Schlaf oder SeniorInnen, um fortzufahren.')
            
    sentence = Processing_Audio.getAudioToText()
    sentence = Various_Functions.normalize(sentence)
            
    if sentence.strip() == 'sport' or sentence.strip() == 'spart': # because always understands me wrong..
        area = 'EX'
        processDecisionTree()
    elif sentence.strip() == 'stress':
        area = 'STR'
        processDecisionTree()
    elif sentence.strip() == 'schlaf':
        area = 'SLE'
        processDecisionTree()
    #elif sentence.strip() == 'spiele' or sentence.strip() == 'spielen': # because always understands me wrong..
    #    area = 'GAM'
    elif sentence.strip() == "seniorinnen":
        area = 'SEN'
        processDecisionTree()
    else:
        area = 'ERROR'
        Various_Functions.qboSpeak('Ich habe dich leider nicht richtig verstanden, versuchen wir es noch einmal')
        startDecisionTree(True)
    
#---------------------------------------------------------------------------------------------
# helper function to handle the tree and sub-trees    
#---------------------------------------------------------------------------------------------
def processDecisionTree():
    
    global area # tell Python interpreter variable area is global
    skip = False
    
    if area == 'ERROR':
        return
    
    while True:
        
        if (not skip):
            nrOfOptions = JsonParser.loadDTData(area)
    
        sentence = Processing_Audio.getAudioToText()
        sentence = Various_Functions.normalize(sentence)

        if  (
            sentence.strip() == 'antwort 1' or
            sentence.strip() == 'antwort 2' or
            sentence.strip() == 'antwort 3' or
            sentence.strip() == 'antwort 4' or
            sentence.strip() == 'antwort 5' or
            sentence.strip() == 'antwort 6' or
            sentence.strip() == 'antwort 7' or
            sentence.strip() == 'antwort 8' or
            sentence.strip() == 'antwort 9' or
            sentence.strip() == 'antwort 10' or
            sentence.strip() == 'antwort 11' or
            sentence.strip() == 'antwort 12' or
            sentence.strip() == 'antwort 13'
            ):                             
                number = [int(s) for s in sentence.strip().split() if s.isdigit()][0]
                
                if(nrOfOptions >= number):
                    skip = False
                    area = JsonParser.goToNewArea(area, number)
                    #os.system("mpg321 -q /opt/QBO/catkin_ws/src/RoboGen-QBO/scripts/Python_Projects/EmotionAudio/mp3/SoundEffect_Confirm.mp3") # Bestätigungs-Sound abspielen
                else:
                    Various_Functions.qboSpeak('Diese Antwort ist leider nicht moeglich. Bitte schau dir die letzte Frage noch einmal genau an')
                    skip = True
        else:
            Various_Functions.qboSpeak('Diese Antwort ist leider nicht moeglich. Bitte schau dir die letzte Frage noch einmal genau an')
            skip = True
        
        
        if area == 'end':
            Various_Functions.qboSpeak('Dein Dialog ist nun zu Ende! Auf Wiedersehen!')
            break
    
    
    

