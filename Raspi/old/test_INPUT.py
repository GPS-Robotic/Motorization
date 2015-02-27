import time
import os
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD) # waehle normale Bezeichnung, nicht die GPIO-Bezeichnung
GPIO.setup(15, GPIO.IN) # definiere PIN 8 als Eingang

while 1:
	print GPIO.input(15)
	time.sleep(0.1)

GPIO.cleanup()
