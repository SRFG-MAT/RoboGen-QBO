import os
import json

class MySettings:
    SETTINGS_FILE = '/opt/QBO/RoboGen-QBO/Python_Projects/MyQBOSettings/settings.json'

    def __init__(self):
        self._load_settings()

    def update_settings(self):
        if self._last_update != os.stat(self.SETTINGS_FILE).st_mtime:
            self._load_settings()
            return True
        return False

    def _load_settings(self):
        with open(self.SETTINGS_FILE) as json_settings:
            settings = json.load(json_settings)
            
            # file info
            self._last_update = os.fstat(json_settings.fileno()).st_mtime

            # robot
            self.robot_name = settings['robotSettings']['robotName']
            self.robot_audiovolume = settings['robotSettings']['robotAudioVolume']
            self.robot_voice = settings['robotSettings']['robotVoice']
            self.robot_threshold_sleep = settings['robotSettings']['robotThresholdSleep']

            # user
            self.user_name = settings['userSettings']['userName']
            self.user_emergency_email = settings['userSettings']['emergencyAddress']['emergencyEmailAccount'] 

            # others
            self.fitbit_sleepMin = settings['fitbitSettings']['sleepMinValue'] 
            self.calendar_settings = settings['calSettings']
            
            
            
            