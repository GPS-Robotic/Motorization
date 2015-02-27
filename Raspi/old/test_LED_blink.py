import time
import os
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD) # waehle normale Bezeichnung, nicht die GPIO-Bezeichnung
GPIO.setup(16, GPIO.OUT) # definiere PIN 16 als Ausgang
LED = GPIO.PWM(16, 0.3) # initialisiere PIN 16 als PWM, Frequenz = 0.3 Hz -> schaltet alle drei Sekunden an/aus

LED.start(1) # warum 1???
input('press anything to stop')

LED.stop()
GPIO.cleanup()
