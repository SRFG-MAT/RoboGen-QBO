import cv2
import math
import sys
import time
import requests
import base64
import pickle
import json

# -------------------------------------------------------------------------------------------
# Set up required webcam object and variables for frame cutting and sampling
# -------------------------------------------------------------------------------------------
vs = cv2.VideoCapture(0)
vs.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 100)
vs.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 100)

frame_rate = 10
prevTime = 0


def im2json(im):
    """Convert a Numpy array to JSON string"""
    imdata = pickle.dumps(im)
    jstr = json.dumps({"image": base64.b64encode(imdata).decode('ascii')})
    return jstr

# -------------------------------------------------------------------------------------------
# keep looping endlessly and send camera frames to python backend service
# -------------------------------------------------------------------------------------------
# 0 "fear"
# 1 "happy"
# 2 "neutral"
# 3 "pain"
# 4 "sadness"
# 5 "surprise"
# else "oh well, something went wrong..."
# -------------------------------------------------------------------------------------------
while True:
    
    emotion = "unknown"

    # -----------------------------
    # reduce frames per second
    # -----------------------------
    if (time.time() - prevTime) > 1./frame_rate:
        prevTime = time.time()
        
        # if no "current frame" available, we reached the videos end
        ret, frame = vs.read()
        if frame is None:
            continue

        # -----------------------------
        # connect to python backend server
        # -----------------------------
        try:
            jstr = im2json(frame)
            
            r = requests.post('https://power2dm.salzburgresearch.at/robogen/FaceDetection/AnalyzeFrameForEmotion', verify=False, json=jstr) #TODO: support multiple faces!!!
            #r = requests.post('https://power2dm.salzburgresearch.at/robogen/v1/api', verify=False, json={"name": "naren"})
            headers = {'Content-type': 'application/json'}
            print(r.status_code)
            
            if r.ok:
                print r.content
                emotion = r.content
                    
        except requests.exceptions.RequestException as e:
            print e
        
        # -----------------------------
        # show result in video stream
        # -----------------------------
        cv2.putText(frame, emotion, (30, 30), cv2.FONT_HERSHEY_COMPLEX, 1.0, (255, 255, 255)) # draw at pos 20,20
        cv2.imshow("Video", frame)
        key = cv2.waitKey(1) & 0xFF

    # -----------------------------
    # if the 'q' key is pressed, stop the loop
    # -----------------------------
    if key == ord("q"):
        break
    
    
