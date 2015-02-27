#import RPIO as GPIO
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)          # GPIO-Numbering

Trig = 27                       # Set GPIO-Pins
Echo = 22

print "Distance Measurement In Progress"

GPIO.setup(Trig,GPIO.OUT)
GPIO.setup(Echo,GPIO.IN)

GPIO.output(Trig, False)        # Initialize Sensor
print "Waiting For Sensor To Settle"
time.sleep(1)


def measure():
	print GPIO.input(Echo)
	GPIO.output(Trig, True)         # Send Trigger
	time.sleep(0.00001)
	GPIO.output(Trig, False)
#	print GPIO.input(Echo)	

#	print "GO"

#	print GPIO.input(Echo)
#	print "LO"
	while (GPIO.input(Echo)==False):      # Receive Signal
    		pulse_start = time.time()
#		print(GPIO.input(Echo))

	print "HEY"

	while GPIO.input(Echo)==True:
    		pulse_end = time.time()

	print "HO"

	pulse_duration = pulse_end - pulse_start    # Calculate Distance

	distance = pulse_duration * 17150

	distance = round(distance, 2)

	print "Distance:",distance,"cm"

	time.sleep(0.5)

try:
	while True:
		measure()

except KeyboardInterrupt:
	GPIO.cleanup()
