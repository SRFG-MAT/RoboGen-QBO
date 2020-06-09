#!/usr/bin/env python
# coding=utf-8
import os, sys
import Processing_Audio
import Various_Functions

#---------------------------------------------------------------------------------------------
# helper function to start EmotionAnalyze
#---------------------------------------------------------------------------------------------
def startEmotionAnalyze(robotName):
    
    Various_Functions.qboSpeak('Hallo, mein Name ist ' + robotName + ', der Roboter! Erzaehl mir etwas und ich werde versuchen deinen Satz zu verstehen und zu analysieren!')
    Various_Functions.qboSpeak('Bei meiner Analyse gehe ich vor Allem auf deine Gefuehle ein! Dazu sehe ich mir an, wie du deinen Satz formuliert hast.')
    Various_Functions.qboSpeak('Probier es aus! Sag mir ein paar Saetze und wenn du fertig bist sag: Satzanalyse beenden!')
    Various_Functions.qboSpeak('Danach gehen wir deine Saetze gemeinsam durch! Hoffen wir mal ich schaffe es, die Saetze richtig zu deuten! Los gehts!')
    
#---------------------------------------------------------------------------------------------
# helper function to process EmotionAnalyze
#---------------------------------------------------------------------------------------------
def processEmotionAnalyze():
    
    allSentences = []
    
    while True:
    
        print("Jetzt sprechen um einen Satz aufzuzeichnen!")    
        sentence = Processing_Audio.getAudioToText()
        sentence = Various_Functions.normalize(sentence)       

        if sentence.strip() == "satzanalyse beenden":
            break
        else:
            allSentences.append(sentence)
            os.system("mpg321 -q /opt/QBO/RoboGen-QBO/Python_Projects/EmotionAudio/mp3/SoundEffect_Confirm.mp3") # Bestätigungs-Sound abspielen
 
    # analysiere und beantworte alle Sätze
    Various_Functions.qboResponse(allSentences)
    
    