#!/usr/bin/env python
# coding=utf-8
import os, sys, time
import Processing_Audio
import Various_Functions

import imp

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

# saved nutrition
sys.path.append('/opt/QBO/RoboGen-QBO/Python_Projects/MyQBOFoodplan')
import FoodReader

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
            
            elif sentence == "lauter":
                SettingsReader.incrementRobotAudioVolume()
                imp.reload(Various_Functions) # To show updated JSON
                Various_Functions.qboSpeak('Verstehe! Ich spreche dir wohl zu leise? Von jetzt an spreche ich lauter!')
                break # break inner endless loop to go back to wakeup word
                
            elif sentence == "leiser":
                SettingsReader.decrementRobotAudioVolume()
                imp.reload(Various_Functions) # To show updated JSON
                Various_Functions.qboSpeak('Verstehe! Ich spreche dir wohl zu laut? Von jetzt an spreche ich leiser!')
                break # break inner endless loop to go back to wakeup word 
            
            elif sentence == "nahrungsaufnahme":
                Various_Functions.qboSpeak('Verstehe! Was hast du kuerzlich gegessen oder getrunken?')
                
                food = Processing_Audio.getAudioToText()
                food = Various_Functions.normalize(food).strip()
                
                entries = FoodReader.searchFoodArray(food)
                if not entries:
                    Various_Functions.qboSpeak('Tut mir Leid, leider konnte ich dieses Nahrungsmittel in meiner Datenbank nicht finden!')
                else:
                    FoodReader.createCalendarEntry(entries[0])
                    Various_Functions.qboSpeak('OK, ich habe das Nahrungsmittel' + entries[0] + 'deinem Ernaehrungstagebuch mit dem heutigen Datum hinzugefuegt!')      
                
                break # break inner endless loop to go back to wakeup word 
            
            elif sentence == "schon gut":
                Various_Functions.qboSpeak('Wenn du was brauchst ich bin hier.')
                break
            
            else:
                Various_Functions.qboSpeak('Ich habe dich leider nicht gut verstanden.')
                break
    


