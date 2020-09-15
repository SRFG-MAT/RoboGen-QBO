#!/usr/bin/env python
# coding=utf-8
import os, json
from gtts import gTTS
from string import punctuation

# used for setting os audio volume
from subprocess import call

# Settings Class
import Settings
mysettings = Settings.MySettings()

# -------------------------------------------------------------------------------------------
# write json settings file (from bluetooth data)
# -------------------------------------------------------------------------------------------
def writeJsonFile(byte_data):
    
    my_json = byte_data.decode('string-escape').replace("'", '"')

    data = json.loads(my_json)
    s = json.dumps(data, indent=4, sort_keys=True)
    
    open(mysettings.SETTINGS_FILE,"w").write(s)
    mysettings.update_settings()
    
    print "------------------------------------------"
    print s
    print "------------------------------------------"
    
    
# -------------------------------------------------------------------------------------------
# increment robot audio volume
# -------------------------------------------------------------------------------------------
def incrementRobotAudioVolume():
    
    if(mysettings.robot_audiovolume <= 90):
        
        with open(mysettings.SETTINGS_FILE, "r") as settings_file:
            data = json.load(settings_file)

        data['robotSettings']['robotAudioVolume']= mysettings.robot_audiovolume + 10
        s = json.dumps(data, indent=4, sort_keys=True)

        with open(mysettings.SETTINGS_FILE, "w") as settings_file:
            settings_file.write(s)
        
        mysettings.update_settings()
    
# -------------------------------------------------------------------------------------------
# decrement robot audio volume
# -------------------------------------------------------------------------------------------
def decrementRobotAudioVolume():
    
    if(mysettings.robot_audiovolume >= 10):
        
        with open(mysettings.SETTINGS_FILE, "r") as settings_file:
            data = json.load(settings_file)

        data['robotSettings']['robotAudioVolume']= mysettings.robot_audiovolume - 10
        s = json.dumps(data, indent=4, sort_keys=True)

        with open(mysettings.SETTINGS_FILE, "w") as settings_file:
            settings_file.write(s)
        
        mysettings.update_settings()

#---------------------------------------------------------------------------------------------
# getters
#---------------------------------------------------------------------------------------------
def getRobotNameFromSettings(): 
    return mysettings.robot_name
            
def getRobotAudioVolume():
    return mysettings.robot_audiovolume
    
def getRobotAudioVoice():
    return mysettings.robot_voice

def getSleepThreshold():
    return mysettings.robot_threshold_sleep
    
def getUserName():
    return mysettings.user_name
	
def getEmergencyEmail():
    return mysettings.user_emergency_email
		
def getSleepMinValue():
    return mysettings.fitbit_sleepMin
		
def getCalendar():
    return mysettings.calendar_settings
    
        
