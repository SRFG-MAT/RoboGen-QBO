#!/usr/bin/env python
# coding=utf-8
import os
import json
from gtts import gTTS
from string import punctuation

settings_data = {}

#---------------------------------------------------------------------------------------------
# get robot name from settings data
#---------------------------------------------------------------------------------------------
def getRobotNameFromSettings():
    
    with open('/home/pi/Documents/RoboGen-QBO/Python_Projects/MyQBOSettings/settings.json', 'r') as settings_file:
        settings_data = json.load(settings_file)
        
        return settings_data['robotSettings']['robotName']
            