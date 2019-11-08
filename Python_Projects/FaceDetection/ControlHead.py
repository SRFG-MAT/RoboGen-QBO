import time
import serial #handles the serial ports
import QboCmd #holds some commands we can use for Qbo
import cv2

Control_X_Axis = 1
Control_Y_Axis = 2
Control_Speed = 100

AngleLimit_Right = 290
AngleLimit_Left = 725
AngleLimit_Up = 530
AngleLimit_Down = 400

#-------------------------------------------------------------------------------------------
# helper functions for moving head using axis, angle and speed
#-------------------------------------------------------------------------------------------
def moveHeadAxis(axis, angle, QBO): 
    QBO.SetServo(axis, angle, Control_Speed)#Axis,Angle,Speed
    
def moveToStart(QBO):
    QBO.SetServo(Control_X_Axis, 511, Control_Speed)#Axis,Angle,Speed
    QBO.SetServo(Control_Y_Axis, 450, Control_Speed)#Axis,Angle,Speed
    time.sleep(1)


#-------------------------------------------------------------------------------------------
# define required head postition variables and constants
#-------------------------------------------------------------------------------------------
def controlQBOHead(threadName, vs, ser, QBO):
    
    CurrentAngle_X = 511 # start pos
    CurrentAngle_Y = 450 # start pos

    moveToStart(QBO)

    #-------------------------------------------------------------------------------------------
    # run in loop, stream QBO video and wait for QWEASD key inputs
    #-------------------------------------------------------------------------------------------
    while True:
        
        ret, frame = vs.read()
        if frame is None:
            continue
        
        cv2.imshow("QBO Video", frame)
        
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord("w"):
            
            if(CurrentAngle_Y > AngleLimit_Down):
                CurrentAngle_Y = CurrentAngle_Y - 10
            
            print("Kopf nach oben bewegen") # print message hier nach oben weil nicht spiegelverkehrt!!
            moveHeadAxis(Control_Y_Axis, CurrentAngle_Y, QBO)
            
        elif key == ord("a"):
            
            if(CurrentAngle_X > AngleLimit_Right):
                CurrentAngle_X = CurrentAngle_X - 20
            
            print("Kopf nach rechts bewegen")
            moveHeadAxis(Control_X_Axis, CurrentAngle_X, QBO)
            
        elif key == ord("s"):
            
            if(CurrentAngle_Y < AngleLimit_Up):
                CurrentAngle_Y = CurrentAngle_Y + 10
            
            print("Kopf nach unten bewegen") # print message hier nach unten weil nicht spiegelverkehrt!!
            moveHeadAxis(Control_Y_Axis, CurrentAngle_Y, QBO)
            
        elif key == ord("d"):
            
            if(CurrentAngle_X < AngleLimit_Left):
                CurrentAngle_X = CurrentAngle_X + 20
        
            print("Kopf nach links bewegen")
            moveHeadAxis(Control_X_Axis, CurrentAngle_X, QBO)
        
        elif key == ord("e"):
            print("Kopf in Startposition ausrichten!")
            moveToStart(QBO)
            
        elif key == ord("q"):
            print("Anwendung wird geschlossen...")
            break
    







    
    