import cv2
import math
import sys
import time
import requests
import base64
import pickle
import json
import serial
import QboCmd
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# -------------------------------------------------------------------------------------------
#set up ports for communicating with servos
# -------------------------------------------------------------------------------------------
port = '/dev/serial0'
ser = serial.Serial(port, baudrate=115200, bytesize = serial.EIGHTBITS, stopbits = serial.STOPBITS_ONE, parity = serial.PARITY_NONE, rtscts = False, dsrdtr =False, timeout = 0)
QBO = QboCmd.Controller(ser)

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
# keep looping endlessly and send camera frames to python backend service
# -------------------------------------------------------------------------------------------
while True:
    
    emotion = "unknown"
    
    # if no "current frame" available, we reached the videos end
    ret, frame = vs.read()
    if frame is None:
        continue
    
    # -----------------------------
    # show result in video stream
    # -----------------------------
    #cv2.putText(frame, emotion, (30, 30), cv2.FONT_HERSHEY_COMPLEX, 1.0, (255, 255, 255)) # draw at pos 20,20
    cv2.imshow("QBO Video", frame)
    
    # -----------------------------
    # reduce frames per second
    # -----------------------------
    if (time.time() - prevTime) > 1./frame_rate:
        prevTime = time.time()

        # -----------------------------
        # connect to python backend server
        # ----------------------------- 
        try:     
            r = requests.post('https://power2dm.salzburgresearch.at/robogen/FaceDetection/AnalyzeFrameForEmotion', verify=False, json=im2json(frame))
            #r = requests.post('https://power2dm.salzburgresearch.at/robogen/v1/api', verify=False, json={"name": "naren"})
            headers = {'Content-type': 'application/json'}
            print("--------------------------")
            print("Server-Antwort: " + str(r.status_code))
            
            if r.ok:
                print("Erkannte Emotion: " + str(r.content))
                print("--------------------------")
                emotion = r.content
            
            # set mouth
            setQBOMouth(emotion)
                    
        except requests.exceptions.RequestException as e:
            print e
              
    # -----------------------------
    # if the 'q' key is pressed, stop the loop
    # -----------------------------
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
    
    
