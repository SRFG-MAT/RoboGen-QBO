#!/usr/bin/env python
import os, sys, time
import rospy
import actionlib
import robogenqbo.msg

# audio capabilities
sys.path.append('/opt/QBO/catkin_ws/src/RoboGen-QBO/scripts/python/RoboGen_Projects/EmotionAudio/')
import Processing_Audio
import Various_Functions

# saved settings
sys.path.append('/opt/QBO/catkin_ws/src/RoboGen-QBO/scripts/python/RoboGen_Projects/MyQBOSettings')
import SettingsReader

#set up ports for communicating with servos
sys.path.append('/opt/QBO/catkin_ws/src/RoboGen-QBO/scripts/python/RoboGen_Projects/EmotionVideo/')
sys.path.append('/opt/QBO/catkin_ws/src/RoboGen-QBO/scripts/python/RoboGen_Projects/ControlQBO')
import serial
import QboCmd
from ControlHeadAsync import *
from EmotionDetectionClient import *

port = '/dev/serial0'
ser = serial.Serial(port, baudrate=115200, bytesize = serial.EIGHTBITS, stopbits = serial.STOPBITS_ONE, parity = serial.PARITY_NONE, rtscts = False, dsrdtr =False, timeout = 0)
QBO = QboCmd.Controller(ser)
QBO.SetNoseColor(QboCmd.nose_color_none) # init nose


#------------------------------------------------------------------------------------------------------------------------------------------------------------
# helper function: speak
#------------------------------------------------------------------------------------------------------------------------------------------------------------
def qbo_speak(sentence):
    Various_Functions.qboSpeak(sentence)
    return True
    
#------------------------------------------------------------------------------------------------------------------------------------------------------------
# helper function: listen
#------------------------------------------------------------------------------------------------------------------------------------------------------------
def qbo_listen():
    print ('Jetzt sprechen!')
    sentence = Processing_Audio.getAudioToText()
    sentence = Various_Functions.normalize(sentence).strip()
    print ('Du hast gesagt: ' + sentence)
    return sentence

#------------------------------------------------------------------------------------------------------------------------------------------------------------
# helper function: move head
#------------------------------------------------------------------------------------------------------------------------------------------------------------ 
def qbo_movehead(position):
 
    if position == "up":           
        print("Kopf nach oben bewegen") # print message hier nach oben weil nicht spiegelverkehrt!!
        QBO.SetServo(2, 450 - 40, 100) #Axis,Angle,Speed
        return True
            
    elif position == "right":   
        print("Kopf nach rechts bewegen")
        QBO.SetServo(1, 511 - 80, 100)
        return True
            
    elif position == "down":            
        print("Kopf nach unten bewegen") # print message hier nach unten weil nicht spiegelverkehrt!!
        QBO.SetServo(2, 450 + 40, 100)
        return True
            
    elif position == "left":        
        print("Kopf nach links bewegen")
        QBO.SetServo(1, 511 + 80, 100)
        return True
        
    elif position == "start":      
        print("Kopf in Startposition ausrichten!")
        QBO.SetServo(1, 511, 100) #Axis,Angle,Speed
        time.sleep(0.1)
        QBO.SetServo(2, 450, 100) #Axis,Angle,Speed
        return True
        
    else:
        return False
    
#------------------------------------------------------------------------------------------------------------------------------------------------------------
# helper function: speak
#------------------------------------------------------------------------------------------------------------------------------------------------------------
def qbo_facedetection(inputFace):
    
    analyzeFramesForEmotion(inputFace) # stop on seeing input face
    return True # TODO

#------------------------------------------------------------------------------------------------------------------------------------------------------------
# helper function: speak
#------------------------------------------------------------------------------------------------------------------------------------------------------------
def qbo_facialexpression(inputFace):
    
    ret = True  
    QBO.SetNoseColor(QboCmd.nose_color_blue_dark)

    if inputFace == "fear":     
        QBO.SetMouth(0x1f1f1f1f) # all leds on
    elif inputFace == "happy":
        QBO.SetMouth(0x110e0000) #smile
    elif inputFace == "neutral":
        QBO.SetMouth(0x1f1f00) #serious
    elif inputFace == "pain":
        QBO.SetMouth(0x40e1f) #pyramide
    elif inputFace == "sadness":
        QBO.SetMouth(0x0e1100) #sad
    elif inputFace == "surprise":
        QBO.SetMouth(0x1f1b151f) #oval
    else:
        QBO.SetMouth(0x1b1f0e04) #love
        ret = False
    
    time.sleep(5)
    QBO.SetMouth(0x00000000) # all leds off
    QBO.SetNoseColor(QboCmd.nose_color_none) 
    
    return ret # TODO
    
#------------------------------------------------------------------------------------------------------------------------------------------------------------
# helper function: write a setting
#------------------------------------------------------------------------------------------------------------------------------------------------------------
def qbo_write_setting(setting, value):
    
    if (setting == 'robotName'):
        SettingsReader.renameRobot(value)
        return True

    elif (setting == 'userName'):
        SettingsReader.renameUser(value)
        return True
    
    else:
        return 'Error: Unknown setting'
        return False
    
#------------------------------------------------------------------------------------------------------------------------------------------------------------
# helper function: read a setting
#------------------------------------------------------------------------------------------------------------------------------------------------------------
def qbo_read_setting(setting):
    
    if (setting == 'robotName'): 
        return (SettingsReader.getRobotNameFromSettings().lower().strip())

    elif (setting == 'userName'):
        return (SettingsReader.getUserName().lower().strip())
    
    else:
        return 'Error: Unknown setting'


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
        
        # append the seeds to give user feedback
        self._feedback.sequence = []
        self._feedback.sequence.append(0)
        self._feedback.sequence.append(1)
        
        rospy.loginfo('%s: Executing, creating VoiceOutput with outputMessage %s with seeds %i, %i' % (self._action_name, goal.outputMessage, self._feedback.sequence[0], self._feedback.sequence[1]))
        
        # start executing the action
        #success = fibonacci_example(self, success)
        success = qbo_speak(goal.outputMessage)
          
        if success:
            self._result.isOK = success
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
        
        # append the seeds to give user feedback
        self._feedback.sequence = []
        self._feedback.sequence.append(0)
        self._feedback.sequence.append(1)
        
        rospy.loginfo('%s: Executing, creating WaitForUserInput with input content %s with seeds %i, %i' % (self._action_name, goal.inputContent, self._feedback.sequence[0], self._feedback.sequence[1]))
        
        # start executing the action
        #success = fibonacci_example(self, success)
        success = True
        returnMsg = qbo_listen()
          
        if success:
            self._result.returnMessage = str(returnMsg)
            rospy.loginfo('%s: Succeeded' % self._action_name)
            self._as.set_succeeded(self._result)

#------------------------------------------------------------------------------------------------------------------------------------------------------------
# MoveToLocation
#------------------------------------------------------------------------------------------------------------------------------------------------------------
class MoveToLocation(object):
       
    _feedback = robogenqbo.msg.MoveToLocationFeedback() #create feedback message
    _result = robogenqbo.msg.MoveToLocationResult() #create result message

    def __init__(self, name):
        self._action_name = name
        self._as = actionlib.SimpleActionServer(self._action_name, robogenqbo.msg.MoveToLocationAction, execute_cb=self.execute_cb, auto_start = False)
        self._as.start()
      
    def execute_cb(self, goal):
        
        # append the seeds to give user feedback
        self._feedback.sequence = []
        self._feedback.sequence.append(0)
        self._feedback.sequence.append(1)
        
        rospy.loginfo('%s: Executing, creating MoveToLocation sequence with location %s with seeds %i, %i' % (self._action_name, goal.location, self._feedback.sequence[0], self._feedback.sequence[1]))
        
        # start executing the action
        #success = fibonacci_example(self, success)
        success = qbo_movehead(goal.location)
          
        if success:
            self._result.isOK = success
            rospy.loginfo('%s: Succeeded' % self._action_name)
            self._as.set_succeeded(self._result)

#------------------------------------------------------------------------------------------------------------------------------------------------------------
# WaitForExternalEvent
#------------------------------------------------------------------------------------------------------------------------------------------------------------
class WaitForExternalEvent(object):
    
    _feedback = robogenqbo.msg.WaitForExternalEventFeedback() #create feedback message
    _result = robogenqbo.msg.WaitForExternalEventResult() #create result message

    def __init__(self, name):
        self._action_name = name
        self._as = actionlib.SimpleActionServer(self._action_name, robogenqbo.msg.WaitForExternalEventAction, execute_cb=self.execute_cb, auto_start = False)
        self._as.start()
      
    def execute_cb(self, goal):
        
        # append the seeds to give user feedback
        self._feedback.sequence = []
        self._feedback.sequence.append(0)
        self._feedback.sequence.append(1)
        
        rospy.loginfo('%s: Executing, creating WaitForExternalEvent sequence with inputText %s with seeds %i, %i' % (self._action_name, goal.inputText, self._feedback.sequence[0], self._feedback.sequence[1]))
        
        # start executing the action
        #success = fibonacci_example(self, success)
        success = qbo_facedetection(goal.inputText)
          
        if success:
            self._result.isOK = success
            rospy.loginfo('%s: Succeeded' % self._action_name)
            self._as.set_succeeded(self._result)
    
#------------------------------------------------------------------------------------------------------------------------------------------------------------
# GraphicalUserInteraction
#------------------------------------------------------------------------------------------------------------------------------------------------------------
class GraphicalUserInteraction(object):
    
    _feedback = robogenqbo.msg.GraphicalUserInteractionFeedback() #create feedback message
    _result = robogenqbo.msg.GraphicalUserInteractionResult() #create result message

    def __init__(self, name):
        self._action_name = name
        self._as = actionlib.SimpleActionServer(self._action_name, robogenqbo.msg.GraphicalUserInteractionAction, execute_cb=self.execute_cb, auto_start = False)
        self._as.start()
      
    def execute_cb(self, goal):
        
        # append the seeds to give user feedback
        self._feedback.sequence = []
        self._feedback.sequence.append(0)
        self._feedback.sequence.append(1)
        
        rospy.loginfo('%s: Executing, creating GraphicalUserInteraction sequence with outputMessage %s with seeds %i, %i' % (self._action_name, goal.outputMessage, self._feedback.sequence[0], self._feedback.sequence[1]))
        
        # start executing the action
        #success = fibonacci_example(self, success)
        success = qbo_facialexpression(goal.outputMessage)
          
        if success:
            self._result.isOK = success
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
        
        # append the seeds to give user feedback
        self._feedback.sequence = []
        self._feedback.sequence.append(0)
        self._feedback.sequence.append(1)
        
        rospy.loginfo('%s: Executing, creating GetData sequence with inputData %s with seeds %i, %i' % (self._action_name, goal.inputData, self._feedback.sequence[0], self._feedback.sequence[1]))
        
        # start executing the action
        #success = fibonacci_example(self, success)
        success = True
        robotName = qbo_read_setting(goal.inputData);
          
        if success:
            self._result.data = str(robotName)
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
        
        # append the seeds to give user feedback
        self._feedback.sequence = []
        self._feedback.sequence.append(0)
        self._feedback.sequence.append(1)
        
        rospy.loginfo('%s: Executing, creating SetData sequence with outputData %s with seeds %i, %i' % (self._action_name, goal.outputData, self._feedback.sequence[0], self._feedback.sequence[1]))
        
        # start executing the action
        #success = fibonacci_example(self, success)
        success = qbo_write_setting('robotName', goal.outputData)
          
        if success:
            self._result.isOK = success
            rospy.loginfo('%s: Succeeded' % self._action_name)
            self._as.set_succeeded(self._result)

#------------------------------------------------------------------------------------------------------------------------------------------------------------
# main function
#------------------------------------------------------------------------------------------------------------------------------------------------------------	 
if __name__ == '__main__':
    
    rospy.init_node('qbo')
    server1 = VoiceOutput('VoiceOutput')
    server2 = WaitForUserInput('WaitForUserInput')
    server3 = MoveToLocation('MoveToLocation')
    server4 = WaitForExternalEvent('WaitForExternalEvent')
    server5 = GraphicalUserInteraction('GraphicalUserInteraction')
    server6 = GetData('GetData')
    server7 = SetData('SetData')
    rospy.spin()
	
	
	