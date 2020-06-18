#!/usr/bin/env python
# coding=utf-8
import os, sys
from gtts import gTTS 

# from emotion analysis
sys.path.append('/opt/QBO/RoboGen-QBO/Python_Projects/EmotionAudio/ea')
from Emotion_Dictionary import emo_dic
from Emotion_Dictionary import emo_changers
from string import punctuation
from fuzzywuzzy import fuzz

# from Settings
sys.path.append('/opt/QBO/RoboGen-QBO/Python_Projects/MyQBOSettings')
import SettingsReader
audioVolume = SettingsReader.getRobotAudioVolume()
audioVoice = SettingsReader.getRobotAudioVoice()

#for pydub audio modification
#from urllib2 import urlopen
from pydub import AudioSegment
from pydub.playback import play

# global variables
filepath_tmp_audio = "/opt/QBO/RoboGen-QBO/Python_Projects/EmotionAudio/mp3/tmp.mp3"


#---------------------------------------------------------------------------------------------
# modify gtts mp3 volume
#---------------------------------------------------------------------------------------------
def modifyAudioVolume(sound):
    return sound + (audioVolume-50)

#---------------------------------------------------------------------------------------------
# modify gtts mp3 pitch voice
#---------------------------------------------------------------------------------------------
def modifyAudioPitchVoice(sound):
    
    if (audioVoice == 1):  # Männlich - Markus
        new_sample_rate = int(sound.frame_rate * (2.0 ** -1.5)) #octaves = -1.5
        return sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate})
    
    elif (audioVoice == 2):  # Männlich - Gustav
        new_sample_rate = int(sound.frame_rate * (2.0 ** -0.5)) #octaves = -0.5
        return sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate})
    
    elif (audioVoice == 3):  # Weiblich - Anita
        new_sample_rate = int(sound.frame_rate * (2.0 ** +0.5)) #octaves = +0.5
        return sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate})
    
    elif (audioVoice == 4):  # Weiblich - Arabella
        new_sample_rate = int(sound.frame_rate * (2.0 ** +1.5)) #octaves = +1.5
        return sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate})
    
    elif (audioVoice == 5):  #Geschlechtsneutral
        new_sample_rate = int(sound.frame_rate * (2.0 ** -3.5)) #octaves = -3.5
        return sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate})
    
    else: # std voice (0)
        return sound   

#---------------------------------------------------------------------------------------------
# qboSpeak - QBO will speak the sentence out loudly
#---------------------------------------------------------------------------------------------
def qboSpeak(sentence):
    
    # Erzeugen der Sprachausgabe und speichern als mp3
    myobj = gTTS(text=sentence, lang='de', slow=False) 
    myobj.save(filepath_tmp_audio)
    
    # Nachbearbeitung der mp3-Datei mit pydub
    sound = AudioSegment.from_mp3(filepath_tmp_audio)
    play(modifyAudioPitchVoice(modifyAudioVolume(sound)))
    
    #os.system("mpg321 -q " + filepath_tmp_audio + " --gain " + str(audioVolume))

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


