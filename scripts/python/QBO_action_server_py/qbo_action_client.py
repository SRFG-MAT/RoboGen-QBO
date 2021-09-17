#! /usr/bin/env python

import rospy
import time

# Brings in the SimpleActionClient
import actionlib

# Brings in the messages used by the qbo actions, including the
# goal message and the result message of the task modules "WaitForUserInput" and "VoiceOutput"
import robogenqbo.msg


#------------------------------------------------------------------------------------------------------------------------------------------------------------
# client request implementations of QBO action server functions
#------------------------------------------------------------------------------------------------------------------------------------------------------------
def qbo_request_VoiceOutput():
    
    rospy.init_node('qbo_client_py') # Initializes a rospy node so that the SimpleActionClient can publish and subscribe over ROS

    client = actionlib.SimpleActionClient('qbo', robogenqbo.msg.VoiceOutputAction) # Creates SimpleActionClient with VoiceOutputAction action type
    client.wait_for_server() # Waits until the action server has started up and started listening for goals
    goal = robogenqbo.msg.VoiceOutputGoal(outputMessage='Hallo ich bin ein sozialer Roboter') # Creates a goal to send to the action server
    client.send_goal(goal) # Sends the goal to the action server
    client.wait_for_result() # Waits for the server to finish performing the action
    
    return client.get_result() # Prints out the result (VoiceOutputResult) of executing the action


def qbo_request_WaitForUserInput():
    
    rospy.init_node('qbo_client_py') # Initializes a rospy node so that the SimpleActionClient can publish and subscribe over ROS

    client = actionlib.SimpleActionClient('qbo', robogenqbo.msg.WaitForUserInputAction) # Creates SimpleActionClient with WaitForUserInputAction action type
    client.wait_for_server() # Waits until the action server has started up and started listening for goals
    goal = robogenqbo.msg.WaitForUserInputGoal(inputContent='void') # Creates a goal to send to the action server
    client.send_goal(goal) # Sends the goal to the action server
    client.wait_for_result() # Waits for the server to finish performing the action
    
    return client.get_result() # Prints out the result (WaitForUserInputResult) of executing the action

def qbo_request_GetData():
    
    rospy.init_node('qbo_client_py') # Initializes a rospy node so that the SimpleActionClient can publish and subscribe over ROS

    client = actionlib.SimpleActionClient('qbo', robogenqbo.msg.GetDataAction) # Creates SimpleActionClient with GetDataAction action type
    client.wait_for_server() # Waits until the action server has started up and started listening for goals
    goal = robogenqbo.msg.GetDataGoal(inputData='robotName') # Creates a goal to send to the action server
    client.send_goal(goal) # Sends the goal to the action server
    client.wait_for_result() # Waits for the server to finish performing the action
    
    return client.get_result() # Prints out the result (GetDataResult) of executing the action

def qbo_request_SetData():
    
    rospy.init_node('qbo_client_py') # Initializes a rospy node so that the SimpleActionClient can publish and subscribe over ROS

    client = actionlib.SimpleActionClient('qbo', robogenqbo.msg.SetDataAction) # Creates SimpleActionClient with SetDataAction action type
    client.wait_for_server() # Waits until the action server has started up and started listening for goals
    goal = robogenqbo.msg.SetDataGoal(outputData='Mario') # Creates a goal to send to the action server
    client.send_goal(goal) # Sends the goal to the action server
    client.wait_for_result() # Waits for the server to finish performing the action
    
    return client.get_result() # Prints out the result (SetDataResult) of executing the action
	
#------------------------------------------------------------------------------------------------------------------------------------------------------------
# main function
#------------------------------------------------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    try:	
        
        # request VoiceOutput
        result = qbo_request_VoiceOutput()
        if result:
            print ('----------------------------------')
            print("Result: " + str(result.isOK))
            print ('----------------------------------')
        
        # request WaitForUserInput
        #result = qbo_request_WaitForUserInput()
        #if result:
        #    print ('----------------------------------')
        #    print("Result:", ', '.join([str(n) for n in result.returnMessage]))
        #    print ('----------------------------------')
        
        # request GetData
        #result = qbo_request_GetData()
        #if result:
        #    print ('----------------------------------')
        #    print("Result:", ', '.join([str(n) for n in result.data]))
        #    print ('----------------------------------')
        
        # request SetData
        #result = qbo_request_SetData()
        #if result:
        #    print ('----------------------------------')
        #    print("Result: " + str(result.isOK))
        #    print ('----------------------------------')
             
    except rospy.ROSInterruptException:
        print("program interrupted before completion")
