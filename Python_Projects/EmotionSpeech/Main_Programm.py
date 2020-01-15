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
        
        Various_Functions.qboSpeak('Hallo, mein Name ist QBO! Erzaehl mir etwas und ich werde versuchen deinen Satz zu verstehen und zu analysieren!')
        Various_Functions.qboSpeak('Bei meiner Analyse gehe ich vor Allem auf deine Gefuehle ein! Dazu sehe ich mir an, wie du deinen Satz formuliert hast.')
        Various_Functions.qboSpeak('Probier es aus! Sag mir ein paar Saetze und wenn du fertig bist sag: Aufzeichnung beenden!')
        Various_Functions.qboSpeak('Danach gehen wir deine Saetze gemeinsam durch! Hoffen wir mal ich schaffe es, die Saetze richtig zu deuten! Los gehts!')
    
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
            os.system("mpg321 -q ./mp3/SoundEffect_Confirm.mp3") # Bestätigungs-Sound abspielen
 
    # analysiere und beantworte alle Sätze
    Various_Functions.qboResponse(allSentences)


