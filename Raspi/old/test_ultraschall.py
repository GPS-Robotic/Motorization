import time
import os
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM) # waehle normale Bezeichnung, nicht die GPIO-Bezeichnung
GPIO.setup(10, GPIO.IN) # definier Echo-PIN as input
GPIO.setup(25, GPIO.OUT) #define Trigger-PIN as output

inp=""

while (inp==""):
	GPIO.output(25,0)
	time.sleep(2)
	GPIO.output(25,1)
	time.sleep(0.00001)
	GPIO.output(25,0)
	print "Triggered...."
	while (GPIO.input(10)==0):
		start_time=time.time()
	while (GPIO.input(10)==1):
		stop_time=time.time()
	distance=17150*(stop_time-start_time)
	print distance, "cm"
	inp=raw_input("Input anything to quit, else repeat")
GPIO.cleanup()
