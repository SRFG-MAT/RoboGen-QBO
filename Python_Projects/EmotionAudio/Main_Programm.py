#!/usr/bin/env python
# coding=utf-8
import os, sys, time
import Processing_Audio
import Various_Functions

# decision trees
sys.path.append('/opt/QBO/RoboGen-QBO/Python_Projects/EmotionAudio/dt')
import DecisionTrees

# emotion analysis
sys.path.append('/opt/QBO/RoboGen-QBO/Python_Projects/EmotionAudio/ea')
import EmotionAnalysis

# emergency trigger
sys.path.append('/opt/QBO/RoboGen-QBO/Python_Projects/EmotionAudio/em')
import Emergency

# saved settings
sys.path.append('/opt/QBO/RoboGen-QBO/Python_Projects/MyQBOSettings')
import SettingsReader

#---------------------------------------------------------------------------------------------
# MainProgram Start - (entrance point)
#---------------------------------------------------------------------------------------------
# wait for wake word
while True:
    
	robotName = SettingsReader.getRobotNameFromSettings().lower().strip()
	userName = SettingsReader.getUserName()
	emergencyMail = SettingsReader.getEmergencyEmail().lower().strip()
    sentence = Processing_Audio.getAudioToText()
    sentence = Various_Functions.normalize(sentence).strip()   
    
    if sentence == robotName:
        
        Various_Functions.qboSpeak('Ja?')
        
        # wait for command
        while True:
            
            sentence = Processing_Audio.getAudioToText()
            sentence = Various_Functions.normalize(sentence).strip()
          
            if sentence == "starte satzanalyse":
                EmotionAnalysis.startEmotionAnalyze(robotName)
                EmotionAnalysis.processEmotionAnalyze()
                break # break inner endless loop to go back to wakeup word
            
            elif sentence == "starte entscheidungsbaum":
                DecisionTrees.startDecisionTree(robotName)
                DecisionTrees.processDecisionTree()
                break # break inner endless loop to go back to wakeup word
				
			elif sentence == "notfall":
				Emergency.startEmergency(userName,emergencyMail)
				break # break inner endless loop to go back to wakeup word
            
            elif sentence == "schon gut":
                Various_Functions.qboSpeak('Wenn du was brauchst ich bin hier.')
                break
            
            else:
                Various_Functions.qboSpeak('Ich habe dich leider nicht gut verstanden.')
                break
    


