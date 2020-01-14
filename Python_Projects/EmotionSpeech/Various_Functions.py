# coding=utf-8

from Emotion_Dictionary import emo_dic
from Emotion_Dictionary import emo_changers
from string import punctuation
from fuzzywuzzy import fuzz
from gtts import gTTS 
import os

#---------------------------------------------------------------------------------------------
# qboSpeak - QBO will speak the sentence out loudly
#---------------------------------------------------------------------------------------------
def qboSpeak(sentence):
    
    language = 'de' # Sprache (ISO Code)
    myobj = gTTS(text=sentence, lang=language, slow=False) # Erzeugen der Sprachausgabe
    myobj.save("./mp3/tmp.mp3") # Speichern als mp3
    os.system("mpg321 -q ./mp3/tmp.mp3")

#---------------------------------------------------------------------------------------------
# qboResponse - analyzes all given sentences in sentenceArray and will answer them
#---------------------------------------------------------------------------------------------
def qboResponse(allSentences):
    
    for sentence in allSentences:
  
        qboSpeak('Ich habe folgenden Satz gehoert: ' + sentence)
    
        emotion, highscore_word, highscore_value = getHighestScoreEmotion(sentence)
        emotion = checkNegation(sentence, emotion) # Funktion für Negierung
    
        if emotion.lower() == 'gluecklich':
            qboSpeak('Ich habe diesen Satz fuer dich analysiert und glaube, du bist gluecklich!')
        elif emotion.lower() == 'wut':
            qboSpeak('Ich habe diesen Satz fuer dich analysiert und glaube, du bist wuetend!')
        elif emotion.lower() == 'ekel':
            qboSpeak('Ich habe diesen Satz fuer dich analysiert und glaube, du bist angewidert!')
        elif emotion.lower() == 'ueberrascht':
            qboSpeak('Ich habe diesen Satz fuer dich analysiert und glaube, du bist ueberrascht worden!')
        elif emotion.lower() == 'traurig':
            qboSpeak('Ich habe diesen Satz fuer dich analysiert und glaube, du bist traurig!')
        elif emotion.lower() == 'angst':
            qboSpeak('Ich habe diesen Satz fuer dich analysiert und glaube, du bist angsterfuellt!')
        else:
            qboSpeak('Ich habe diesen Satz fuer dich analysiert, aber ich konnte deine Emotion leider nicht richtig zuordnen!')
        
        qboSpeak('Der erzielte Highscore von %s Punkten wurde hauptsaechlich durch das enthaltene Wort %s hervorgerufen!' % (highscore_value, highscore_word))    

    qboSpeak("Das waren alle Saetze, die ich verstanden habe. Ich wuensche dir einen schoenen Tag!")

#---------------------------------------------------------------------------------------------
# getEmotion - (get Emotion from a sentence)
#---------------------------------------------------------------------------------------------
def getHighestScoreEmotion(sentence):
    
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
    
    return highscore_emotion, highscore_word, str(highscore)


#---------------------------------------------------------------------------------------------
# checkNegation - (find negetaion in sentence)
#---------------------------------------------------------------------------------------------
def checkNegation(sentence, emotion):
    
    words = sentence.split()

    for word in words:
        for neg in emo_changers["Negators"]:
            if word == neg:
                
                qboSpeak("Ein negierendes Wort wurde im Satzbau entdeckt!")

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


