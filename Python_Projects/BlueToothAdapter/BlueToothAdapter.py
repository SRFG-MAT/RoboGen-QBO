#!/usr/bin/env python2.7
import os, sys, time
time.sleep(25) # wait for ubuntu bluetoothservice to be init (TODO: maybe change this to wait until service is ready)

import bluetooth
import subprocess

# saved settings
sys.path.append('/opt/QBO/RoboGen-QBO/Python_Projects/MyQBOSettings')
import SettingsReader

# -------------------------------------------------------------------------------------------
# defining criteria for listening socket
# -------------------------------------------------------------------------------------------
BUFF_SIZE = 4096 # 4 KiB
port = 1

# -------------------------------------------------------------------------------------------
# helper function: create the socket and bind to it
# -------------------------------------------------------------------------------------------
def createSocketAndBind():
    socket=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
    socket.bind(("",port))
    socket.listen(1)
    print("Socket created succesfully. Port is %i " % port)
    return socket

# -------------------------------------------------------------------------------------------
# helper function: wait for accepted socket
# -------------------------------------------------------------------------------------------
def waitForConnection(server_socket):
    print('Waiting for accepted connection...')
    client_socket,address = server_socket.accept()
    print("Accepted connection from ", address)
    return client_socket,address

# -------------------------------------------------------------------------------------------
# listen in endless loop
# -------------------------------------------------------------------------------------------
while True:
    server_socket = createSocketAndBind() 
    client_socket,address = waitForConnection(server_socket)   

    while True:
    
        try:
            data = None  
            req = client_socket.recv(BUFF_SIZE)
                
            # check for length
            if len(req) == 0: break
            elif len(req) == 1 and ord(req[0]) == 113: # 113 == 'q'
                print ("Shutdown Android Communication")
                server_socket.close()
                break        
                    
            # write json               
            SettingsReader.writeJsonFile(req)
            client_socket.send("Daten erfolgreich erhalten!")

        except IOError: pass
    
        except KeyboardInterrupt:         
            client_socket.close()
            client_socket.close()
            print "user forced close: cleanup all done"
            break
    
        except bluetooth.btcommon.BluetoothError as btError:      
            print('Lost accepted connection...')
            client_socket,address = waitForConnection(server_socket)
            continue
 
