import time
import RPi.GPIO as GPIO

def get_distance(i):
	GPIO.setmode(GPIO.BCM)

	TRIG = [16, 20, 21]  # 16  20  21
	ECHO = [13, 19, 26]  # 13  19  26
#	SERVO = 6 # for moving sensor 2

	GPIO.setup(TRIG[i], GPIO.OUT)
	GPIO.setup(ECHO[i], GPIO.IN)

	GPIO.output(TRIG[i], False)
#	print "Echo: " + str(GPIO.input(ECHO[i]))

	time.sleep(.04)

	GPIO.output(TRIG[i], True)
	time.sleep(0.00001)
	GPIO.output(TRIG[i], False)
	
	while (GPIO.input(ECHO[i])!=1):
		start_time = time.time()
	
	while (GPIO.input(ECHO[i])==1):
		dt = time.time() - start_time
		if(dt>0.05):
			return 10000000.0

	dist = dt*17000.0
#	print "Distance (" + str(i) + "): " + str(dist) + "cm"
	time.sleep(.04)
	return dist
