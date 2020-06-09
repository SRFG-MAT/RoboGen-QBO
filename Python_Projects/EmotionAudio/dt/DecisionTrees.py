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
def startDecisionTree(robotName):
    
    global area # tell Python interpreter variable area is global
    
    Various_Functions.qboSpeak('Hallo, mein Name ist' + robotName + ', der Roboter! Du hast die Entscheidungsbaeume gestartet!')
    Various_Functions.qboSpeak('Waehle nun den Entscheidungsbaum Sport, Stress, Schlaf oder Spiele, um fortzufahren.')
            
    sentence = Processing_Audio.getAudioToText()
    sentence = Various_Functions.normalize(sentence)
            
    if sentence.strip() == 'sport' or sentence.strip() == 'spart': # because always understands me wrong..
        area = 'EX'
    elif sentence.strip() == 'stress':
        area = 'STR'
    elif sentence.strip() == 'schlaf':
        area = 'SLE'
    elif sentence.strip() == 'spiele' or sentence.strip() == 'spielen': # because always understands me wrong..
        area = 'GAM'
    else:
        area = 'ERROR'
        Various_Functions.qboSpeak('Ich habe dich leider nicht richtig verstanden, versuchen wir es noch einmal')
    
#---------------------------------------------------------------------------------------------
# helper function to handle the tree and sub-trees    
#---------------------------------------------------------------------------------------------
def processDecisionTree():
    
    global area # tell Python interpreter variable area is global
    
    if area == 'ERROR':
        return
    
    while True:
        
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
                
                    area = JsonParser.goToNewArea(area, number)
                    os.system("mpg321 -q /opt/QBO/RoboGen-QBO/Python_Projects/EmotionAudio/mp3/SoundEffect_Confirm.mp3") # Bestätigungs-Sound abspielen
                else:
                    Various_Functions.qboSpeak('Diese Antwort ist leider nicht moeglich. Bitte hoer dir die letzte Frage noch einmal genau an')
        else:
            Various_Functions.qboSpeak('Diese Antwort ist leider nicht moeglich. Bitte hoer dir die letzte Frage noch einmal genau an')
        
        
        if area == 'end':
            Various_Functions.qboSpeak('Dein Entscheidungsbaum ist nun zu Ende! Auf Wiedersehen!')
            break
    
    
    

