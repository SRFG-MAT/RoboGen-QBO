import time
import serial #handles the serial ports
import QboCmd #holds some commands we can use for Qbo
import cv2

#-------------------------------------------------------------------------------------------
#set up ports for communicating with servos
#-------------------------------------------------------------------------------------------
port = '/dev/serial0'
ser = serial.Serial(port, baudrate=115200, bytesize = serial.EIGHTBITS, stopbits = serial.STOPBITS_ONE, parity = serial.PARITY_NONE, rtscts = False, dsrdtr =False, timeout = 0)
QBO = QboCmd.Controller(ser)

#-------------------------------------------------------------------------------------------
# helper functions for moving head using axis, angle and speed
#-------------------------------------------------------------------------------------------
def moveHeadAxis(axis, angle): 
    QBO.SetServo(axis, angle, Control_Speed)#Axis,Angle,Speed
    
def moveToStart():
    QBO.SetServo(Control_X_Axis, 511, Control_Speed)#Axis,Angle,Speed
    QBO.SetServo(Control_Y_Axis, 450, Control_Speed)#Axis,Angle,Speed
    time.sleep(1)

#-------------------------------------------------------------------------------------------
# set up video stream
#-------------------------------------------------------------------------------------------
vs = cv2.VideoCapture(0)
vs.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 100)
vs.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 100)

#-------------------------------------------------------------------------------------------
# define required head postition variables and constants
#-------------------------------------------------------------------------------------------
Control_X_Axis = 1
Control_Y_Axis = 2
Control_Speed = 100

AngleLimit_Right = 290
AngleLimit_Left = 725
AngleLimit_Up = 530
AngleLimit_Down = 400

CurrentAngle_X = 511 # start pos
CurrentAngle_Y = 450 # start pos

moveToStart()

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
        moveHeadAxis(Control_Y_Axis, CurrentAngle_Y)
        
    elif key == ord("a"):
        
        if(CurrentAngle_X > AngleLimit_Right):
            CurrentAngle_X = CurrentAngle_X - 20
        
        print("Kopf nach rechts bewegen")
        moveHeadAxis(Control_X_Axis, CurrentAngle_X)
        
    elif key == ord("s"):
        
        if(CurrentAngle_Y < AngleLimit_Up):
            CurrentAngle_Y = CurrentAngle_Y + 10
        
        print("Kopf nach unten bewegen") # print message hier nach unten weil nicht spiegelverkehrt!!
        moveHeadAxis(Control_Y_Axis, CurrentAngle_Y)
        
    elif key == ord("d"):
        
        if(CurrentAngle_X < AngleLimit_Left):
            CurrentAngle_X = CurrentAngle_X + 20
        
        print("Kopf nach links bewegen")
        moveHeadAxis(Control_X_Axis, CurrentAngle_X)
        
    elif key == ord("e"):
        print("Kopf in Startposition ausrichten!")
        moveToStart()
        
    elif key == ord("q"):
        print("Anwendung wird geschlossen...")
        break
    







    
    