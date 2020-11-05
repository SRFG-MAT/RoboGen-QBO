#!/usr/bin/env python
# coding=utf-8
import os, sys
import Various_Functions
import smtplib
from email.mime.text import MIMEText as text

def startEmergency(userName,emergencyMail):

    Various_Functions.qboSpeak('Ich habe verstanden, dass ein Notfall vorliegt und werde sofort eine Nachricht an deine Kontaktperson senden.')
    processEmergency(userName,emergencyMail)

#---------------------------------------------------------------------------------------------
# helper function to handle the mail sending  
#---------------------------------------------------------------------------------------------
def processEmergency(userName,emergencyMail):

    s = smtplib.SMTP('smtp.gmail.com', 587) 
    s.starttls() 
    s.login("qbo.emergency@gmail.com", "qboEmergencyPass321!") 
    SUBJECT = "Notfall bei "+userName
    TEXT = "Notfall bei "+userName+"!\n\nSofort pruefen!"
    FROM = "QBO Mail"
    m = text(TEXT)
    m['Subject'] = SUBJECT
    m['From'] = FROM
    s.sendmail("qbo.emergency@gmail.com", emergencyMail, m.as_string()) 
    s.quit() 
