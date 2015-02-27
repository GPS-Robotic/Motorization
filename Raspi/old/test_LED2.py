import time
import os
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD) # waehle normale Bezeichnung, nicht die GPIO-Bezeichnung
GPIO.setup(16, GPIO.OUT) # definiere PIN 16 als Ausgang
LED = GPIO.PWM(16, 50) # initialisiere PIN 16 als PWM, Frequenz = 50 Hz

LED.start(0)
try:
	while 1:
		for dc in range(0, 101, 1):
			LED.ChangeDutyCycle(dc)
			time.sleep(0.05)
		for dc in range(0, -1, -5):
			LED.ChangeDutyCycle(dc)
			time.sleep(0.05)
except KeyboardInterrupt:
	pass

LED.stop()
GPIO.cleanup()
