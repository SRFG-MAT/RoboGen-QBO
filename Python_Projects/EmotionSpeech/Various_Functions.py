# coding=utf-8

from Emotion_Dictionary import emo_dic
from Emotion_Dictionary import emo_changers
from string import punctuation
from fuzzywuzzy import fuzz
import os

#---------------------------------------------------------------------------------------------
# talkEmotionToMe - (output mp3 audio file)
#---------------------------------------------------------------------------------------------
def talkEmotionToMe(emotion):
    print ("spiele: " + emotion)
    
    if emotion.lower() == 'gluecklich':
        os.system("mpg321 ./mp3/Play_Gluecklich.mp3")
    elif emotion.lower() == 'wut':
        os.system("mpg321 ./mp3/Play_Wut.mp3")
    elif emotion.lower() == 'ekel':
        os.system("mpg321 ./mp3/Play_Eckel.mp3")
    elif emotion.lower() == 'ueberrascht':
        os.system("mpg321 ./mp3/Play_Ueberrascht.mp3")
    elif emotion.lower() == 'traurig':
        os.system("mpg321 ./mp3/Play_Trauer.mp3")
    elif emotion.lower() == 'angst':
        os.system("mpg321 ./mp3/Play_Angst.mp3")
    else:
        print("Es konnte keine MP3-Date gefunden werden, die zu der eingegebenen Emotion passt")


#---------------------------------------------------------------------------------------------
# getEmotion - (get Emotion from a sentence)
#---------------------------------------------------------------------------------------------
def getEmotion(sentence):
    
    words = sentence.split()
    highscore = 0
    highscore_emotion = ''
    highscore_word = ''
    
    for word in words:
        for emotion in emo_dic: #for Emotion in Wörterbuch
            for feeling in emo_dic[emotion]: #for Wort in Emotion
                value = fuzz.ratio(word, feeling)
                if highscore < value:
                    highscore = value
                    highscore_emotion = emotion
                    highscore_word = word
                    
    # Folgende drei prints sind nur zur ueberpruefung da
    print(highscore_word + "\n" + highscore_emotion + "\n" + str(highscore) + "\n")
    
    return highscore_emotion


#---------------------------------------------------------------------------------------------
# checkNegation - (find negetaion in sentence)
#---------------------------------------------------------------------------------------------
def checkNegation(sentence, emotion):
    
    words = sentence.split()

    for word in words:
        for neg in emo_changers["Negators"]:
            if word == neg:
                
                print("Negierendes Wort entdeckt für " + emotion.lower())

                if emotion.lower() == 'gluecklich':
                    emotion = 'Traurig'
                elif emotion.lower() == 'wut':
                    emotion = 'Gluecklich'
                elif emotion.lower() == 'ekel':
                    emotion = 'Gluecklich'
                elif emotion.lower() == 'ueberrascht':
                    emotion = 'Gluecklich'
                elif emotion.lower() == 'traurig':
                    emotion = 'Gluecklich'
                elif emotion.lower() == 'angst':
                    emotion = 'Gluecklich'
                else:
                    print("Die zu negierende Emotion konnte nicht gefunden werden")

    return emotion


#---------------------------------------------------------------------------------------------
# normalize - (needed for processing Google String)
#---------------------------------------------------------------------------------------------
def normalize(sentence):
    
    for p in punctuation:
        sentence = sentence.replace(p, '')

    return sentence.lower()


