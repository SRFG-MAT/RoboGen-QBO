#import pyttsx

#Engine = pyttsx.init(driverName='espeak')
#Engine.setProperty('voice', 'en+f2')
#Engine.say('leich eins auf die Fresse')
#Engine.runAndWait()

import os
os.system("espeak -vde+f1 'Sum quam esse, jetzt gibts gleich eins auf die Fresse'")