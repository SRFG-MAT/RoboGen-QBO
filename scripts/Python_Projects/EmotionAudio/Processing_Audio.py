#!/usr/bin/env python
# coding=utf-8

import speech_recognition as sr

from ctypes import *
import pyaudio

# speech-to-text source, can be "Google" or "IBM"
stt_src = "Google"
# IBM keys v1
ibm_api_key = "qHTNcaz_aCi4vf-uqnCSMwc1Gn7Yl3PB-bWQ-lM47TAj"
ibm_url = "https://api.eu-de.speech-to-text.watson.cloud.ibm.com/instances/2c390da0-ee03-4b16-af63-f6a9547335ce/v1/recognize?model=de-DE_BroadbandModel"
# IBM keys v2
#ibm_api_key = "MDlpOdtcBGankFLxzFUSKuLXWNOvwQGqFRihaSP7c_al"
#ibm_url = "https://api.eu-de.speech-to-text.watson.cloud.ibm.com/instances/a807706d-de82-498f-a59f-266a89528e93/v1/recognize?model=de-DE_BroadbandModel"
# IBM keys v3
#ibm_api_key = "_fb8dF0odQAQ8n90GMXfmcZyRkhkeG7lKfLU8We8UWtg"
#ibm_url = "https://api.eu-de.speech-to-text.watson.cloud.ibm.com/instances/e286a508-bece-465a-92f4-8703fd1abc6b/v1/recognize?model=de-DE_BroadbandModel"

#---------------------------------------------------------------------------------------------
# surpress ALSA errors and warnings
#---------------------------------------------------------------------------------------------
# From alsa-lib Git 3fd4ab9be0db7c7430ebd258f2717a976381715d
# $ grep -rn snd_lib_error_handler_t
# include/error.h:59:typedef void (*snd_lib_error_handler_t)(const char *file, int line, const char *function, int err, const char *fmt, ...) /* __attribute__ ((format (printf, 5, 6))) */;
# Define our error handler type
#---------------------------------------------------------------------------------------------
ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)
def py_error_handler(filename, line, function, err, fmt):
  pass # surpress printing alsa error, do nothing instead
  
# Set error handler and pyaudio
c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)
asound = cdll.LoadLibrary('libasound.so')
asound.snd_lib_error_set_handler(c_error_handler)
p = pyaudio.PyAudio()
p.terminate()

#---------------------------------------------------------------------------------------------
# getAudioToText - (use Google lib to get microphone input as text)
#---------------------------------------------------------------------------------------------
def getAudioToText():
    recognizer = sr.Recognizer()
    
    #print(sr.Microphone.list_microphone_names())

    while True:
        
        with sr.Microphone() as source:          
            
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        try:
            sentence = ""
            if (stt_src == "Google"):
                sentence = recognizer.recognize_google(audio, language="de-AT")
            elif (stt_src == "IBM"):
                ibm_headers = {"Content-Type": "application/json"}
                ibm_auth = ("apikey", ibm_api_key)
                resp = requests.post(ibm_url, headers=ibm_headers, auth=ibm_auth, data=audio)
                sentence = resp.results[0].alternatives[0].transcript
            special_char_map = {ord(u'ä'):u'ae', ord(u'Ä'):u'Ae', ord(u'ü'):u'ue', ord(u'Ü'):u'Ue', ord(u'ö'):u'oe', ord(u'Ö'):u'Oe', ord(u'ß'):u'ss'}
            sentence_norm = sentence.translate(special_char_map)
            print("Die Sprachaufzeichnung glaubt du sagst: " + sentence_norm)            
            return sentence_norm
        
        except sr.UnknownValueError:
            print("Die Sprachaufzeichnung konnte dich leider nicht verstehen")
            
        except sr.RequestError as e:
            print("Konnte kein Ergebnis vom Server erhalten; {0}".format(e))
            
            