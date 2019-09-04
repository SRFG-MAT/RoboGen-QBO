# coding=utf-8

import speech_recognition as sr

def getAudioToText():
    r = sr.Recognizer()

    while True:
        with sr.Microphone() as source:
            print("Sprich zu mir!")
            audio = r.listen(source)

        try:
            sentence = r.recognize_google(audio, language="de")
            print("Google Speech Recognition glaubt du sagst: " + sentence)
            return sentence
        except sr.UnknownValueError:
            print("Google Speech Recognition konnte dich leider nicht verstehen")
        except sr.RequestError as e:
            print("Konnte kein Ergebniss von Google Speech Recognition erhalten; {0}".format(e))