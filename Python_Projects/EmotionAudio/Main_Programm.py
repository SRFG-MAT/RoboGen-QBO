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

# notif trigger
sys.path.append('/opt/QBO/RoboGen-QBO/Python_Projects/EmotionAudio/not')
import Notif

# saved settings
sys.path.append('/opt/QBO/RoboGen-QBO/Python_Projects/MyQBOSettings')
import SettingsReader

# saved nutrition
sys.path.append('/opt/QBO/RoboGen-QBO/Python_Projects/MyQBOFoodplan')
import FoodManager

# saved and uploaded calendar on server
sys.path.append('/opt/QBO/RoboGen-QBO/Python_Projects/MyQBOCalendar')
import CalendarManager

# use QBOControl File to control Head
sys.path.append('/opt/QBO/RoboGen-QBO/Python_Projects/ControlQBO')
import serial
import QboCmd

port = '/dev/serial0'
ser = serial.Serial(port, baudrate=115200, bytesize = serial.EIGHTBITS, stopbits = serial.STOPBITS_ONE, parity = serial.PARITY_NONE, rtscts = False, dsrdtr =False, timeout = 0)
QBO = QboCmd.Controller(ser)

#---------------------------------------------------------------------------------------------
# ChangeMicrophone: will switch between Arduino QBoards connected MICs
#---------------------------------------------------------------------------------------------
def ChangeMicrophone():
    
    par_list = QBO.GetHeadCmd("GET_MIC_REPORT", 0) # Get mics present RMS values 0 - 32767: 0 - 1V
    if par_list:
        mic1_rms = (par_list[1] << 8 | par_list[0]) / 32767.0
        mic2_rms = (par_list[3] << 8 | par_list[2]) / 32767.0
        mic3_rms = (par_list[5] << 8 | par_list[4]) / 32767.0
        
        #print mic1_rms
        #print mic2_rms
        #print mic3_rms
       
    QBO.GetHeadCmd("SET_MIC_INPUT", 0) # Switch to mic 0/1/2 (or 1/2/3?)

#---------------------------------------------------------------------------------------------
# MainProgram Start - (entrance point)
#---------------------------------------------------------------------------------------------
ChangeMicrophone()

# wait for wake word
while True:
    
    SettingsReader.LoadFromServer()
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

            elif sentence == "benachrichtigung":
                Notif.startNotif(userName,emergencyMail)
                break # break inner endless loop to go back to wakeup word
            
            elif sentence == "roboter umbenennen":
                Various_Functions.qboSpeak('Verstehe! Wie soll mein Name in Zukunft lauten?')
                name = Processing_Audio.getAudioToText()
                name = Various_Functions.normalize(name).strip()
                SettingsReader.renameRobot(name)
                Various_Functions.qboSpeak('OK, gut ab jetzt kannst du mich ' + name + " nennen!")
                break # break inner endless loop to go back to wakeup word
            
            elif sentence == "benutzer umbenennen":
                Various_Functions.qboSpeak('Verstehe! Mit wem spreche ich gerade?')
                name = Processing_Audio.getAudioToText()
                name = Various_Functions.normalize(name).strip()
                SettingsReader.renameUser(name)
                Various_Functions.qboSpeak('OK, ab jetzt werde ich dich ' + name + " nennen!")
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
            
            elif sentence == "nahrung":
                
                Various_Functions.qboSpeak('Verstehe! Was hast du kuerzlich gegessen oder getrunken?')
                food = Processing_Audio.getAudioToText()
                food = Various_Functions.normalize(food).strip()
                
                Various_Functions.qboSpeak('Verstehe! Wieviel hast du davon konsumiert?')
                amount = Processing_Audio.getAudioToText()
                amount = Various_Functions.normalize(amount).strip()
                
                Various_Functions.qboSpeak('Verstehe! Ich werde einen Nahrungseintrag vornehmen! Welches Datum soll eingetragen werden?')
                date = Processing_Audio.getAudioToText()
                date = Various_Functions.normalize(date).strip()
                
                Various_Functions.qboSpeak('Verstehe! Welche Uhrzeit soll eingetragen werden?')
                time = Processing_Audio.getAudioToText()
                time = Various_Functions.normalize(time).strip()
                        
                ret = FoodManager.uploadNutritionEntry(food, date, time, amount)
                FoodManager.downloadNutritionEntry()
                
                if "Server stored entry succesfully" in str(ret): 
                    Various_Functions.qboSpeak('Danke, ich habe das Nahrungsmittel eingetragen!')
                else:
                    Various_Functions.qboSpeak('Entschuldige, aber ich habe dieses Nahrungsmittel nicht gefunden!')   
                
                break # break inner endless loop to go back to wakeup word
            
            elif sentence == "meine nahrung entfernen":
                if FoodManager.resetNutritionDiary():
                    Various_Functions.qboSpeak('Ich habe alle deine Nahrungseintraege fuer dich geloescht!')
                else:
                    Various_Functions.qboSpeak('Hoppla! Das Loeschen der Nahrungseintraege hat offenbar nicht funktioniert!')
                
                break # break inner endless loop to go back to wakeup word
            
            elif sentence == "kalendereintrag":
                
                Various_Functions.qboSpeak('Verstehe! Wie lautet der Titel dieses Kalendereintrages?')
                title = Processing_Audio.getAudioToText()
                title = Various_Functions.normalize(title).strip()
                
                Various_Functions.qboSpeak('Verstehe! Ich werde einen Kalendereintrag vornehmen! Welches Datum soll eingetragen werden?')
                date = Processing_Audio.getAudioToText()
                date = Various_Functions.normalize(date).strip()
                
                Various_Functions.qboSpeak('Verstehe! Welche Uhrzeit soll eingetragen werden?')
                time = Processing_Audio.getAudioToText()
                time = Various_Functions.normalize(time).strip()
                
                Various_Functions.qboSpeak('Verstehe! Wie lange vorher moechtest du an dieses Event erinnert werden?')
                reminder = Processing_Audio.getAudioToText()
                reminder = Various_Functions.normalize(reminder).strip()
                
                Various_Functions.qboSpeak('Verstehe! Wie oft soll dieses Event wiederholt werden?')
                repeat = Processing_Audio.getAudioToText()
                repeat = Various_Functions.normalize(repeat).strip()             
                
                CalendarManager.uploadCalendarEntry(title, date, time, reminder, repeat)                
                CalendarManager.downloadCalendarEntry()
                
                break # break inner endless loop to go back to wakeup word
            
            elif sentence == "kalender entfernen":
                if CalendarManager.resetCalendar():
                    Various_Functions.qboSpeak('Ich habe alle deine Kalendereintraege fuer dich geloescht!')
                else:
                    Various_Functions.qboSpeak('Hoppla! Das Loeschen der Kalendereintraege hat offenbar nicht funktioniert!')
                
                break # break inner endless loop to go back to wakeup word
            
            elif sentence == "schon gut":
                Various_Functions.qboSpeak('Wenn du was brauchst ich bin hier.')
                break
            
            else:
                Various_Functions.qboSpeak('Ich habe dich leider nicht gut verstanden.')
                break
    


