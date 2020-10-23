#!/usr/bin/env python2.7
import os, sys, time
time.sleep(25) # wait for ubuntu bluetoothservice to be init (TODO: maybe change this to wait until service is ready)

import bluetooth
import subprocess

# -------------------------------------------------------------------------------------------
# defining criteria for listening socket
# -------------------------------------------------------------------------------------------
BUFF_SIZE = 1024 # 1 KiB
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
            req = client_socket.recv(BUFF_SIZE)
            
            if len(req) == 1 and ord(req[0]) == 113: # 113 == 'q'
                print ("Shutdown Android Communication")
                server_socket.close()
                break
            elif req == "LEFT":
                print("TODO: Drive to the LEFT now")
                client_socket.send("Roboter versucht nach LINKS zu fahren...")
                server_socket.close()
                break
            elif req == "UP":
                print("TODO: Drive FORWARD now")
                client_socket.send("Roboter versucht nach VORNE zu fahren...")
                server_socket.close()
                break
            elif req == "DOWN":
                print("TODO: Drive BACKWARD now")
                client_socket.send("Roboter versucht nach HINTEN zu fahren...")
                server_socket.close()
                break
            elif req == "RIGHT":
                print("TODO: Drive to the RIGHT now")
                client_socket.send("Roboter versucht nach RECHTS zu fahren...")
                server_socket.close()
                break

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
                     
    
 
