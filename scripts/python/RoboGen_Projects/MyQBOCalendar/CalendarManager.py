#!/usr/bin/env python
# coding=utf-8
import requests
import json
import base64

calendar_endpoint = 'https://api.jsonstorage.net/v1/json/547520b2-1b42-4451-86df-dcff1e6d3d8c'
add_entries = True

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
    if (add_entries):
        data_old = json.loads(downloadCalendarEntry())
        data_old.append(data)
        data_new = data_old
    else:
        data_new = data
    
    try:     
        #r = requests.post('https://power2dm.salzburgresearch.at/robogen/DataBase/UploadJSON_MyCalendar', timeout=5, verify=False, json=data_new)
        r = requests.put(calendar_endpoint, timeout=5, verify=False, json=data_new)
        headers = {'Content-type': 'application/json'}      
            
        if r.ok:
            print("Kalender gespeichert")
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
        #r = requests.post('https://power2dm.salzburgresearch.at/robogen/DataBase/DownloadJSON_MyCalendar', timeout=5, verify=False, json='')
        r = requests.get(calendar_endpoint, timeout=5, verify=False, json='')
        headers = {'Content-type': 'application/json'}      
            
        if r.ok:
            #print(r.content)
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
            #print(r.content)
            return True
        else:
            print("--------------------------")
            print("Fehler bei Server-Antwort: " + str(r.status_code))
            print("--------------------------")
            return False
                        
    except requests.exceptions.RequestException as e:
        print e



