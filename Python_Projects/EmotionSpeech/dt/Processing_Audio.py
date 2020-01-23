#!/usr/bin/env python
# coding=utf-8

import speech_recognition as sr

#---------------------------------------------------------------------------------------------
# getAudioToText - (use Google lib to get microphone input as text)
#---------------------------------------------------------------------------------------------
def getAudioToText():
    recognizer = sr.Recognizer()

    while True:
        
        with sr.Microphone() as source:          
            
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        try:
            sentence = recognizer.recognize_google(audio, language="de-AT")
            
            print("------------------------------------------------------")
            print("Google Speech Recognition glaubt du sagst: \n" + sentence)
            print("------------------------------------------------------")
            
            return sentence
        
        except sr.UnknownValueError:
            print("------------------------------------------------------")
            print("Die Sprachaufzeichnung konnte dich leider nicht verstehen")
            print("------------------------------------------------------")
        except sr.RequestError as e:
            print("------------------------------------------------------")
            print("Konnte kein Ergebnis von Google erhalten; {0}".format(e))
            print("------------------------------------------------------")