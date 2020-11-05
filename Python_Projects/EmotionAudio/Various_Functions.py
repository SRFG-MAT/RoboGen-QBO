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

#for pydub audio modification
#from urllib2 import urlopen
from pydub import AudioSegment
from pydub.playback import play

# global variables
filepath_tmp_audio = "/opt/QBO/RoboGen-QBO/Python_Projects/EmotionAudio/mp3/tmp.mp3"

voice_profile_markus = 1 # Männlich - Markus
markus_speed = 2.0
markus_octaves = -0.5
markus_velocidad_X = 1.5 # speedup

voice_profile_gustav = 2 # Männlich - Gustav
gustav_speed = 2.0
gustav_octaves = -0.25
gustav_velocidad_X = 1.2 # speedup

voice_profile_anita = 3 # Weiblich - Anita
anita_speed = 2.0
anita_octaves = +0.25

voice_profile_arabella = 4 # Weiblich - Arabella
arabella_speed = 2.0
arabella_octaves = +0.5

voice_profile_neutral = 5 # Geschlechtsneutral
neutral_speed = 2.2
neutral_octaves = +0.3


#---------------------------------------------------------------------------------------------
# modify gtts mp3 volume
#---------------------------------------------------------------------------------------------
def modifyAudioVolume(sound):
    return sound + (SettingsReader.getRobotAudioVolume() - 50)

#---------------------------------------------------------------------------------------------
# modify gtts mp3 pitch voice
#---------------------------------------------------------------------------------------------
def modifyAudioPitchVoice(sound):
    
    audioVoice = SettingsReader.getRobotAudioVoice()
    
    if (audioVoice == voice_profile_markus):  
        new_sample_rate = int(sound.frame_rate * (markus_speed ** markus_octaves)) 
        sound = sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate})
        return sound.speedup(markus_velocidad_X, 150, 25)
    
    elif (audioVoice == voice_profile_gustav):  
        new_sample_rate = int(sound.frame_rate * (gustav_speed ** gustav_octaves)) 
        sound = sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate})
        return sound.speedup(gustav_velocidad_X, 150, 25)
    
    elif (audioVoice == voice_profile_anita):  
        new_sample_rate = int(sound.frame_rate * (anita_speed ** anita_octaves)) 
        return sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate})
    
    elif (audioVoice == voice_profile_arabella):  
        new_sample_rate = int(sound.frame_rate * (arabella_speed ** arabella_octaves)) 
        return sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate})
    
    elif (audioVoice == voice_profile_neutral):  
        new_sample_rate = int(sound.frame_rate * (neutral_speed ** neutral_octaves))
        return sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate})
    
    else: # std voice (0)
        return sound   

#---------------------------------------------------------------------------------------------
# qboSpeak - QBO will speak the sentence out loudly
#---------------------------------------------------------------------------------------------
def qboSpeak(sentence):
    
    #update load settings config from server to see if any changes
    SettingsReader.LoadFromServer()
    
    # Erzeugen der Sprachausgabe und speichern als mp3
    tts = gTTS(text=sentence, lang='de', slow=False)
    tts.save(filepath_tmp_audio)
    
    # Nachbearbeitung der mp3-Datei mit pydub und Audio-Ausgabe
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


