import time
import os
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD) # waehle normale Bezeichnung, nicht die GPIO-Bezeichnung
GPIO.setup(16, GPIO.OUT) # definiere PIN 16 als Ausgang

GPIO.output(16,1)
dc = raw_input("Press anything to quit. ")
GPIO.output(16,0)
GPIO.cleanup()
