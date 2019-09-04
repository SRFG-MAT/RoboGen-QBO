import bluetooth
import subprocess
import os

# -------------------------------------------------------------------------------------------
# helper function: wait for accepted socket
# -------------------------------------------------------------------------------------------
def waitForConnection(server_socket):
    print('Waiting for accepted connection...')
    client_socket,address = server_socket.accept()
    print("Accepted connection from ", address)
    return client_socket,address

# -------------------------------------------------------------------------------------------
# defining criteria for listening socket
# -------------------------------------------------------------------------------------------
server_socket=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
port = 1
server_socket.bind(("",port))
server_socket.listen(1)
print("Socket created succesfully. Port is %i " % port)

# wait for connection
client_socket,address = waitForConnection(server_socket)

# -------------------------------------------------------------------------------------------
# listen in endless loop
# -------------------------------------------------------------------------------------------
while True:
    
    try:
        data = client_socket.recv(1) # receive one char
    except bluetooth.btcommon.BluetoothError as btError:
        print('Lost accepted connection...')
        client_socket,address = waitForConnection(server_socket)
        continue
    
    # parse received command
    print ("Received: %s" % data)
  
    if (ord(data) == 1):
        print ("---------------------------------------------------------")
        print ("Start Q.bo mouth.py) all output will be redirected:")
        print ("---------------------------------------------------------")
        subprocess.call(['python', "../Control/mouth.py"])
        print ("---------------------------------------------------------")
        
        client_socket.send("OK1")
        
    elif (ord(data) == 2):
        print ("---------------------------------------------------------")
        print ("Start Q.bo head.py) all output will be redirected:")
        print ("---------------------------------------------------------")
        subprocess.call(['python', "../Control/head.py"])
        print ("---------------------------------------------------------")
        
        client_socket.send("OK2")
        
    elif (ord(data) == 3):
        print ("---------------------------------------------------------")
        print ("Start Q.bo FaceDetectionWebCamEmotionDetectionDlib.py) all output will be redirected:")
        print ("---------------------------------------------------------")
        os.chdir("../FaceDetection") # only works in its own folder
        subprocess.call(['python', "FaceDetectionWebCam.py"])
        os.chdir("../BlueToothAdapter") # switch back to BluetoothAdapter folder
        print ("---------------------------------------------------------")
        
        client_socket.send("OK3")
        
    elif (ord(data) == 4):
        print ("---------------------------------------------------------")
        print ("Start Q.bo EmotionSpeech.py) all output will be redirected:")
        print ("---------------------------------------------------------")
        os.chdir("../EmotionSpeech") # only works in its own folder
        subprocess.call(['python', "Main_Programm.py"])
        os.chdir("../BlueToothAdapter") # switch back to BluetoothAdapter folder
        print ("---------------------------------------------------------")
        
        client_socket.send("OK4")
  
    elif (ord(data) == 113): # 113 == 'q'
        print ("Shutdown Android Communication")
        break
 
client_socket.close()
server_socket.close()
