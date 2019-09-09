import cv2
import numpy as np
import dlib
from sklearn.svm import SVC
import math
import sys
from sklearn.externals import joblib
from scipy.stats import mode
import pickle
import time

# -------------------------------------------------------------------------------------------
# Set up face detection variables
# -------------------------------------------------------------------------------------------
faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat") #Or set this to whatever you named the downloaded file
clf = SVC(kernel='linear', probability=True, tol=1e-3)#, verbose = True) #Set the classifier as a support vector machines with polynomial kernel
data = {} #Make dictionary for all values

#clf = joblib.load("EmotionPredictionModel_All.sav")
#clf = joblib.load("EDModel.sav")
clf = pickle.load( open("EmotionPredictionModel_All.p", "rb"))
list_of_current_emotions = []

# -------------------------------------------------------------------------------------------
# Set up some required webcam object and change size of images
# -------------------------------------------------------------------------------------------
vs = cv2.VideoCapture(0)
vs.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 400)
vs.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 400)

# -------------------------------------------------------------------------------------------
# helpers needed to reduce frames per second
# -------------------------------------------------------------------------------------------
frame_rate = 5
prev = 0

# -------------------------------------------------------------------------------------------
# function decodeEmotion
# -------------------------------------------------------------------------------------------
def decodeEmotion(pred):
    if pred == 0:
        return "fear"
    elif pred == 1:
        return "happy"
    elif pred == 2:
        return "neutral"
    elif pred == 3:
        return "pain"
    elif pred == 4:
        return "sadness"
    elif pred == 5:
        return "surprise"
    else:
        return "oh well, something went wrong..."

# -------------------------------------------------------------------------------------------
# function get_landmarks_for_classification
# -------------------------------------------------------------------------------------------
def get_landmarks_for_classification(image):
    detections = detector(image, 1)

    for k, d in enumerate(detections): #For all detected face instances individually
        shape = predictor(image, d) #Draw Facial Landmarks with the predictor class
        xlist = []
        ylist = []
        for i in range(1, 68): #Store X and Y coordinates in two lists
            xlist.append(float(shape.part(i).x))
            ylist.append(float(shape.part(i).y))
        xmean = np.mean(xlist)
        ymean = np.mean(ylist)
        xcentral = [(x-xmean) for x in xlist]
        ycentral = [(y-ymean) for y in ylist]
        landmarks_vectorised = []
        for x, y, w, z in zip(xcentral, ycentral, xlist, ylist):
            landmarks_vectorised.append(w)
            landmarks_vectorised.append(z)
            meannp = np.asarray((ymean, xmean))
            coornp = np.asarray((z, w))
            dist = np.linalg.norm(coornp-meannp)
            landmarks_vectorised.append(dist)
            landmarks_vectorised.append((math.atan2(y, x)*360)/(2*math.pi))
            #print(len(landmarks_vectorised))
        return landmarks_vectorised

# -------------------------------------------------------------------------------------------
# keep looping endlessly to find 
# -------------------------------------------------------------------------------------------
while True:  

    # reduce frames per second
    if (time.time() - prev) > 1./frame_rate:
        prev = time.time()
        
        # grab the current frame
        # if we did not get a frame, we have reached the videos end
        ret, frame = vs.read()
        if frame is None:
            continue

        faces = faceCascade.detectMultiScale(frame)
        
        for (x, y, w, h) in faces:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convert image to grayscale
            face = gray[y:y + h, x:x + w]  # Cut the frame to size
            face_two = cv2.resize(face, (350, 350))
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            clahe_image = clahe.apply(face_two)
            features = np.array(get_landmarks_for_classification(clahe_image))
            features = np.reshape(features, (1, -1))
            
            if len(features[0]) < 100:
                continue

            prediction = clf.predict(features)
            list_of_current_emotions.append(prediction)
            
            if len(list_of_current_emotions) > 5:
                list_of_current_emotions.pop(0)

            int_emotion = mode(list_of_current_emotions)[0]
            emotion = decodeEmotion(int_emotion)

            cv2.putText(frame, emotion, (x, y), cv2.FONT_HERSHEY_COMPLEX, 1.0, (255, 255, 255))
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        cv2.imshow("Video", frame)
        key = cv2.waitKey(1) & 0xFF

    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break