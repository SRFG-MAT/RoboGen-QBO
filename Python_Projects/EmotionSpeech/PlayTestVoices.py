# coding=utf-8

import sys
import Various_Functions
import Processing_Audio
import os

#---------------------------------------------------------------------------------------------
# Play Test Voices here
#---------------------------------------------------------------------------------------------
while True:

    sentence = Processing_Audio.getAudioToText()

    if sentence.strip() == "aus" or sentence.strip() == "programm beenden":
        os.system("mpg321 -q ./mp3/Play_Abschied.mp3")
        sys.exit(0)
		
    elif sentence.strip() == "Anita":
	os.system("mpg321 -q ./mp3/Testvoice_Anika.mp3")
	
    elif sentence.strip() == "Arabella":
	os.system("mpg321 -q ./mp3/Testvoice_Arabella.mp3")
	
    elif sentence.strip() == "Markus":
	os.system("mpg321 -q ./mp3/Testvoice_Markus.mp3")
		
    elif sentence.strip() == "Gustav":
	os.system("mpg321 -q ./mp3/Testvoice_Gustav.mp3")
		
    else:
        print("Die Eingabe passt zu keiner Teststimme! Mögliche Eingaben sind Anika, Arabella, Markus oder Gustav!")
		
		
		
		
		
