#!/usr/bin/env python
# coding=utf-8
import sys
import os

sys.path.append('/home/pi/Documents/RoboGen-QBO/Python_Projects/EmotionSpeech/dt')
import Processing_Audio
import Various_Functions
import DecisionTrees

#---------------------------------------------------------------------------------------------
# helper function to start EmotionAnalyze
#---------------------------------------------------------------------------------------------
def startEmotionAnalyze():
    Various_Functions.qboSpeak('Hallo, mein Name ist QBO! Erzaehl mir etwas und ich werde versuchen deinen Satz zu verstehen und zu analysieren!')
    Various_Functions.qboSpeak('Bei meiner Analyse gehe ich vor Allem auf deine Gefuehle ein! Dazu sehe ich mir an, wie du deinen Satz formuliert hast.')
    Various_Functions.qboSpeak('Probier es aus! Sag mir ein paar Saetze und wenn du fertig bist sag: Aufzeichnung beenden!')
    Various_Functions.qboSpeak('Danach gehen wir deine Saetze gemeinsam durch! Hoffen wir mal ich schaffe es, die Saetze richtig zu deuten! Los gehts!')
    
#---------------------------------------------------------------------------------------------
# helper function to process EmotionAnalyze
#---------------------------------------------------------------------------------------------
def processEmotionAnalyze():
    while True:
    
        print("------------------------------------------------------")
        print("Jetzt sprechen um einen Satz aufzuzeichnen!")
        print("------------------------------------------------------")
    
        sentence = Processing_Audio.getAudioToText()
        sentence = Various_Functions.normalize(sentence)
        
        print("------------------------------------------------------")
        print("Google Speech Recognition glaubt du sagst: \n" + sentence)
        print("------------------------------------------------------")

        if sentence.strip() == "satzanalyse beenden":
            break
        else:
            allSentences.append(sentence)
            os.system("mpg321 -q /home/pi/Documents/RoboGen-QBO/Python_Projects/EmotionSpeech/mp3/SoundEffect_Confirm.mp3") # Bestätigungs-Sound abspielen
 
    # analysiere und beantworte alle Sätze
    Various_Functions.qboResponse(allSentences)

#---------------------------------------------------------------------------------------------
# MainProgram Start - (entrance point)
#---------------------------------------------------------------------------------------------


# wait for wake word
while True:
    allSentences = []
    sentence = Processing_Audio.getAudioToText()
    sentence = Various_Functions.normalize(sentence)
          
    if sentence.strip() == "satzanalyse starten":
        startEmotionAnalyze()
        processEmotionAnalyze()
            
    elif sentence.strip() == "entscheidungsbaum starten":
        DecisionTrees.startDecisionTree()
        DecisionTrees.processDecisionTree()
            
    


