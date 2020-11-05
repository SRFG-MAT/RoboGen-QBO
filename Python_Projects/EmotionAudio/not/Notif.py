#!/usr/bin/env python
# coding=utf-8
import os, sys
import Processing_Audio
import Various_Functions
import smtplib


def startNotif(userName,emergencyMail):
    
    Various_Functions.qboSpeak('Ich habe verstanden, dass du eine Benachrichtigung an deine Kontaktperson senden willst. Bitte nenne jetzt deinen Benachrichtigungstext.')
    sentence = Processing_Audio.getAudioToText()
    sentence = Various_Functions.normalize(sentence)
    Various_Functions.qboSpeak('Vielen Dank. Ich werde deine Nachricht sofort an deine Kontaktperson senden.')
	processNotif(userName,sentence,emergencyMail)
            
    
    
#---------------------------------------------------------------------------------------------
# helper function to handle the mail sending  
#---------------------------------------------------------------------------------------------
def processNotif(userName,sentence,emergencyMail):
    
	s = smtplib.SMTP('smtp.gmail.com', 587) 
	s.starttls() 
	s.login("qbo.emergency@gmail.com", "qboEmergencyPass321!") 
	SUBJECT = "Benachrichtigung von "+userName
	TEXT = "Benachrichtigung von "+userName+":\n\n"+sentence
	message = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)
	s.sendmail("qbo.emergency@gmail.com", emergencyMail, message) 
	s.quit() 
