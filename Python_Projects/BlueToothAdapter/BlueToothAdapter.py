import bluetooth
import subprocess
import os, sys

# saved settings
sys.path.append('/home/pi/Documents/RoboGen-QBO/Python_Projects/MyQBOSettings')
import SettingsReader

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
BUFF_SIZE = 4096 # 4 KiB


# -------------------------------------------------------------------------------------------
# listen in endless loop
# -------------------------------------------------------------------------------------------
while True:
    
    try:
        data = None  
        req = client_socket.recv(BUFF_SIZE)
                
        # check for length
        if len(req) == 0: break
        elif len(req) == 1 and ord(req[0]) == 113: # 113 == 'q'
            print ("Shutdown Android Communication")
            sys.exit()
                
        # check if send response             
        if req in ('temp', '*temp'):
            data = str(random.random())+'!'            
            client_socket.send(data)
            #print "sending [%s]" % data
                    
        # write json               
        SettingsReader.writeJsonFile(req)

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
 
