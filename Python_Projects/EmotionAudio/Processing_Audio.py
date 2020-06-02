#!/usr/bin/env python
# coding=utf-8

import speech_recognition as sr

from ctypes import *
import pyaudio

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

    while True:
        
        with sr.Microphone() as source:          
            
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        try:
            sentence = recognizer.recognize_google(audio, language="de-AT")          
            print("Google Speech Recognition glaubt du sagst: " + sentence)            
            return sentence
        
        except sr.UnknownValueError:
            print("Die Sprachaufzeichnung konnte dich leider nicht verstehen")
            
        except sr.RequestError as e:
            print("Konnte kein Ergebnis von Google erhalten; {0}".format(e))
            
            