#!/usr/bin/env python2.7
import sys
import os
import time

## Initial Head position
Xcoor = 511
Ycoor = 450
Facedet = 0
Kpx = 1
Kpy = 1
Ksp = 40

## Head X and Y angle limits
Xmax = 725
Xmin = 290
Ymax = 550
Ymin = 420

# -------------------------------------------------------------------------------------------
# interprets the cameraCode from server to see if any adjustments from head are required
# -------------------------------------------------------------------------------------------
def AdjustHeadPosition(QBO, camCode):
    
    # no face found
    if camCode[0] == 0 and camCode[1] == 0:
        return
    
    QBO.SetNoseColor(2) 
    
    # move head left
    if camCode[0] > 190:       
        CamLeft(QBO, 2,1)
        print("Kopf nach links bewegen")
    elif camCode[0] > 200:      
        CamLeft(QBO, 5,2)
        print("Kopf nach links bewegen")
    elif camCode[0] > 210:      
        CamLeft(QBO, 10,3)
        print("Kopf nach links bewegen")

    # move head right
    if camCode[0] < 150:
        CamRight(QBO, 2,1)
        print("Kopf nach rechts bewegen")
    elif camCode[0] < 140:
        CamRight(QBO, 5,2)
        print("Kopf nach rechts bewegen")
    elif camCode[0] < 130:
        CamRight(QBO, 10,3)
        print("Kopf nach rechts bewegen")

    # move head down
    if camCode[1] > 150:
        CamDown(QBO, 1,1)
        print("Kopf nach unten bewegen")
    elif camCode[1] > 160:
        CamDown(QBO, 3,2)
        print("Kopf nach unten bewegen")
    elif camCode[1] > 170:
        CamDown(QBO, 7,3)
        print("Kopf nach unten bewegen")

    # move head up
    if camCode[1] < 130:
        CamUp(QBO, 1,1)
        print("Kopf nach oben bewegen")
    elif camCode[1] < 100:
        CamUp(QBO, 3,2)
        print("Kopf nach oben bewegen")
    elif camCode[1] < 90:
        CamUp(QBO, 7,3)
        print("Kopf nach oben bewegen")
               
        
# -------------------------------------------------------------------------------------------
# moves head left
# -------------------------------------------------------------------------------------------
def CamLeft(QBO, distance, speed ):                # To move left, we are provided a distance to move and a speed to move.
        global Xcoor, Xmin, touch_tm
        Xcoor = Xcoor - Kpx * distance
        if Xcoor < Xmin:
                Xcoor = Xmin
        #print "LEFT:",distance, Xcoor, Ycoor 
        QBO.SetServo(1, Xcoor, Ksp * speed)
        touch_tm = time.time()
        return

# -------------------------------------------------------------------------------------------
# moves head right
# -------------------------------------------------------------------------------------------
def CamRight(QBO, distance, speed):                   # Same logic as above
        global Xcoor, Xmax, touch_tm
        Xcoor = Xcoor + Kpx * distance
        if Xcoor > Xmax:
                Xcoor = Xmax
        #print "RIGHT:",distance, Xcoor, Ycoor 
        QBO.SetServo(1, Xcoor, Ksp * speed)
        touch_tm = time.time()
        return
    
# -------------------------------------------------------------------------------------------
# moves head down
# -------------------------------------------------------------------------------------------
def CamDown(QBO, distance, speed):                   # Same logic as above
        global Ycoor, Ymax, touch_tm
        Ycoor = Ycoor + Kpy * distance
        if Ycoor > Ymax:
                Ycoor = Ymax
        #print "DOWN:",distance, Xcoor, Ycoor 
        QBO.SetServo(2, Ycoor, Ksp * speed)
        touch_tm = time.time()
        return
    
# -------------------------------------------------------------------------------------------
# moves head up
# -------------------------------------------------------------------------------------------
def CamUp(QBO, distance, speed):                     # Same logic as above
        global Ycoor, Ymin, touch_tm
        Ycoor = Ycoor - Kpy * distance
        if Ycoor < Ymin:
                Ycoor = Ymin
        #print "UP:",distance, Xcoor,Ycoor
        QBO.SetServo(2, Ycoor, Ksp * speed)
        touch_tm = time.time()
        return
    
    