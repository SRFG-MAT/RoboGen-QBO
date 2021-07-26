#!/usr/bin/env python
# coding=utf-8
import os, sys, time, json

# audio
sys.path.append('/opt/QBO/catkin_ws/src/RoboGen-QBO/scripts/python/RoboGen_Projects/EmotionAudio')
import Processing_Audio
import Various_Functions

# saved settings
sys.path.append('/opt/QBO/catkin_ws/src/RoboGen-QBO/scripts/python/RoboGen_Projects/MyQBOSettings')
import SettingsReader

sleepThreshold = SettingsReader.getSleepThreshold()
sleepMinValue = SettingsReader.getSleepMinValue()
#calendar = SettingsReader.getCalendar()
firstRun = 0
calendarTriggered = 0
launch = time.time()

#---------------------------------------------------------------------------------------------
# MainProgram Start - (entrance point)
#---------------------------------------------------------------------------------------------
while True:

	#robotName = SettingsReader.getRobotNameFromSettings().lower().strip()
	#newSleepThreshold = SettingsReader.getSleepThreshold()
	#newSleepMinValue = SettingsReader.getSleepMinValue()
	#newCalendar = SettingsReader.getCalendar()
	ts = time.time()
	
	# trigger in case of first run or changed data
	#if firstRun == 0 or newSleepThreshold != sleepThreshold or newSleepMinValue != sleepMinValue or json.dumps(calendar) != json.dumps(newCalendar):
        if firstRun == 0:
		firstRun = 1
		#sleepThreshold = newSleepThreshold
		#sleepMinValue = newSleepMinValue
		#calendar = newCalendar
		if sleepMinValue < sleepThreshold:
			Various_Functions.qboSpeak('Es scheint als haettest du kuerzlich schlecht geschlafen. Sage Dialog und danach Schlaf, um Hilfe zu bekommen.')
			
	if calendarTriggered == 0 and ts > (launch+15):
		calendarTriggered = 1
		Various_Functions.qboSpeak('In 10 Minuten ist Zeit fuer Medikamente nehmen.')
	