#!/usr/bin/env python
import cv2
import math
import sys
import ast
import time
import threading
import requests
import base64
import pickle
import json
import serial
import QboCmd

from ControlHeadAsync import *
from AutomaticFaceFollow import *

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# -------------------------------------------------------------------------------------------
#set up ports for communicating with servos
# -------------------------------------------------------------------------------------------
port = '/dev/serial0'
ser = serial.Serial(port, baudrate=115200, bytesize = serial.EIGHTBITS, stopbits = serial.STOPBITS_ONE, parity = serial.PARITY_NONE, rtscts = False, dsrdtr =False, timeout = 0)
QBO = QboCmd.Controller(ser)
QBO.SetNoseColor(QboCmd.nose_color_none) # init nose

# -------------------------------------------------------------------------------------------
# Set up required webcam object and variables for frame cutting and sampling
# -------------------------------------------------------------------------------------------
vs = cv2.VideoCapture(0)
vs.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 100)
vs.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 100)

frame_rate = 1
prevTime = 0


# -------------------------------------------------------------------------------------------
# helper function to pack image into a json string
# -------------------------------------------------------------------------------------------
def im2json(im):
    
    retval, buffer = cv2.imencode('.jpg', im)
    buffer64 = base64.b64encode(buffer)   
    return json.dumps({"image": buffer64})

# -------------------------------------------------------------------------------------------
# helper function to display mouths
# -------------------------------------------------------------------------------------------
def setQBOMouth(emotion, serverDown):
    
     # server down
    if serverDown:
        QBO.SetMouth(0x00000000) # all leds off
        return

    if emotion == "fear":     
        QBO.SetMouth(0x1f1f1f1f) # all leds on
    elif emotion == "happy":
        QBO.SetMouth(0x110e0000) #smile
    elif emotion == "neutral":
        QBO.SetMouth(0x1f1f00) #serious
    elif emotion == "pain":
        QBO.SetMouth(0x40e1f) #pyramide
    elif emotion == "sadness":
        QBO.SetMouth(0x0e1100) #sad
    elif emotion == "surprise":
        QBO.SetMouth(0x1f1b151f) #oval
    else:
        QBO.SetMouth(0x1b1f0e04) #love
        
# -------------------------------------------------------------------------------------------
# helper function to control nose color
# -------------------------------------------------------------------------------------------
def setQBONose(camCode, serverDown):
    
    # server down
    if serverDown:
        QBO.SetNoseColor(QboCmd.nose_color_none)  
        return
    
    # no face found
    if camCode[camCode_XPos] == 0 and camCode[camCode_YPos] == 0:
        QBO.SetNoseColor(QboCmd.nose_color_green)  
        return
    
    # face found
    QBO.SetNoseColor(QboCmd.nose_color_blue_dark)

		
# -------------------------------------------------------------------------------------------
# helper function to control head position
# -------------------------------------------------------------------------------------------
def setQBOHeadPos(camCode, serverDown):
    
    # server down
    if serverDown:
        return
    
    # no face found
    if camCode[camCode_XPos] == 0 and camCode[camCode_YPos] == 0:
        return
    
    # face found
    AdjustHeadPosition(QBO, camCode)


# -------------------------------------------------------------------------------------------
# keep looping until worker dies and send camera frames to python backend service
# -------------------------------------------------------------------------------------------
worker_thread = threading.Thread(target=controlQBOHead, args=("Thread-AsyncControl", vs, ser, QBO))
worker_thread.start()

emotion = ""
camCode = [0, 0]

while worker_thread.is_alive():  
    
    ret, frame = vs.read()

    # send request to python backend server 
    try:     
        r = requests.post('https://power2dm.salzburgresearch.at/robogen/FaceDetection/AnalyzeFrameForEmotion', verify=False, json=im2json(frame))
        headers = {'Content-type': 'application/json'}      
            
        if r.ok:
            emotion, strPos = r.content.split("-")
            camCode = ast.literal_eval(strPos)
            
            ##print("--------------------------")         
            ##print("Erkannte Emotion: " + emotion)
            ##print("Position des Gesichtes ist: " + strPos)
            ##print("--------------------------")                          
            
        else:
            print("--------------------------")
            print("Fehler bei Server-Antwort: " + str(r.status_code))
            print("--------------------------")
            
        # set mouth, nose and headPos
        setQBOMouth(emotion, not r.ok) # set mouth
        time.sleep(0.1) # wait for queue
        
        setQBONose(camCode, not r.ok) # set nose
        time.sleep(0.1) # wait for queue
        
	setQBOHeadPos(camCode, not r.ok) # set head position, dont sleep, will take long enough..
	
                    
    except requests.exceptions.RequestException as e:
        print e
    
    
