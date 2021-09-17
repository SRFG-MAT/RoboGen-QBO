#! /usr/bin/env python

import rospy

# Brings in the SimpleActionClient
import actionlib

# Brings in the messages used by the qbo actions, including the
# goal message and the result message of the task modules "WaitForUserInput" and "VoiceOutput"
import robogenqbo.msg


#------------------------------------------------------------------------------------------------------------------------------------------------------------
# client implementation of QBO functions
#------------------------------------------------------------------------------------------------------------------------------------------------------------
def qbo_request_VoiceOutput():

    # Creates the SimpleActionClient, passing the type of the action
    # (VoiceOutputAction) to the constructor.
    client = actionlib.SimpleActionClient('qbo', robogenqbo.msg.VoiceOutputAction)

    # Waits until the action server has started up and started
    # listening for goals.
    client.wait_for_server()

    # Creates a goal to send to the action server.
    goal = robogenqbo.msg.VoiceOutputGoal(voice_output='Hallo du')

    # Sends the goal to the action server.
    client.send_goal(goal)

    # Waits for the server to finish performing the action.
    client.wait_for_result()

    # Prints out the result of executing the action
    return client.get_result()  # A VoiceOutputResult

	
#------------------------------------------------------------------------------------------------------------------------------------------------------------
# main function
#------------------------------------------------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    try:	
        # Initializes a rospy node so that the SimpleActionClient can
        # publish and subscribe over ROS.
		
        rospy.init_node('qbo_client_py')
        result = qbo_request_VoiceOutput()
        print("Result:", ', '.join([str(n) for n in result.sequence]))
    except rospy.ROSInterruptException:
        print("program interrupted before completion")
