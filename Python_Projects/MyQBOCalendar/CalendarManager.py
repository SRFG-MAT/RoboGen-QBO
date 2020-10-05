#!/usr/bin/env python
# coding=utf-8
import requests
import json
import base64

# -------------------------------------------------------------------------------------------
# uploadCalendarEntry
# -------------------------------------------------------------------------------------------
def uploadCalendarEntry(title, date, time, reminder, repeat):
    
    data = {
        'title': title.encode('utf-8').strip(),
        'date': date.encode('utf-8').strip(),
        'time': time.encode('utf-8').strip(),
        'reminder': reminder.encode('utf-8').strip(),
        'repeat': repeat.encode('utf-8').strip()
    }
    json_data = json.dumps(data)
    
    try:     
        r = requests.post('https://power2dm.salzburgresearch.at/robogen/DataBase/UploadJSON_MyCalendar', timeout=5, verify=False, json=json_data)
        headers = {'Content-type': 'application/json'}      
            
        if r.ok:
            print(r.content)
        else:
            print("--------------------------")
            print("Fehler bei Server-Antwort: " + str(r.status_code))
            print("--------------------------")
                        
    except requests.exceptions.RequestException as e:
        print e
        
# -------------------------------------------------------------------------------------------
# downloadCalendarEntry (download full calender with all entries)
# send request to python backend server 
# -------------------------------------------------------------------------------------------
def downloadCalendarEntry():
    
    try:     
        r = requests.post('https://power2dm.salzburgresearch.at/robogen/DataBase/DownloadJSON_MyCalendar', timeout=5, verify=False, json='')
        headers = {'Content-type': 'application/json'}      
            
        if r.ok:
            print(r.content)
            return r.content
        else:
            print("--------------------------")
            print("Fehler bei Server-Antwort: " + str(r.status_code))
            print("--------------------------")
            return "Error"
                        
    except requests.exceptions.RequestException as e:
        print e
        
# -------------------------------------------------------------------------------------------
# resetCalendar (reset full calender to null)
# send request to python backend server 
# -------------------------------------------------------------------------------------------
def resetCalendar():
    
    try:     
        r = requests.post('https://power2dm.salzburgresearch.at/robogen/DataBase/ResetJSON_MyCalendar', timeout=5, verify=False, json='')
        headers = {'Content-type': 'application/json'}      
            
        if r.ok:
            print(r.content)
            return True
        else:
            print("--------------------------")
            print("Fehler bei Server-Antwort: " + str(r.status_code))
            print("--------------------------")
            return False
                        
    except requests.exceptions.RequestException as e:
        print e



