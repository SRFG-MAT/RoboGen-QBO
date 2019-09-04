# coding=utf-8

from Emotion_Dictionary import emo_dic
from Emotion_Dictionary import emo_changers
from string import punctuation
from fuzzywuzzy import fuzz
import os

def talkEmotionToMe(emotion):
    if emotion.lower() == 'gluecklich':
        os.system("mpg321 gluecklich.mp3")
    elif emotion.lower() == 'wut':
        os.system("mpg321 wut.mp3")
    elif emotion.lower() == 'ekel':
        os.system("mpg321 eckel.mp3")
    elif emotion.lower() == 'ueberrascht':
        os.system("mpg321 ueberrascht.mp3")
    elif emotion.lower() == 'traurig':
        os.system("mpg321 trauer.mp3")
    else:
        os.system("mpg321 angst.mp3")

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
    #print(highscore_word)
    #print(highscore_emotion)
    #print(highscore)
    return highscore_emotion


def checkNegation(sentence, emotion):
    words = sentence.split()

    for word in words:
        for neg in emo_changers["Negators"]:
            if word == neg:

                if emotion.lower() == 'gluecklich':
                    emotion = 'Trauer'
                elif emotion.lower() == 'wut':
                    emotion = 'Angst'
                elif emotion.lower() == 'ekel':
                    emotion = 'Gluecklich'
                elif emotion.lower() == 'ueberrascht':
                    emotion = 'Gluecklich'
                elif emotion.lower() == 'trauer':
                    emotion = 'Gluecklich'
                else:
                    emotion = 'Wut'

    return emotion



def normalize(sentence):
    for p in punctuation:
        sentence = sentence.replace(p, '')

    return sentence.lower()