import time
import serial #handles the serial ports
import QboCmd #holds some commands we can use for Qbo

#set up ports for communicating with servos
port = '/dev/serial0'
ser = serial.Serial(port, baudrate=115200, bytesize = serial.EIGHTBITS, stopbits = serial.STOPBITS_ONE, parity = serial.PARITY_NONE, rtscts = False, dsrdtr =False, timeout = 0)
QBO = QboCmd.Controller(ser)

print("Up Positon")
#Move the head to the left
QBO.SetServo(2,530, 100)#Axis,Angle,Speed
#Pause
time.sleep(1)