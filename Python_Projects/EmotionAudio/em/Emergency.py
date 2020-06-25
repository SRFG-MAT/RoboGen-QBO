#!/usr/bin/env python
# coding=utf-8
import os, sys
import Various_Functions
import smtplib


def startEmergency(userName,emergencyMail):
    
	Various_Functions.qboSpeak('Ich habe verstanden, dass ein Notfall vorliegt und werde sofort eine Nachricht an deinen Notfallkontakt senden.')
	processEmergency(userName,emergencyMail)
            
    
    
#---------------------------------------------------------------------------------------------
# helper function to handle the mail sending  
#---------------------------------------------------------------------------------------------
def processEmergency(userName,emergencyMail):
    
	s = smtplib.SMTP('smtp.gmail.com', 587) 
	s.starttls() 
	s.login("qbo.emergency@gmail.com", "qboEmergencyPass321!") 
	message = "Notfall bei "+userName+"! Sofort pruefen!"
	s.sendmail("qbo.emergency@gmail.com", emergencyMail, message) 
	s.quit() 
