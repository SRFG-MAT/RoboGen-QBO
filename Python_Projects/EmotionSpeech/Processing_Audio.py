# coding=utf-8

import speech_recognition as sr

def getAudioToText():
    r = sr.Recognizer()

    while True:
        with sr.Microphone() as source:
            print("------------------------------------------------------")
            print("Sprich zu mir!")
            print("------------------------------------------------------")
            audio = r.listen(source)

        try:
            sentence = r.recognize_google(audio, language="de")
            print("------------------------------------------------------")
            print("Google Speech Recognition glaubt du sagst: \n" + sentence)
            print("------------------------------------------------------")
            return sentence
        except sr.UnknownValueError:
            print("------------------------------------------------------")
            print("Google Speech Recognition konnte dich leider nicht verstehen")
            print("------------------------------------------------------")
        except sr.RequestError as e:
            print("------------------------------------------------------")
            print("Konnte kein Ergebniss von Google Speech Recognition erhalten; {0}".format(e))
            print("------------------------------------------------------")