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
# rename robot
# -------------------------------------------------------------------------------------------
def renameRobot(name):
    mysettings.settings['robotSettings']['robotName'] = name
    mysettings.update_settings()
    mysettings._load_settings()
    
# -------------------------------------------------------------------------------------------
# rename user
# -------------------------------------------------------------------------------------------
def renameUser(name):
    mysettings.settings['userSettings']['userName'] = name
    mysettings.update_settings()
    mysettings._load_settings()
    
# -------------------------------------------------------------------------------------------
# increment robot audio volume
# -------------------------------------------------------------------------------------------
def incrementRobotAudioVolume():
    
    if(mysettings.robotAudioVolume <= 90):
        mysettings.settings['robotSettings']['robotAudioVolume']+= 10
        mysettings.update_settings()
        mysettings._load_settings()
    
# -------------------------------------------------------------------------------------------
# decrement robot audio volume
# -------------------------------------------------------------------------------------------
def decrementRobotAudioVolume():
    
    if(mysettings.robotAudioVolume >= 10):
        mysettings.settings['robotSettings']['robotAudioVolume']-= 10
        mysettings.update_settings()
        mysettings._load_settings()

#---------------------------------------------------------------------------------------------
# getters
#---------------------------------------------------------------------------------------------
def getRobotNameFromSettings(): 
    return mysettings.robotName
            
def getRobotAudioVolume():
    return mysettings.robotAudioVolume
    
def getRobotAudioVoice():
    return mysettings.robotVoice

def getSleepThreshold():
    return mysettings.robotThresholdSleep
    
def getUserName():
    return mysettings.userName
	
def getEmergencyEmail():
    return mysettings.userEmergencyEmail
		
def getSleepMinValue():
    return mysettings.userSleepMinValue
		
def getCalendar():
    return mysettings.calendar_settings
    
        
