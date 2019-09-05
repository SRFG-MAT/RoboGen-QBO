#import pyttsx

#import pyttsx
#engine = pyttsx.init()
#engine.say('Guten Tag.', 'de-DE')
#engine.runAndWait()

from gtts import gTTS
import os
 
# Text
mytext = 'Ciao Ciao'
 
# Sprache (ISO Code)
language = 'de'
 
# Erzeugen der Sprachausgabe
myobj = gTTS(text=mytext, lang=language, slow=False)
 
# Speichern als mp3
myobj.save("./mp3/abschied.mp3")
os.system("mpg321 ./mp3/abschied.mp3")


#import espeak

#es = espeak.ESpeak()
#es.voice = 'de'
#es.speed = 1

#es.say("Wie geht es dir?")
