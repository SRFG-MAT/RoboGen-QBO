import cv2
import dlib
import time

# -------------------------------------------------------------------------------------------
# Set up some required webcam object and change size of images
# -------------------------------------------------------------------------------------------
video_capture = cv2.VideoCapture(0)
video_capture.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 400)
video_capture.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 400)
#video_capture.set(cv2.cv.CV_CAP_PROP_FRAME_COUNT, 2) # TODO: does not seem to be supported by camera

# -------------------------------------------------------------------------------------------
# Set up face detector and landmark identifier
# -------------------------------------------------------------------------------------------
detector = dlib.get_frontal_face_detector()                               # Face detector
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat") # Landmark identifier

# -------------------------------------------------------------------------------------------
# helpers needed to reduce frames per second
# -------------------------------------------------------------------------------------------
frame_rate = 10
prev = 0

# -------------------------------------------------------------------------------------------
# run in loop and read frames until user presses q
# -------------------------------------------------------------------------------------------
while True:
  
    # reduce frames per second
    if (time.time() - prev) > 1./frame_rate:
        prev = time.time()
    
        # get image and set image params
        ret, frame = video_capture.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        clahe_image = clahe.apply(gray)
 
        # init detector
        detections = detector(clahe_image, 0) # Detect the faces in the image
    
        # for each detected face, get coordinates
        for k,d in enumerate(detections):
            shape = predictor(clahe_image, d)
            
            # for each landmark point on a face (68 per face), draw a red circle on the frame
            for i in range(1,68): 
                cv2.circle(frame, (shape.part(i).x, shape.part(i).y), 1, (0,0,255), thickness=2)
            
        cv2.imshow("Video", frame) #Display the frame
    
    if cv2.waitKey(1) & 0xFF == ord('q'): #Exit program when the user presses 'q'
        break
    