import time
import os
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD) # waehle normale Bezeichnung, nicht die GPIO-Bezeichnung
GPIO.setup(16, GPIO.OUT) # definiere PIN 16 als Ausgang
LED = GPIO.PWM(16, 1) # initialisiere PIN 16 als PWM, Frequenz = 1 Hz -> durchlaeuft sekuendlich

stop = "n"

while stop!="y":
	dc = raw_input("Enter duty-cycle between 0 and 100. ")
	value = raw_input("Enter start-value. ")
	LED.stop()
	LED.ChangeDutyCycle(int(dc))
	LED.start(int(value))
	stop = raw_input("Stop? [y] ")

LED.stop()
GPIO.cleanup()
