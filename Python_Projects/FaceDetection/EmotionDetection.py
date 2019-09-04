import cv2
import glob
import random
import numpy as np

emotions = ["neutral", "anger", "contempt", "disgust", "fear", "happy", "sadness", "surprise"] #Emotion list
fishface = cv2.face.FisherFaceRecognizer_create() #Initialize fisher face classifier
faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
data = {}

def decodeEmotion(pred):
    if pred == 0:
        return "neutral"
    elif pred == 1:
        return "anger"
    elif pred == 2:
        return "contempt"
    elif pred == 3:
        return "disgust"
    elif pred == 4:
        return "fear"
    elif pred == 5:
        return "happy"
    elif pred == 6:
        return "sadness"
    elif pred == 7:
        return "surprise"
    else:
        return "oh well, something went wrong..."

def get_files(emotion): #Define function to get file list, randomly shuffle it and split 80/20
    files = glob.glob("dataset\\%s\\*" %emotion)
    random.shuffle(files)
    training = files[:int(len(files)*0.8)] #get first 80% of file list
    prediction = files[-int(len(files)*0.2):] #get last 20% of file list
    return training, prediction

def make_sets():
    training_data = []
    training_labels = []
    prediction_data = []
    prediction_labels = []
    for emotion in emotions:
        training, prediction = get_files(emotion)
        #Append data to training and prediction list, and generate labels 0-7
        for item in training:
            image = cv2.imread(item) #open image
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) #convert to grayscale
            training_data.append(gray) #append image array to training data list
            training_labels.append(emotions.index(emotion))
        for item in prediction: #repeat above process for prediction set
            image = cv2.imread(item)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            prediction_data.append(gray)
            prediction_labels.append(emotions.index(emotion))
    return training_data, training_labels, prediction_data, prediction_labels

training_data, training_labels, prediction_data, prediction_labels = make_sets()
print("training fisher face classifier")
print("size of training set is:", len(training_labels), "images")


fishface.train(training_data, np.asarray(training_labels))

print("Training done")

# grab the reference to the webcam
vs = cv2.VideoCapture(0)

# keep looping
while True:
    # grab the current frame
    ret, frame = vs.read()

    # if we are viewing a video and we did not grab a frame,
    # then we have reached the end of the video
    if frame is None:
        break

    faces = faceCascade.detectMultiScale(frame)

    for (x, y, w, h) in faces:

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convert image to grayscale
        face = gray[y:y + h, x:x + w]  # Cut the frame to size
        face_two = cv2.resize(face, (350, 350))
        pred, conf = fishface.predict(face_two)

        emotion = decodeEmotion(pred)
        cv2.putText(frame, emotion, (x, y), cv2.FONT_HERSHEY_COMPLEX, 1.0, (255, 255, 255),
                        lineType=cv2.LINE_AA)


        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
    # show the frame to our screen
    cv2.imshow("Video", frame)
    key = cv2.waitKey(1) & 0xFF

    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break

# close all windows
cv2.destroyAllWindows()