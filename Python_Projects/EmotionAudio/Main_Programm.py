#!/usr/bin/env python
# coding=utf-8
import os, sys, time
import Processing_Audio
import Various_Functions

# decision trees
sys.path.append('/home/pi/Documents/RoboGen-QBO/Python_Projects/EmotionAudio/dt')
import DecisionTrees

# emotion analysis
sys.path.append('/home/pi/Documents/RoboGen-QBO/Python_Projects/EmotionAudio/ea')
import EmotionAnalysis

# saved settings
sys.path.append('/home/pi/Documents/RoboGen-QBO/Python_Projects/MyQBOSettings')
import SettingsReader
robotName = SettingsReader.getRobotNameFromSettings().lower()


#---------------------------------------------------------------------------------------------
# MainProgram Start - (entrance point)
#---------------------------------------------------------------------------------------------
# wait for wake word
while True:
    
    sentence = Processing_Audio.getAudioToText()
    sentence = Various_Functions.normalize(sentence)
    
    if sentence.strip() == robotName.strip():
        
        Various_Functions.qboSpeak('Ja?')
        
        # wait for command
        while True:
            
            sentence = Processing_Audio.getAudioToText()
            sentence = Various_Functions.normalize(sentence)
          
            if sentence.strip() == "starte satzanalyse":
                EmotionAnalysis.startEmotionAnalyze(robotName)
                EmotionAnalysis.processEmotionAnalyze()
                break # break inner endless loop to go back to wakeup word
            
            elif sentence.strip() == "starte entscheidungsbaum":
                DecisionTrees.startDecisionTree(robotName)
                DecisionTrees.processDecisionTree()
                break # break inner endless loop to go back to wakeup word
            
            elif sentence.strip() == "schon gut":
                Various_Functions.qboSpeak('Wenn du was brauchst ich bin hier.')
                break
            
            else:
                Various_Functions.qboSpeak('Ich habe dich leider nicht gut verstanden.')
                break
    


