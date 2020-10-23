#!/usr/bin/env python
# coding=utf-8
import requests
import json
import base64
import os
import json

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# -------------------------------------------------------------------------------------------
# Settings Class holds internal json representation
# -------------------------------------------------------------------------------------------
class MySettings:

    # initialization
    def __init__(self):
        self._load_settings()

    # write update to server
    def update_settings(self):   
        self.uploadSettings(self.settings) # upload json file

    # load update from server
    def _load_settings(self):
        self.settings = json.loads(self.downloadSettings()) # download json file
        
        # save to members to access from outside
        self.robotName = self.settings['robotSettings']['robotName']
        self.robotAudioVolume = self.settings['robotSettings']['robotAudioVolume']
        self.robotVoice = self.settings['robotSettings']['robotVoice']
        self.robotThresholdSleep = self.settings['robotSettings']['robotThresholdSleep']
        self.userName = self.settings['userSettings']['userName']
        self.userEmergencyEmail = self.settings['userSettings']['emergencyAddress']['emergencyEmailAccount']
        self.userSleepMinValue = self.settings['fitbitSettings']['sleepMinValue']
    
    # -------------------------------------------------------------------------------------------
    # uploadSettingsEntry (upload full settings with all entries)
    # -------------------------------------------------------------------------------------------
    def uploadSettings(self, settings):
    
        try:     
            r = requests.post('https://power2dm.salzburgresearch.at/robogen/DataBase/UploadJSON_MySettings', timeout=5, verify=False, json=settings)
            headers = {'Content-type': 'application/json'}      
            
            if r.ok:
                print(r.content)
            else:
                print("--------------------------")
                print("Fehler bei Server-Antwort: " + str(r.status_code))
                print("--------------------------")
                        
        except requests.exceptions.RequestException as e:
            print e
        
    # -------------------------------------------------------------------------------------------
    # downloadSettings (download full settings with all entries)
    # -------------------------------------------------------------------------------------------
    def downloadSettings(self):
    
        try:     
            r = requests.post('https://power2dm.salzburgresearch.at/robogen/DataBase/DownloadJSON_MySettings', timeout=5, verify=False, json='')
            headers = {'Content-type': 'application/json'}      
            
            if r.ok:
                #print(r.content)
                return r.content
            else:
                print("--------------------------")
                print("Fehler bei Server-Antwort: " + str(r.status_code))
                print("--------------------------")
                return "Error"
                        
        except requests.exceptions.RequestException as e:
            print e
            
            
            
            