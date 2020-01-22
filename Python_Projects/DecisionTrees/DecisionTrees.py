#!/usr/bin/env python
# coding=utf-8
import sys
import Processing_Audio
import JsonParser

area = 'UNKNOWN'

#---------------------------------------------------------------------------------------------
# helper function to wait for wake word and tree selection
#---------------------------------------------------------------------------------------------
def startDecisionTree():
    
    global area # tell Python interpreter variable area is global
    
    while True:
        sentence = Processing_Audio.getAudioToText()
        sentence = JsonParser.normalize(sentence)
    
        if sentence.strip() == "starte entscheidungsbaum":
            JsonParser.qboSpeak('Hallo, mein Name ist QBO! Du hast die Entscheidungsbaeume gestartet!')
            JsonParser.qboSpeak('Waehle nun den Entscheidungsbaum Sport, Stress, Schlaf oder Spiele, um fortzufahren.')
            
            sentence = Processing_Audio.getAudioToText()
            sentence = JsonParser.normalize(sentence)
            
            if sentence.strip() == 'sport':
                area = 'EX'
                break
            elif sentence.strip() == 'stress':
                area = 'STR'
                break
            elif sentence.strip() == 'schlaf':
                area = 'SLE'
                break
            elif sentence.strip() == 'spiele':
                area = 'GAM'
                break
            else:
                area = 'ERROR'
                JsonParser.qboSpeak('Ich habe dich leider nicht richtig verstanden, versuchen wir es noch einmal')
    
#---------------------------------------------------------------------------------------------
# helper function to handle the tree and sub-trees    
#---------------------------------------------------------------------------------------------
def processDecisionTree():
    
    global area # tell Python interpreter variable area is global
    
    while True:
        
        JsonParser.loadDTData(area)
    
        sentence = Processing_Audio.getAudioToText()
        sentence = JsonParser.normalize(sentence)     

        if sentence.strip() == 'antwort 1': area = JsonParser.goToNewArea(area, 1)
        elif sentence.strip() == 'antwort 2': area = JsonParser.goToNewArea(area, 2)
        elif sentence.strip() == 'antwort 3': area = JsonParser.goToNewArea(area, 3)
        else: break
        
        if area == 'end':
            JsonParser.qboSpeak('Dein Entscheidungsbaum ist nun zu Ende! Auf Wiedersehen!')
            break

#---------------------------------------------------------------------------------------------
# MainProgram Start - (entrance point)
#---------------------------------------------------------------------------------------------
while True:

    # wait for wake word and tree selection
    startDecisionTree()
    
    # handle tree and sub trees
    processDecisionTree()
    
    
    

