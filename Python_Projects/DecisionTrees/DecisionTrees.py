#!/usr/bin/env python
# coding=utf-8
import sys
import Processing_Audio
import JsonParser

area = ''

#---------------------------------------------------------------------------------------------
# MainProgram Start - (entrance point)
#---------------------------------------------------------------------------------------------
while True:

    # warte auf wake word
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
                JsonParser.qboSpeak('Ich habe dich leider nicht richtig verstanden, versuchen wir es noch einmal')         

    
    # sammle alle Sätze zusammen
    while True:
        
        JsonParser.loadDTData(area)
    
        sentence = Processing_Audio.getAudioToText()
        sentence = JsonParser.normalize(sentence)
        

        if sentence.strip() == 'antwort 1':
            area = JsonParser.goToNewArea(area, 1)
        elif sentence.strip() == 'antwort 2':
            area = JsonParser.goToNewArea(area, 2)
        elif sentence.strip() == 'antwort 3':
            area = JsonParser.goToNewArea(area, 3)
        else:
            break
        
        if area == 'end':
            JsonParser.qboSpeak('Dein Entscheidungsbaum ist nun zu Ende! Auf Wiedersehen!')
            break

