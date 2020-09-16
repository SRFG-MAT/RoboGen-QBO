#!/usr/bin/env python
# coding=utf-8
import os, json
from datetime import date

filepath_food = '/opt/QBO/RoboGen-QBO/Python_Projects/MyQBOFoodplan/food.json'
filepath_mycalendar = '/opt/QBO/RoboGen-QBO/Python_Projects/MyQBOFoodplan/mycalendar.txt'

# -------------------------------------------------------------------------------------------
# search the nutrition table for the food search term
# -------------------------------------------------------------------------------------------
def searchFoodArray(searchTerm):
    
    entries = []
    
    with open(filepath_food, 'r') as dt_file:
        dt_data = json.load(dt_file)
        
        i = 0
        for entry in dt_data:
             
            if entry['Lebensmittel'].lower() == searchTerm:
                entries.append(entry['Lebensmittel'])
                print ("Gefunden: " + entry['Lebensmittel'])
                
            i = i + 1
        
    return entries

# -------------------------------------------------------------------------------------------
# create JSON calendar entry
# -------------------------------------------------------------------------------------------
def createCalendarEntry(food):
    
    today = date.today()
    str = "[" + today.strftime("%d/%m/%Y") + "]: " + food + "\n"
    
    file = open(filepath_mycalendar, "a") # 'a' -> append for writing if exists
    file.write(str) 
    file.close() 
    