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
        
        nrOfOptions = JsonParser.loadDTData(area)
    
        sentence = Processing_Audio.getAudioToText()
        sentence = JsonParser.normalize(sentence)     

        if sentence.strip() == 'antwort 1' and nrOfOptions >= 1: area = JsonParser.goToNewArea(area, 1)
        elif sentence.strip() == 'antwort 2' and nrOfOptions >= 2: area = JsonParser.goToNewArea(area, 2)
        elif sentence.strip() == 'antwort 3' and nrOfOptions >= 3: area = JsonParser.goToNewArea(area, 3)       
        elif sentence.strip() == 'antwort 4' and nrOfOptions >= 4: area = JsonParser.goToNewArea(area, 4)
        elif sentence.strip() == 'antwort 5' and nrOfOptions >= 5: area = JsonParser.goToNewArea(area, 5)
        elif sentence.strip() == 'antwort 6' and nrOfOptions >= 6: area = JsonParser.goToNewArea(area, 6)
        elif sentence.strip() == 'antwort 7' and nrOfOptions >= 7: area = JsonParser.goToNewArea(area, 7)
        elif sentence.strip() == 'antwort 8' and nrOfOptions >= 8: area = JsonParser.goToNewArea(area, 8)
        elif sentence.strip() == 'antwort 9' and nrOfOptions >= 9: area = JsonParser.goToNewArea(area, 9)
        else:
            JsonParser.qboSpeak('Diese Antwort ist leider nicht moeglich. Bitte hoer dir die letzte Frage noch einmal genau an')
        
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
    
    
    

