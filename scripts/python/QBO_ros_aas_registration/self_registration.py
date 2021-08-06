#!/usr/bin/env python
# coding=utf-8
import requests
import json

#register one full AAS in asset-directory-controller under "/directory/aas" or one submodel under "/directory/submodel"

#---------------------------------------------------------------------------------------------
# loadAASType
#---------------------------------------------------------------------------------------------
def loadAASType():

    with open('/opt/QBO/catkin_ws/src/RoboGen-QBO/scripts/python/QBO_ros_aas_registration/QBO_type.json', 'r') as dt_file:
        dt_data = json.load(dt_file) 
        # TODO
    
    return dt_data

#---------------------------------------------------------------------------------------------
# loadAASInstance
#---------------------------------------------------------------------------------------------
def loadAASInstance():
    
    with open('/opt/QBO/catkin_ws/src/RoboGen-QBO/scripts/python/QBO_ros_aas_registration/QBO_instance.json', 'r') as dt_file:
        dt_data = json.load(dt_file) 
        # TODO
        
    return dt_data

# -------------------------------------------------------------------------------------------
# uploadAAS (upload full settings with all entries)
# -------------------------------------------------------------------------------------------
def uploadAAS(aas):
    
    try:     
        #r = requests.post('https://power2dm.salzburgresearch.at/robogen/DataBase/UploadJSON_MySettings', timeout=5, verify=False, json=aas)
        r = requests.put(settings_endpoint, timeout=5, verify=False, json=aas)
        headers = {'Content-type': 'application/json'}      
            
        if r.ok:
            print("Description uploaded succesfullly")
        else:
            print("--------------------------")
            print("Error in server response: " + str(r.status_code))
            print("--------------------------")
                        
    except requests.exceptions.RequestException as e:
        print e
        
#------------------------------------------------------------------------------------------------------------------------------------------------------------
# main function
#------------------------------------------------------------------------------------------------------------------------------------------------------------	 
if __name__ == '__main__':
    
    aas_type = loadAASType()
    aas_instance = loadAASInstance()
    uploadAAS(aas_type)
    uploadAAS(aas_instance)
    
    
    
    