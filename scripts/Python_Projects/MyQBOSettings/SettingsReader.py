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

age_senior = 50
vol_min = 50
vol_max = 90

# -------------------------------------------------------------------------------------------
# to update/refresh infos from outside
# -------------------------------------------------------------------------------------------
def LoadFromServer():
    mysettings._load_settings()

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
    
    if(mysettings.robotAudioVolume <= (vol_max-10)):
        mysettings.settings['robotSettings']['robotAudioVolume']+= 10
        mysettings.update_settings()
        mysettings._load_settings()
    
# -------------------------------------------------------------------------------------------
# decrement robot audio volume
# -------------------------------------------------------------------------------------------
def decrementRobotAudioVolume():
    
    if(mysettings.robotAudioVolume >= (vol_min+10)):
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

def getUserSen():
    return (mysettings.userAge>=age_senior)

def getUserDiab():
    return ((mysettings.userDiseases==0) or (mysettings.userDiseases==2))

def getEmergencyEmail():
    return mysettings.userEmergencyEmail

def getSleepMinValue():
    return mysettings.userSleepMinValue

def getCalendar():
    return mysettings.calendar_settings