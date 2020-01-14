# coding=utf-8

import sys
import Various_Functions
import Processing_Audio
import os

#---------------------------------------------------------------------------------------------
# MainProgram Start - (entrance point)
#---------------------------------------------------------------------------------------------
while True:

    allSentences = []

    # warte auf wake word
    while True:
        sentence = Processing_Audio.getAudioToText()
        sentence = Various_Functions.normalize(sentence)
        
        print("------------------------------------------------------")
        print("Google Speech Recognition glaubt du sagst: \n" + sentence)
        print("------------------------------------------------------")
    
        if sentence.strip() == "aufzeichnung starten":
            break

    # sammle alle Sätze zusammen
    while True:
    
        print("------------------------------------------------------")
        print("Jetzt sprechen um einen Satz aufzuzeichnen!")
        print("------------------------------------------------------")
    
        sentence = Processing_Audio.getAudioToText()
        sentence = Various_Functions.normalize(sentence)
        
        print("------------------------------------------------------")
        print("Google Speech Recognition glaubt du sagst: \n" + sentence)
        print("------------------------------------------------------")

        if sentence.strip() == "aufzeichnung beenden":
            break
        else:
            allSentences.append(sentence)
 
    # analysiere und beantworte alle Sätze
    Various_Functions.qboResponse(allSentences)


