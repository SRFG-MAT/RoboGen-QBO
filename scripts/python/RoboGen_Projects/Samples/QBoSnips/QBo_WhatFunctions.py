#!/usr/bin/env python

# Sollte gewollt werden, dass der letzte Kommand, weiteres aufzaehlen der Funktionen, gewuenscht ist bzw. eine genauere Erklaerung der Funktionen, muesste fast eine Sprachverarbeitung hinzugefuegt werden

import os
import time
import speech_recognition as sr
from snips_nlu import SnipsNLUEngine

os.system("espeak -vde+m1 'Ich werde nun meine Funktionen aufzaehlen und eine kurze Beschreibung liefern, was diese koennen.'")

os.system("espeak -vde+m1 'Funktion Stresstagebuch: Wir bearbeiten einen Fragebogen und werden am Ende besprechen welche Moeglichkeiten du hast, deinen Stress zu reduzieren.'")

os.system("espeak -vde+m1 'Funktion Diabetisfragebogen: Wir werden gemeinsam Moeglichkeiten auf den Grund gehen, wie du dein Leben mit Diabetis meistern kannst.'")

os.system("espeak -vde+m1 'QBo Silver Edition: Du kannst mir alles erzahelen was du willst und ich hoere dir aufmerksam zu.'")

os.system("espeak -vde+m1 'Wenn du noch mehr Funktionen aufgelistet haben willst, sag mir Bescheid.'")

#time.sleep(2)
#with sr.Microphone() as source:
#	audio = r.listen(source)
#sentence = r.recognize_google(audio, language=de)

nlu_engine = SnipsNLUEngine.from_path("SnipsNLU/QBo_Model")
parsing = nlu_engine.parse(u"Ja")
intent = parsing["intent"]["intentName"]
print(intent)

if intent == "nein":
	os.system("espeak -vde+m1 'Verstanden, ich beende das Programm. Auf wiederhoeren.'")
elif intent == "ja":
	os.system("espeak -vde+m1 'Weitere moegliche Funktionen waeren Einschlafgeraeusche, was die lieblingsapplikation von einem meiner Entwickler ist. Sonstige Funktionen werden im Laufe der Zeit hinzugefuegt.'")
else:
	os.system("espeak -vde+m1 'Es tut mir leid, aber diese Aussage konnte ich leider nicht verarbeiten. Das Programm wird beendet und kann spaeter erneut aufgerufen werden. Tudel lu.'")
