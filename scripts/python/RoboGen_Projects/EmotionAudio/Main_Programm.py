#!/usr/bin/env python
# coding=utf-8
import os, sys, time
import Processing_Audio
import Various_Functions

import imp

from datetime import datetime
from datetime import date

# decision trees
sys.path.append('/opt/QBO/catkin_ws/src/RoboGen-QBO/scripts/python/RoboGen_Projects/EmotionAudio/dt')
import DecisionTrees

# emotion analysis
sys.path.append('/opt/QBO/catkin_ws/src/RoboGen-QBO/scripts/python/RoboGen_Projects/EmotionAudio/ea')
import EmotionAnalysis

# emergency trigger
sys.path.append('/opt/QBO/catkin_ws/src/RoboGen-QBO/scripts/python/RoboGen_Projects/EmotionAudio/em')
import Emergency

# notif trigger
sys.path.append('/opt/QBO/catkin_ws/src/RoboGen-QBO/scripts/python/RoboGen_Projects/EmotionAudio/not')
import Notif

# saved settings
sys.path.append('/opt/QBO/catkin_ws/src/RoboGen-QBO/scripts/python/RoboGen_Projects/MyQBOSettings')
import SettingsReader

# saved nutrition
sys.path.append('/opt/QBO/catkin_ws/src/RoboGen-QBO/scripts/python/RoboGen_Projects/MyQBOFoodplan')
import FoodManager

# saved and uploaded calendar on server
sys.path.append('/opt/QBO/catkin_ws/src/RoboGen-QBO/scripts/python/RoboGen_Projects/MyQBOCalendar')
import CalendarManager

# use QBOControl File to control Head
sys.path.append('/opt/QBO/catkin_ws/src/RoboGen-QBO/scripts/python/RoboGen_Projects/ControlQBO')
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
SettingsReader.LoadFromServer()

QBO.SetMouth(0x1b1f0e04)
QBO.SetMouth(0x1b1f0e04)
QBO.SetNoseColor(QboCmd.nose_color_green) # init nose
QBO.SetNoseColor(QboCmd.nose_color_green) # init nose

# wait for wake word
while True:
    
    try:
    
        #SettingsReader.LoadFromServer()
        robotName = SettingsReader.getRobotNameFromSettings().lower().strip()
        userName = SettingsReader.getUserName()
        emergencyMail = SettingsReader.getEmergencyEmail().lower().strip()
        sentence = Processing_Audio.getAudioToText()
        sentence = Various_Functions.normalize(sentence).strip()
    
        if sentence == robotName:
        
            SettingsReader.LoadFromServer()
        
            Various_Functions.qboSpeak('Ja?')
        
            # wait for command
            while True:
            
                sentence = Processing_Audio.getAudioToText()
                sentence = Various_Functions.normalize(sentence).strip()
            
                if sentence == "dialog":
                    DecisionTrees.startDecisionTree(False)
                    #DecisionTrees.processDecisionTree()
                    break # break inner endless loop to go back to wakeup word
            
                #elif sentence == "satzanalyse":
                #    EmotionAnalysis.startEmotionAnalyze(robotName)
                #    EmotionAnalysis.processEmotionAnalyze()
                #    break # break inner endless loop to go back to wakeup word

                #elif sentence == "notfall":
                #    Emergency.startEmergency(userName,emergencyMail)
                #    break # break inner endless loop to go back to wakeup word

                elif sentence == "nachricht":
                    Notif.startNotif(userName,emergencyMail)
                    break # break inner endless loop to go back to wakeup word
            
                #elif sentence == "roboter umbenennen":
                #    Various_Functions.qboSpeak('Verstehe! Wie soll mein Name in Zukunft lauten?')
                #    name = Processing_Audio.getAudioToText()
                #    name = Various_Functions.normalize(name).strip()
                #    SettingsReader.renameRobot(name)
                #    Various_Functions.qboSpeak('OK, ab jetzt kannst du mich ' + name + " nennen!")
                #    break # break inner endless loop to go back to wakeup word
                
                #elif sentence == "benutzer umbenennen":
                #    Various_Functions.qboSpeak('Verstehe! Mit wem spreche ich gerade?')
                #    name = Processing_Audio.getAudioToText()
                #    name = Various_Functions.normalize(name).strip()
                #    SettingsReader.renameUser(name)
                #    Various_Functions.qboSpeak('OK, ab jetzt werde ich dich ' + name + " nennen!")
                #    break # break inner endless loop to go back to wakeup word
                
                elif sentence == "lauter":
                    SettingsReader.incrementRobotAudioVolume()
                    imp.reload(Various_Functions) # To show updated JSON
                    Various_Functions.qboSpeak('Verstehe! Ich spreche dir wohl zu leise. Von jetzt an spreche ich lauter!')
                    break # break inner endless loop to go back to wakeup word
                
                elif sentence == "leiser":
                    SettingsReader.decrementRobotAudioVolume()
                    imp.reload(Various_Functions) # To show updated JSON
                    Various_Functions.qboSpeak('Verstehe! Ich spreche dir wohl zu laut. Von jetzt an spreche ich leiser!')
                    break # break inner endless loop to go back to wakeup word 
                
                elif sentence == "mahlzeit":

                    Various_Functions.qboSpeak('Verstehe! Was hast du kuerzlich gegessen oder getrunken?')
                    food = Processing_Audio.getAudioToText()
                    food = Various_Functions.normalize(food).strip()

                    Various_Functions.qboSpeak('Wieviel hast du davon konsumiert?')
                    amount = Processing_Audio.getAudioToText()
                    amount = Various_Functions.normalize(amount).strip()

                    #Various_Functions.qboSpeak('Verstehe! Ich werde einen Nahrungseintrag vornehmen! Welches Datum soll eingetragen werden?')
                    #d1 = Processing_Audio.getAudioToText()
                    #d1 = Various_Functions.normalize(1).strip()

                    #Various_Functions.qboSpeak('Verstehe! Welche Uhrzeit soll eingetragen werden?')
                    #t1 = Processing_Audio.getAudioToText()
                    #t1 = Various_Functions.normalize(time).strip()

                    now = datetime.now()
                    d1 = now.strftime("%Y-%m-%d")
                    t1 = now.strftime("%H:%M")
                            
                    ret = FoodManager.uploadNutritionEntry(food, d1, t1, amount)
                    #FoodManager.downloadNutritionEntry()
                    
                    Various_Functions.qboSpeak('Danke, ich habe die Mahlzeit gespeichert! Du kannst deine Eintraege am Tablet aufrufen und aendern.')  
                    
                    break # break inner endless loop to go back to wakeup word
            
                #elif sentence == "mahlzeit entfernen":
                #    if FoodManager.resetNutritionDiary():
                #        Various_Functions.qboSpeak('Ich habe alle deine Nahrungseintraege fuer dich geloescht!')
                #    else:
                #        Various_Functions.qboSpeak('Hoppla! Das Loeschen der Nahrungseintraege hat offenbar nicht funktioniert!')
                #    
                #    break # break inner endless loop to go back to wakeup word
                
                elif sentence == "kalender":
                    
                    Various_Functions.qboSpeak('Verstehe! Wie lautet der Titel des Kalendereintrages?')
                    title = Processing_Audio.getAudioToText()
                    title = Various_Functions.normalize(title).strip()
                    
                    Various_Functions.qboSpeak('Welches Datum soll eingetragen werden?')
                    date = Processing_Audio.getAudioToText()
                    date = Various_Functions.normalize(date).strip()
                    
                    Various_Functions.qboSpeak('Welche Uhrzeit soll eingetragen werden?')
                    time = Processing_Audio.getAudioToText()
                    time = Various_Functions.normalize(time).strip()
                
                    #Various_Functions.qboSpeak('Verstehe! Wie lange vorher moechtest du an dieses Ereignis erinnert werden?')
                    #reminder = Processing_Audio.getAudioToText()
                    #reminder = Various_Functions.normalize(reminder).strip()
                    reminder = "0"
                    
                    #Various_Functions.qboSpeak('Verstehe! Wie oft soll dieses Ereignis wiederholt werden?')
                    #repeat = Processing_Audio.getAudioToText()
                    #repeat = Various_Functions.normalize(repeat).strip()
                    repeat = "0"
                    
                    CalendarManager.uploadCalendarEntry(title, date, time, reminder, repeat)                
                    #CalendarManager.downloadCalendarEntry()
                    
                    Various_Functions.qboSpeak('Danke, ich habe das Ereignis gespeichert! Du kannst deine Eintraege am Tablet aufrufen und aendern.')
                    
                    break # break inner endless loop to go back to wakeup word
                
                #elif sentence == "kalender entfernen":
                #    if CalendarManager.resetCalendar():
                #        Various_Functions.qboSpeak('Ich habe alle deine Kalendereintraege fuer dich geloescht!')
                #    else:
                #        Various_Functions.qboSpeak('Hoppla! Das Loeschen der Kalendereintraege hat offenbar nicht funktioniert!')
                #    
                #    break # break inner endless loop to go back to wakeup word

                elif sentence == "energie batterie":
                    Various_Functions.qboSpeak('Die Energie Batterie findest du am Tablet.')
                    break

                elif sentence == "schlafdaten":
                    Various_Functions.qboSpeak('Die Schlafdaten findest du am Tablet.')
                    break
                
                elif sentence == "schon gut":
                    Various_Functions.qboSpeak('Wenn du was brauchst, ich bin hier.')
                    break
                
                else:
                    Various_Functions.qboSpeak('Ich habe dich leider nicht gut verstanden. Bitte wiederhole dein Kommando.')
            
    
    except KeyboardInterrupt:
        QBO.SetMouth(0x00000000)
        QBO.SetMouth(0x00000000)
        QBO.SetNoseColor(QboCmd.nose_color_none)
        QBO.SetNoseColor(QboCmd.nose_color_none)
        print("exit")
        sys.exit()

