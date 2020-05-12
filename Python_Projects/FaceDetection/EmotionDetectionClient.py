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
from ControlHead import *
from AutomaticFaceFollow import *
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# -------------------------------------------------------------------------------------------
#set up ports for communicating with servos
# -------------------------------------------------------------------------------------------
port = '/dev/serial0'
ser = serial.Serial(port, baudrate=115200, bytesize = serial.EIGHTBITS, stopbits = serial.STOPBITS_ONE, parity = serial.PARITY_NONE, rtscts = False, dsrdtr =False, timeout = 0)
QBO = QboCmd.Controller(ser)
QBO.SetNoseColor(0) # init nose

# -------------------------------------------------------------------------------------------
# Set up required webcam object and variables for frame cutting and sampling
# -------------------------------------------------------------------------------------------
vs = cv2.VideoCapture(0)
vs.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 100)
vs.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 100)

frame_rate = 1
prevTime = 0


## nose colors
nose_color_none = 0
nose_color_blue_dark = 3
nose_color_green = 4
nose_color_blue_light = 5


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
def setQBOMouth(emotion):

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
def setQBONose(camCode):
    
    # no face found
    if camCode[camCode_XPos] == 0 and camCode[camCode_YPos] == 0:
        QBO.SetNoseColor(nose_color_none)  
        return
    
    # face found
    QBO.SetNoseColor(nose_color_blue_dark)

		
# -------------------------------------------------------------------------------------------
# helper function to control head position
# -------------------------------------------------------------------------------------------
def setQBOHeadPos(camCode):
    
    # no face found
    if camCode[camCode_XPos] == 0 and camCode[camCode_YPos] == 0:
        return
    
    # face found
    AdjustHeadPosition(QBO, camCode)


# -------------------------------------------------------------------------------------------
# keep looping until worker dies and send camera frames to python backend service
# -------------------------------------------------------------------------------------------
worker_thread = threading.Thread(target=controlQBOHead, args=("Thread-1", vs, ser, QBO))
worker_thread.start()

while worker_thread.is_alive():
    
    emotion = ""
    camCode = [0, 0]
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
            
        ##else:
            ##print("--------------------------")
            ##print("Fehler bei Server-Antwort: " + str(r.status_code))
            ##print("--------------------------")
            
        # set mouth, nose and headPos
        setQBOMouth(emotion) # set mouth
        time.sleep(0.1) # wait for queue
        
        setQBONose(camCode) # set nose
        time.sleep(0.1) # wait for queue
        
	setQBOHeadPos(camCode) # set head position
	time.sleep(0.1) # wait for queue
                    
    except requests.exceptions.RequestException as e:
        print e
    
    
