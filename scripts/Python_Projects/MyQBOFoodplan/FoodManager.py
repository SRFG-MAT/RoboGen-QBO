#!/usr/bin/env python
# coding=utf-8
import requests
import json
import base64

food_endpoint = 'https://api.jsonstorage.net/v1/json/324bf60d-07e0-4098-9f4c-5fc40486e1c3'
add_entries = True

# -------------------------------------------------------------------------------------------
# uploadNutritionEntry
# -------------------------------------------------------------------------------------------
def uploadNutritionEntry(food, date, time, amount):
    
    data = {
        'food': food.encode('utf-8').strip(),
        'amount': amount.encode('utf-8').strip(),
        'date': date.encode('utf-8').strip(),
        'time': time.encode('utf-8').strip()
    }
    if (add_entries):
        data_old = downloadNutritionEntry()
        data_new = data_old.append(data)
    else:
        data_new = data
    
    try:     
        #r = requests.post('https://power2dm.salzburgresearch.at/robogen/DataBase/UploadJSON_MyNutrition', timeout=5, verify=False, json=data_new)
        r = requests.put(food_endpoint, timeout=5, verify=False, json=data)
        headers = {'Content-type': 'application/json'}      
            
        if r.ok:
            print("Mahlzeit gespeichert")
            return r.content

        else:
            print("--------------------------")
            print("Fehler bei Server-Antwort: " + str(r.status_code))
            print("--------------------------")
            return "ERROR"
                        
    except requests.exceptions.RequestException as e:
        print e
        
# -------------------------------------------------------------------------------------------
# downloadNutritionEntry (download full diary with all entries)
# send request to python backend server 
# -------------------------------------------------------------------------------------------
def downloadNutritionEntry():
    
    try:     
        r = requests.post('https://power2dm.salzburgresearch.at/robogen/DataBase/DownloadJSON_MyNutrition', timeout=5, verify=False, json='')
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
# resetNutritionDiary (reset full diary to null)
# send request to python backend server 
# -------------------------------------------------------------------------------------------
def resetNutritionDiary():
    
    try:     
        r = requests.post('https://power2dm.salzburgresearch.at/robogen/DataBase/ResetJSON_MyNutrition', timeout=5, verify=False, json='')
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



