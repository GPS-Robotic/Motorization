import RPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)          # GPIO-Numbering

Trig = 23                       # Set GPIO-Pins
Echo = 24

print "Distance Measurement In Progress"

GPIO.setup(Trig,GPIO.OUT)
GPIO.setup(Echo,GPIO.IN)

GPIO.output(Trig, False)        # Initialize Sensor
print "Waiting For Sensor To Settle"
time.sleep(2)

GPIO.output(Trig, True)         # Send Trigger
time.sleep(0.00001)
GPIO.output(Trig, False)

while GPIO.input(Echo)==0:      # Receive Signal
    pulse_start = time.time()

while GPIO.input(Echo)==1:
    pulse_end = time.time()

pulse_duration = pulse_end - pulse_start    # Calculate Distance

distance = pulse_duration * 17150

distance = round(distance, 2)

print "Distance:",distance,"cm"

GPIO.cleanup()
