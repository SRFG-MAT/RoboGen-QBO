#!/usr/bin/env python

import rospy
import actionlib
import robogenqbo.msg

import os, sys, time
sys.path.append('/opt/QBO/catkin_ws/src/RoboGen-QBO/scripts/python/RoboGen_Projects/EmotionAudio/')
import Processing_Audio
import Various_Functions

# saved settings
sys.path.append('/opt/QBO/catkin_ws/src/RoboGen-QBO/scripts/python/RoboGen_Projects/MyQBOSettings')
import SettingsReader

#------------------------------------------------------------------------------------------------------------------------------------------------------------
# helper function: fibonacci_example
#------------------------------------------------------------------------------------------------------------------------------------------------------------
def fibonacci_example(self):
    
    r = rospy.Rate(1)
    success = True
    
    for i in range(1, goal.order):
        # check that preempt has not been requested by the client
        if self._as.is_preempt_requested():
            rospy.loginfo('%s: Preempted' % self._action_name)
            self._as.set_preempted()
            success = False
            break
            
        self._feedback.sequence.append(self._feedback.sequence[i] + self._feedback.sequence[i-1])           
        self._as.publish_feedback(self._feedback) # publish the feedback 
        r.sleep() # this step is not necessary, the sequence is computed at 1 Hz for demonstration purposes
    
    return success

#------------------------------------------------------------------------------------------------------------------------------------------------------------
# helper function: qbo functions
#------------------------------------------------------------------------------------------------------------------------------------------------------------
def qbo_speak(sentence):
    Various_Functions.qboSpeak(sentence)
    return True
    
def qbo_listen():
    print ('Jetzt sprechen!')
    sentence = Processing_Audio.getAudioToText()
    sentence = Various_Functions.normalize(sentence).strip()
    print ('Du hast gesagt: ' + sentence)
    return True
    
def qbo_write_setting(setting, value):
    
    if (setting == 'robotName'):
        SettingsReader.setRobotNameFromSettings()
        return True

    elif (setting == 'userName'):
        SettingsReader.setUserName(value)
        return True
    
    elif (setting == 'emergencyMail'):
        SettingsReader.setEmergencyEmail(value)
        return True
    
    else:
        return 'Error: Unknown setting'
        return False
    
def qbo_read_setting(setting):
    
    if (setting == 'robotName'): 
        print (SettingsReader.getRobotNameFromSettings().lower().strip())
        return True

    elif (setting == 'userName'):
        print (SettingsReader.getUserName())
        return True
    
    elif (setting == 'emergencyMail'):
        print (SettingsReader.getEmergencyEmail().lower().strip())
        return True
    
    else:
        return 'Error: Unknown setting'
        return False

#------------------------------------------------------------------------------------------------------------------------------------------------------------
# VoiceOutput
#------------------------------------------------------------------------------------------------------------------------------------------------------------
class VoiceOutput(object):
    
    _feedback = robogenqbo.msg.VoiceOutputFeedback() # create feedback message
    _result = robogenqbo.msg.VoiceOutputResult() # create result message

    def __init__(self, name):
        self._action_name = name
        self._as = actionlib.SimpleActionServer(self._action_name, robogenqbo.msg.VoiceOutputAction, execute_cb=self.execute_cb, auto_start = False)
        self._as.start()
      
    def execute_cb(self, goal):
        
        # append the seeds for the fibonacci sequence
        self._feedback.sequence = []
        self._feedback.sequence.append(0)
        self._feedback.sequence.append(1)
        
        rospy.loginfo('%s: Executing, creating VoiceOutput with sentence %s with seeds %i, %i' % (self._action_name, goal.voice_output, self._feedback.sequence[0], self._feedback.sequence[1]))
        
        # start executing the action
        #success = fibonacci_example(self, success)
        success = qbo_speak(goal.voice_output)
          
        if success:
            self._result.sequence = self._feedback.sequence
            rospy.loginfo('%s: Succeeded' % self._action_name)
            self._as.set_succeeded(self._result)
			
#------------------------------------------------------------------------------------------------------------------------------------------------------------
# WaitForUserInput
#------------------------------------------------------------------------------------------------------------------------------------------------------------
class WaitForUserInput(object):
    
    _feedback = robogenqbo.msg.WaitForUserInputFeedback() #create feedback message
    _result = robogenqbo.msg.WaitForUserInputResult() #create result message

    def __init__(self, name):
        self._action_name = name
        self._as = actionlib.SimpleActionServer(self._action_name, robogenqbo.msg.WaitForUserInputAction, execute_cb=self.execute_cb, auto_start = False)
        self._as.start()
      
    def execute_cb(self, goal):
        
        # append the seeds for the fibonacci sequence
        self._feedback.sequence = []
        self._feedback.sequence.append(0)
        self._feedback.sequence.append(1)
        
        rospy.loginfo('%s: Executing, creating WaitForUserInput sequence of order %i with seeds %i, %i' % (self._action_name, goal.order, self._feedback.sequence[0], self._feedback.sequence[1]))
        
        # start executing the action
        #success = fibonacci_example(self, success)
        success = qbo_listen()
          
        if success:
            self._result.sequence = self._feedback.sequence
            rospy.loginfo('%s: Succeeded' % self._action_name)
            self._as.set_succeeded(self._result)

#------------------------------------------------------------------------------------------------------------------------------------------------------------
# GetData
#------------------------------------------------------------------------------------------------------------------------------------------------------------
class GetData(object):
    
    _feedback = robogenqbo.msg.GetDataFeedback() #create feedback message
    _result = robogenqbo.msg.GetDataResult() #create result message

    def __init__(self, name):
        self._action_name = name
        self._as = actionlib.SimpleActionServer(self._action_name, robogenqbo.msg.GetDataAction, execute_cb=self.execute_cb, auto_start = False)
        self._as.start()
      
    def execute_cb(self, goal):
        
        # append the seeds for the fibonacci sequence
        self._feedback.sequence = []
        self._feedback.sequence.append(0)
        self._feedback.sequence.append(1)
        
        rospy.loginfo('%s: Executing, creating GetData sequence of order %i with seeds %i, %i' % (self._action_name, goal.order, self._feedback.sequence[0], self._feedback.sequence[1]))
        
        # start executing the action
        #success = fibonacci_example(self, success)
        success = qbo_read_setting('robotName');
          
        if success:
            self._result.sequence = self._feedback.sequence
            rospy.loginfo('%s: Succeeded' % self._action_name)
            self._as.set_succeeded(self._result)

#------------------------------------------------------------------------------------------------------------------------------------------------------------
# SetData
#------------------------------------------------------------------------------------------------------------------------------------------------------------
class SetData(object):
    
    _feedback = robogenqbo.msg.SetDataFeedback() #create feedback message
    _result = robogenqbo.msg.SetDataResult() #create result message

    def __init__(self, name):
        self._action_name = name
        self._as = actionlib.SimpleActionServer(self._action_name, robogenqbo.msg.SetDataAction, execute_cb=self.execute_cb, auto_start = False)
        self._as.start()
      
    def execute_cb(self, goal):
        
        # append the seeds for the fibonacci sequence
        self._feedback.sequence = []
        self._feedback.sequence.append(0)
        self._feedback.sequence.append(1)
        
        rospy.loginfo('%s: Executing, creating SetData sequence of order %i with seeds %i, %i' % (self._action_name, goal.order, self._feedback.sequence[0], self._feedback.sequence[1]))
        
        # start executing the action
        #success = fibonacci_example(self, success)
        success = qbo_write_setting('robotName', 'Maria')
          
        if success:
            self._result.sequence = self._feedback.sequence
            rospy.loginfo('%s: Succeeded' % self._action_name)
            self._as.set_succeeded(self._result)
     
#------------------------------------------------------------------------------------------------------------------------------------------------------------
# main function
#------------------------------------------------------------------------------------------------------------------------------------------------------------	 
if __name__ == '__main__':
    rospy.init_node('qbo')
    server1 = VoiceOutput(rospy.get_name())
    server2 = WaitForUserInput(rospy.get_name())
    server3 = GetData(rospy.get_name())
    server4 = SetData(rospy.get_name())
    rospy.spin()
	
	
	