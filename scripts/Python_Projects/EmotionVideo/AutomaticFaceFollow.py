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

## cam code axes constants
camCode_XPos = 0
camCode_YPos = 1

## thresholds in frame
threshold_left1 = 265
threshold_left2 = 275
threshold_left3 = 285

threshold_right1 = 225
threshold_right2 = 215
threshold_right3 = 205

threshold_down1 = 200
threshold_down2 = 210
threshold_down3 = 220

threshold_up1 = 160
threshold_up2 = 150
threshold_up3 = 140

## distances for cam movement
distance_X1 = 1
distance_X2 = 2
distance_X3 = 3

distance_Y1 = 1
distance_Y2 = 2
distance_Y3 = 3

## speed for cam movement
cam_speed_slow = 1    ## standard is 1
cam_speed_medium = 2  ## standard is 2
cam_speed_fast = 3    ## standard is 3 (on QBO this is too fast, doesnt look good)

# -------------------------------------------------------------------------------------------
# interprets the cameraCode from server to see if any adjustments from head are required
# -------------------------------------------------------------------------------------------
def AdjustHeadPosition(QBO, camCode):
    
    # move head left
    if camCode[camCode_XPos] > threshold_left1:       
        CamLeft(QBO, distance_X1, cam_speed_slow)
        ##print("Kopf nach links bewegen 1")
    if camCode[camCode_XPos] > threshold_left2:      
        CamLeft(QBO, distance_X2, cam_speed_medium)
        ##print("Kopf nach links bewegen 2")
    if camCode[camCode_XPos] > threshold_left3:      
        CamLeft(QBO, distance_X3, cam_speed_fast)
        ##print("Kopf nach links bewegen 3")

    # move head right
    if camCode[camCode_XPos] < threshold_right1:
        CamRight(QBO, distance_X1, cam_speed_slow)
        ##print("Kopf nach rechts bewegen 1")
    if camCode[camCode_XPos] < threshold_right2:
        CamRight(QBO, distance_X2, cam_speed_medium)
        ##print("Kopf nach rechts bewegen 2")
    if camCode[camCode_XPos] < threshold_right3:
        CamRight(QBO, distance_X3, cam_speed_fast)
        ##print("Kopf nach rechts bewegen 3")

    # move head down
    if camCode[camCode_YPos] > threshold_down1:
        CamDown(QBO, distance_Y1, cam_speed_slow)
        ##print("Kopf nach unten bewegen 1")
    if camCode[camCode_YPos] > threshold_down2:
        CamDown(QBO, distance_Y2, cam_speed_medium)
        ##print("Kopf nach unten bewegen 2")
    if camCode[camCode_YPos] > threshold_down3:
        CamDown(QBO, distance_Y3, cam_speed_fast)
        ##print("Kopf nach unten bewegen 3")

    # move head up
    if camCode[camCode_YPos] < threshold_up1:
        CamUp(QBO, distance_Y1, cam_speed_slow)
        ##print("Kopf nach oben bewegen 1")
    if camCode[camCode_YPos] < threshold_up2:
        CamUp(QBO, distance_Y2, cam_speed_medium)
        ##print("Kopf nach oben bewegen 2")
    if camCode[camCode_YPos] < threshold_up3:
        CamUp(QBO, distance_Y3, cam_speed_fast)
        ##print("Kopf nach oben bewegen 3")
              
                    
# -------------------------------------------------------------------------------------------
# moves head left
# -------------------------------------------------------------------------------------------
def CamLeft(QBO, distance, speed ):                # To move left, we are provided a distance to move and a speed to move.
    
        global Xcoor, Xmin, touch_tm
        Xcoor = Xcoor - Kpx * distance
        
        if Xcoor < Xmin:
            Xcoor = Xmin
        
        QBO.SetServo(1, Xcoor, Ksp * speed)
        return

# -------------------------------------------------------------------------------------------
# moves head right
# -------------------------------------------------------------------------------------------
def CamRight(QBO, distance, speed):                   # Same logic as above
    
        global Xcoor, Xmax, touch_tm
        Xcoor = Xcoor + Kpx * distance
        
        if Xcoor > Xmax:
            Xcoor = Xmax
        
        QBO.SetServo(1, Xcoor, Ksp * speed)
        return
    
# -------------------------------------------------------------------------------------------
# moves head down
# -------------------------------------------------------------------------------------------
def CamDown(QBO, distance, speed):                   # Same logic as above
    
        global Ycoor, Ymax, touch_tm
        Ycoor = Ycoor + Kpy * distance
        
        if Ycoor > Ymax:
            Ycoor = Ymax
        
        QBO.SetServo(2, Ycoor, Ksp * speed)
        return
    
# -------------------------------------------------------------------------------------------
# moves head up
# -------------------------------------------------------------------------------------------
def CamUp(QBO, distance, speed):                     # Same logic as above
    
        global Ycoor, Ymin, touch_tm
        Ycoor = Ycoor - Kpy * distance
        
        if Ycoor < Ymin:
            Ycoor = Ymin
        
        QBO.SetServo(2, Ycoor, Ksp * speed)
        return
    
    