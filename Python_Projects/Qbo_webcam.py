#!/usr/bin/env python2

############################################################### 
# Qbo_webcam.py
#
# Based upon "Face Detection in Python Using a Webcam"
# (https://realpython.com/face-detection-in-python-using-a-webcam/)
# and "OpenQbo v3.0" (https://gitlab.com/thecorpora/QBO)
#
# 1. Connect to Q.bo using VNC
# 2. Copy this file Qbo_webcam.py to the /home/pi/ directory
# 3. Press Ctrl+Alt+T to open a terminal
# 4. Enter
#    sudo pkill python
#    sudo pkill chromium
# 5. Enter
#    python Qbo_webcam.py
#
# Press 'q' to quit.
#
# Visual aid:
#    Green rectangles are detected frontal faces
#    Blue rectangles are detected profile faces
###############################################################

import yaml
import cv2
import logging as log
import time
import datetime as dt
from time import sleep

# Initialize logging
log.basicConfig(filename='Qbo_webcam.log',level=log.INFO)

# Load configuration
config = yaml.safe_load(open("/opt/qbo/config.yml"))

# Initialize vision
webcam = cv2.VideoCapture(int(config['camera']))  # Get ready to start getting images from the webcam
webcam.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 320)   # I have found this to be about the highest-
webcam.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 240)  # resolution you'll want to attempt on the pi
#webcam.set(cv2.CV_CAP_PROP_BUFFERSIZE, 2)		   # frame buffer storage

frontal_face = cv2.CascadeClassifier("/opt/qbo/haarcascades/haarcascade_frontalface_alt2.xml")  # frontal face pattern detection
profile_face = cv2.CascadeClassifier("/opt/qbo/haarcascades/haarcascade_profileface.xml")       # side face pattern detection

frontal_anterior = 0
profile_anterior = 0

while True:
    if not webcam.isOpened():
        log.error('Unable to load camera.')
        sleep(5)
        pass

    # Wait for present frame
    t_ini = time.time()
    while time.time() - t_ini < 0.01:  # wait for present frame
		t_ini = time.time()
		ret, frame = webcam.read()

    # Capture frame-by-frame
    #ret, frame = webcam.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    frontal_faces = frontal_face.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=4,
        minSize=(60, 60),
        flags = cv2.cv.CV_HAAR_DO_CANNY_PRUNING + cv2.cv.CV_HAAR_FIND_BIGGEST_OBJECT + cv2.cv.CV_HAAR_DO_ROUGH_SEARCH
    )

    profile_faces = profile_face.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=4,
        minSize=(80, 80),
        flags = cv2.cv.CV_HAAR_DO_CANNY_PRUNING + cv2.cv.CV_HAAR_FIND_BIGGEST_OBJECT + cv2.cv.CV_HAAR_DO_ROUGH_SEARCH
    )

    # Draw a green rectangle around detected frontal faces
    for (x, y, w, h) in frontal_faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
    # Draw a blue rectangle around detected profile faces
    for (x, y, w, h) in profile_faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

    # Log how many faces we saw
    if frontal_anterior != len(frontal_faces) or profile_anterior != len(profile_faces):
        frontal_anterior = len(frontal_faces)
        profile_anterior = len(profile_faces)
        log.info("Frontal faces: "+str(len(frontal_faces))+", Profile faces: "+str(len(profile_faces))+" at "+str(dt.datetime.now()))

    # Display the resulting frame
    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Display the resulting frame
    cv2.imshow('Video', frame)

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()