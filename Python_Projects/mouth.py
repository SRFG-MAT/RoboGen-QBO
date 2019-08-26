import time
import serial #handles the serial ports
import QboCmd #holds some commands we can use for Qbo

#set up ports for communicating with servos
port = '/dev/serial0'
ser = serial.Serial(port, baudrate=115200, bytesize = serial.EIGHTBITS, stopbits = serial.STOPBITS_ONE, parity = serial.PARITY_NONE, rtscts = False, dsrdtr =False, timeout = 0)
QBO = QboCmd.Controller(ser)

print("all")
#ALL LEDs value from website 000000001f1f1f1f  remember replace leading zeros with 0x
QBO.SetMouth(0x1f1f1f1f)  
#Pause
time.sleep(1)

print("oval")
#oval value from website 000000000e11110e  remember replace leading zeros with 0x
QBO.SetMouth(0xe11110e)
#Pause
time.sleep(1)

print("smile")
#smile -value from website  00000000110e0000  remember replace leading zeros with 0x
QBO.SetMouth(0x110e0000)
#Pause
time.sleep(1)

print("sad")
#sad value from website  00000000000e1100  remember replace leading zeros with 0x
QBO.SetMouth(0x0e1100)
#Pause
time.sleep(1)

print("serious")
#serious website value 00000000001f1f00  remember replace leading zeros with 0x
QBO.SetMouth(0x1f1f00)
#Pause
time.sleep(1)

print("love")
#love wesite value 000000001b1f0e04  remember replace leading zeros with 0x
QBO.SetMouth(0x1b1f0e04)
time.sleep(1)

print("pyramide")
QBO.SetMouth(0x40e1f)
time.sleep(1)

print("oval")
#oval value from website 000000000e11110e  remember replace leading zeros with 0x
QBO.SetMouth(0x1f1b151f)