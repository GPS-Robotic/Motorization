import time
import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BCM)

TRIG = 21  # 16  20  21
ECHO = 26  # 13  19  26

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

GPIO.output(TRIG, False)
print "Echo: " + str(GPIO.input(ECHO))

time.sleep(2)

while True:
	GPIO.output(TRIG, True)
	time.sleep(0.00001)
	GPIO.output(TRIG, False)

	while (GPIO.input(ECHO)!=1):
		start_time = time.time()

	while (GPIO.input(ECHO)==1):
		stop_time = time.time()

	dt = stop_time - start_time
#	print "Time elapsed: " + str(dt)
	print "Distance: " + str(dt*17000.0) + "cm"
	time.sleep(.1)
