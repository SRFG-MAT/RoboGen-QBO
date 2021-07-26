#!/usr/bin/env python3

############################################################### 
# Qbo_face_detect_and_track.py
#
# Based upon "Face Detection in Python Using a Webcam"
# (https://realpython.com/face-detection-in-python-using-a-webcam/),
# and "OpenCV Object Tracking"
# (https://www.pyimagesearch.com/2018/07/30/opencv-object-tracking/)
# and "Increasing webcam FPS with Python and OpenCV"
# (https://www.pyimagesearch.com/2015/12/21/increasing-webcam-fps-with-python-and-opencv/)
# and "OpenQbo v3.0" (https://gitlab.com/thecorpora/QBO)
#
# 1. Connect to Q.bo using VNC
# 2. Copy this file Qbo_face_detect_and_track.py to the /home/pi/ directory
# 3. Press Ctrl+Alt+T to open a terminal
# 4. Enter
#    sudo pkill python
#    sudo pkill chromium
# 5. Enter
#    sudo apt-get install libjasper-dev
#    sudo apt-get install libqtgui4
#    sudo apt-get install libqt4-test
#    sudo pip3 install pyyaml
#    sudo pip3 install imutils
#    sudo pip3 install opencv-contrib-python
#    sudo pip3 install opencv-contrib-python
#    sudo pip3 install imutils
# 6. Enter
#    python3 Qbo_face_detect_and_track.py
#
# Press 'q' to quit.
#
# We need to have a recent OpenCV available for Python3 because of the used tracker CSRT
# or 'Discriminative Correlation Filter (with Channel and Spatial Reliability)'
# which requires minimum OpenCV 3.4.2)
###############################################################

from imutils.video import FPS
import logging as log
import imutils
import yaml
import time
import cv2


VISION_FRAME_WIDTH = 320              # Highest resolution that tested out well
VISION_FRAME_HEIGHT = 240
VISION_MAX_FACE_TRACKING_FRAMES = 50  # 50 frames (about 10 seconds) tracking then redetect face


# Initialize logging
log.basicConfig(
    filename='Qbo_face_detect_and_track.log',
    level=log.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
log.info('Initialized logging')

# Load configuration
log.info('Reading /opt/qbo/config.yml')
qbo_config = yaml.safe_load(open("/home/pi/Documents/configQbo_GTK/config.yml"))

# Get ready to start getting images from the webcam
log.info('Starting the webcam thread')
vision_webcam = cv2.VideoCapture(int(qbo_config['camera']))        # Initialize webcam on configured source
vision_webcam.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, VISION_FRAME_WIDTH)    # Set webcam frame width
vision_webcam.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, VISION_FRAME_HEIGHT)  # Set webcam frame height

# Allow the camera to startup
time.sleep(2)

# Start the FPS counter
log.info('Starting the frames per second counter')
vision_fps = FPS().start()

# Setup face detectors (frontal face detection and pofile face detection)
log.info('Setup cascade classifier frontal face detection (/home/pi/Documents/Python projects/haarcascade_frontalface_alt2.xml)')
vision_face_frontal = cv2.CascadeClassifier('/home/pi/Documents/Python projects/haarcascade_frontalface_alt2.xml')  # frontal face pattern detection
log.info('Setup cascade classifier profile face detection (/home/pi/Documents/Python projects/haarcascade_profileface.xml')
vision_face_profile = cv2.CascadeClassifier('/home/pi/Documents/Python projects/haarcascade_profileface.xml')       # side face pattern detection

# Initialization face detection
vision_face_tracking_frames = 0      # Are we tracking a face? If yes, how many more frames to track without redetection
vision_face_tracker = None           # Place holder for face tracker once detected
vision_face_bounding_box = None      # Place holder for face bounding box (rectangle) if found
vision_face_frontal_detection = True # Start by detecting a frontal face

# Main endless loop
while True:
    # Get the next frame
    successful, vision_frame = vision_webcam.read()
    if not successful:
        log.error('Not successful grabbing a frame, skipping and try again')
        pass
    
    # Aren't we tracking a face already?
    if not vision_face_tracking_frames:

        # We are not tracking a face, try detecting a face

        # For now, we are only interested in the 'largest'
        # face, and we determine this based on the largest
        # area of the found bounding_box. First initialize the
        # required variables to 0
        vision_face_max_area = 0
        vision_face_bounding_box = None
        
        # Convert to gray for faster processing
        vision_frame_gray = cv2.cvtColor(vision_frame, cv2.COLOR_BGR2GRAY)

        if vision_face_frontal_detection:
            # Detect a frontal face
            log.debug('Detecting a frontal face')
            faces = vision_face_frontal.detectMultiScale(
                vision_frame_gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30)
            )
        else:
            # Detect a profile face
            log.debug('Detecting a profile face')
            faces = vision_face_profile.detectMultiScale(
                vision_frame_gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30)
            )
    
        # Did we detect frontal faces ...
        if not len(faces):
            # .... no, try another face detection next time
            vision_face_frontal_detection = not vision_face_frontal_detection
        else:
            # ... yes, log
            log.debug('Face(s) found')

            # Loop over all faces and check if the area for this
            # face is the largest so far
            for (_x, _y, _w, _h) in faces:
                if  _w * _h > vision_face_max_area:
                    vision_face_max_area = _w * _h
                    vision_face_bounding_box = (_x, _y, _w, _h)

            # Initialize the tracker on the largest face in the picture
            if vision_face_max_area > 0:
                # Initialize face we are going to track
                log.debug('Initialize face tracker')
                # Experiment between
                #     cv2.TrackerCSRT_create        # Tends to be more accurate than KCF but slightly slower.
                #     cv2.TrackerKCF_create         # Faster than BOOSTING and MIL. Similar to MIL and KCF, does not handle full occlusion well.
                #     cv2.TrackerBoosting_create    # This tracker is slow and does not work very well.
                #     cv2.TrackerMIL_create         # Better accuracy than BOOSTING tracker but does a poor job of reporting failure.
                #     cv2.TrackerTLD_create         # Incredibly prone to false-positives.
                #     cv2.TrackerMedianFlow_create  # Does a nice job reporting failures; however, if there is too large of a jump in motion, the model will fail.
                #     cv2.TrackerMOSSE_create       # Very, very fast. Not as accurate as CSRT or KCF but a good choice if you need pure speed.
                vision_face_tracker = cv2.TrackerCSRT_create()
                #vision_face_tracker = cv2.face.createLBPHFaceRecognizer()
                if vision_face_tracker.init(vision_frame, vision_face_bounding_box):
                    vision_face_tracking_frames = VISION_MAX_FACE_TRACKING_FRAMES

    else:

        # We are tracking a face!

    	# Get the new bounding_box of the object
        log.debug('Trying to track detected face')
        (successful, vision_face_bounding_box) = vision_face_tracker.update(vision_frame)

        # If a face is detected draw a green bounding_box on the frame
        if successful:
            # Calculate remainder of frames to track before automatic redetection
            vision_face_tracking_frames = vision_face_tracking_frames - 1

            # Draw a green bounding_box around detected face
            log.debug('Tracked the face, ' + str(vision_face_tracking_frames) + ' frames to track before auto-redetection')
            (_x, _y, _w, _h) = [int(_v) for _v in vision_face_bounding_box]
            cv2.rectangle(vision_frame, (_x, _y), (_x + _w, _y + _h), (0, 255, 0), 2)
        else:
            # We lost the face, redetect
            vision_face_tracking_frames = 0


    # Display the resulting frame
    cv2.imshow('Video', vision_frame)

    # If the 'q' key was pressed, break from the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        log.info('Stopping because the q key was pressed')
        break

    # Update the FPS counter
    vision_fps.update()

# Stop the timer and display FPS information
vision_fps.stop()
log.info('Elapsed time: {:.2f}'.format(vision_fps.elapsed()))
log.info('Vision approx. FPS: {:.2f}'.format(vision_fps.fps()))

# When everything is done, release the capture
cv2.destroyAllWindows()

log.info('Script ended')