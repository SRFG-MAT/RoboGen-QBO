#!/usr/bin/env python
# coding=utf-8
import requests
import json
import base64

# -------------------------------------------------------------------------------------------
# uploadNutritionEntry
# -------------------------------------------------------------------------------------------
def uploadNutritionEntry(food, date, time, amount):
    
    data = {
        'food': food.encode('utf-8').strip(),
        'date': date.encode('utf-8').strip(),
        'time': time.encode('utf-8').strip(),
        'amount': amount.encode('utf-8').strip()
    }
    
    try:     
        r = requests.post('https://power2dm.salzburgresearch.at/robogen/DataBase/UploadJSON_MyNutrition', timeout=5, verify=False, json=data)
        headers = {'Content-type': 'application/json'}      
            
        if r.ok:
            print(r.content)
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
# resetNutritionDiary (reset full diary to null)
# send request to python backend server 
# -------------------------------------------------------------------------------------------
def resetNutritionDiary():
    
    try:     
        r = requests.post('https://power2dm.salzburgresearch.at/robogen/DataBase/ResetJSON_MyNutrition', timeout=5, verify=False, json='')
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



