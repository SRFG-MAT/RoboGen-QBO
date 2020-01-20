#!/usr/bin/env python
# coding=utf-8

import sys
import Processing_Audio
from string import punctuation
from gtts import gTTS 
import os

#---------------------------------------------------------------------------------------------
# qboSpeak - QBO will speak the sentence out loudly
#---------------------------------------------------------------------------------------------
def qboSpeak(sentence):
    
    language = 'de' # Sprache (ISO Code)
    myobj = gTTS(text=sentence, lang=language, slow=False) # Erzeugen der Sprachausgabe
    myobj.save("/home/pi/Documents/RoboGen-QBO/Python_Projects/EmotionSpeech/mp3/tmp.mp3") # Speichern als mp3
    os.system("mpg321 -q /home/pi/Documents/RoboGen-QBO/Python_Projects/EmotionSpeech/mp3/tmp.mp3")
    
#---------------------------------------------------------------------------------------------
# normalize - (needed for processing Google String)
#---------------------------------------------------------------------------------------------
def normalize(sentence):
    
    for p in punctuation:
        sentence = sentence.replace(p, '')

    return sentence.lower()


#---------------------------------------------------------------------------------------------
# MainProgram Start - (entrance point)
#---------------------------------------------------------------------------------------------
while True:

    # warte auf wake word
    while True:
        sentence = Processing_Audio.getAudioToText()
        sentence = normalize(sentence)
        
        qboSpeak('Hallo, mein Name ist QBO! Du hast die Entscheidungsbaume gestartet!')
    
        if sentence.strip() == "starte entscheidungsbaum":
            break

    # sammle alle Sätze zusammen
    while True:
    
        print("------------------------------------------------------")
        print("Jetzt sprechen um einen Satz aufzuzeichnen!")
        print("------------------------------------------------------")
    
        sentence = Processing_Audio.getAudioToText()
        sentence = normalize(sentence)
        
        print("------------------------------------------------------")
        print("Google Speech Recognition glaubt du sagst: \n" + sentence)
        print("------------------------------------------------------")

        #if sentence.strip() == "entscheidungsbaum beenden":
        #    break
        #else:
        #    os.system("mpg321 -q /home/pi/Documents/RoboGen-QBO/Python_Projects/EmotionSpeech/mp3/SoundEffect_Confirm.mp3") # Bestätigungs-Sound abspielen


