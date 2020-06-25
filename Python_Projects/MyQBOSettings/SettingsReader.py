#!/usr/bin/env python
# coding=utf-8
import os, json
from gtts import gTTS
from string import punctuation

# used for setting os audio volume
from subprocess import call


settingsfile_path = '/opt/QBO/RoboGen-QBO/Python_Projects/MyQBOSettings/settings.json'
settings_data = {}

# -------------------------------------------------------------------------------------------
# write json settings file
# -------------------------------------------------------------------------------------------
def writeJsonFile(byte_data):
    
    my_json = byte_data.decode('string-escape').replace("'", '"')
    data = json.loads(my_json)
    
    s = json.dumps(data, indent=4, sort_keys=True)
    
    print "------------------------------------------"
    print s
    print "------------------------------------------"
    
    open(settingsfile_path,"w").write(s)
    


#---------------------------------------------------------------------------------------------
# get settings
#---------------------------------------------------------------------------------------------
def getRobotNameFromSettings():
    
    with open(settingsfile_path, 'r') as settings_file:
        settings_data = json.load(settings_file)      
        return settings_data['robotSettings']['robotName']
            
            
def getRobotAudioVolume():
    
    with open(settingsfile_path, 'r') as settings_file:
        settings_data = json.load(settings_file)
        return settings_data['robotSettings']['robotAudioVolume']
    
    
def getRobotAudioVoice():
    
    with open(settingsfile_path, 'r') as settings_file:
        settings_data = json.load(settings_file)
        return settings_data['robotSettings']['robotVoice']   

def getSleepThreshold():

    with open(settingsfile_path, 'r') as settings_file:
        settings_data = json.load(settings_file)
        return settings_data['robotSettings']['robotThresholdSleep'] 		
    
def getUserName():

    with open(settingsfile_path, 'r') as settings_file:
        settings_data = json.load(settings_file)
        return settings_data['userSettings']['userName'] 
	
def getEmergencyEmail():

    with open(settingsfile_path, 'r') as settings_file:
        settings_data = json.load(settings_file)
        return settings_data['userSettings']['emergencyAddress']['emergencyEmailAccount']  
		
def getSleepMinValue():
    with open(settingsfile_path, 'r') as settings_file:
        settings_data = json.load(settings_file)
        return settings_data['fitbitSettings']['sleepMinValue'] 
		
def getCalendar():
    with open(settingsfile_path, 'r') as settings_file:
        settings_data = json.load(settings_file)
        return settings_data['calSettings']
    
        