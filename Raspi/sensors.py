
import time
import threading
import RPi.GPIO as GPIO
from RPIO import PWM.Servo as servo



class sensors(threading.Thread):
	def __init__(self, mode=0):

		# initialize background-thread (not yet started)
		threading.Thread.__init__(self)

		# set thread-mode (if background-thread is started)
		self.mode = mode # 0 = waiting, 1 = scanning all

		# set standart-Sensor- & Servo- PINS
		# USE GPIO-NUMBERING, NOT BOARD-NUMBERING!
		self.TRIG = [16, 20, 21]
		self.ECHO = [13, 19, 26]
		self.SERVO = 6

		# are the pins initialized to the GPIO-Module?
		self.pins_set = False

		# is the background-thread running?
		self.running = False

		# is there a measurement ongoing?
		self.is_at_measure = False

		# constants for single distance-measurements
		self.out_of_sight_time = 0.05 # max. waiting-time in seconds for echo-signal to be recieved
		self.out_of_sight_value = 10000000.0 # return value of distance measurement after out_of_sight_time
		self.relaxation_time_before = 0.04 # waiting time before measurement: to ensure sensor to be at rest
		self.dt_to_distance = 17000.0 # constant to convert time-difference to distance (standart: 17000cm/s; speed of sound/2)
		self.relaxation_time_after = 0.04 # waiting time after measurement: to ensure no sensor overlap??

		# constants for servo-positions
		# CAUTION: HAS TO BE MULTIPLE OF 10!
		# 	   ALSO self.servo_segment_size HAS TO BE MULTIPLE OF 10!
		#    system-values
		self.servo_OFFSET = 0
		self.servo_NULL = 1500 + self.servo_OFFSET
		self.servo_MAX = 2000 + self.servo_OFFSET
		self.servo_MIN = 1000 + self.servo_OFFSET
		#    current position
		self.servo_position = self.servo_NULL
		#    overall number of segments in scanning-mode
		self.servo_segments = 10
		self.servo_segment_size = (self.servo_MAX - self.servo_MIN)/self.servo

		# what is the current systems-status?
		# [mode, is_at_measure, servo_position]
		self.status = [self.mode, self.is_at_measure, self.servo_position]

		# what are the most current distance values of the sensors and there measurement times?
		# [[first_sensor, time], [[first_segment, time], [second_segment, time], ...], [third_sensor, time]]
		self.measurements = [[0, 0], [[0, 0]], [0, 0]]

	def set_PINS(TRIG=[-1,-1,-1], ECHO=[-1,-1,-1], SERVO=-1):
		# USE GPIO-NUMBERING, NOT BOARD-NUMBERING!

		# if PIN-Values set to -1: no changes --> standart if called by set_PINS()
		#    else: change values
		if (TRIG!=[-1,-1,-1]):
			self.TRIG = TRIG
		if (new_ECHO!=[-1,-1,-1]):
			self.ECHO = ECHO
		if (SERVO!=-1):
			self.SERVO = SERVO

		# initialize PINS on Board

		GPIO.setmode(GPIO.BCM)

		for i in (0,1,2):
			GPIO.setup(self.TRIG[i], GPIO.OUT)
			GPIO.setup(self.ECHO[i], GPIO.IN)

		self.pins_set = True


	def get_sensor(sensor_number):

		# wait, if there is a measure at the moment

		while(self.is_at_measure==True):
			time.sleep()

		# tell, that there is measure now

		self.is_at_measure = True

		# check for valid sensor-number

		if ( (sensor_number<0) or (sensor_number>2) ):
			print "Error! Sensor-Number must be between 0 and 2! Abort"
			return

		# check for pins to be initialized

		if (self.pins_set == False):
			self.set_PINS()

		# MEASURE

		# RELAX
		GPIO.output(self.TRIG[sensor_number], False)
		time.sleep(self.relaxation_time_before)

		# TRIGGER
		GPIO.output(self.TRIG[sensor_number], True)
		time.sleep(0.00001)
		GPIO.output(self.TRIG[sensor_number], False)
	
		# WAIT FOR ECHO
		while (GPIO.input(self.ECHO[sensor_number])!=1):
			start_time = time.time()
	
		# MEASURE ECHO-DURATION
		while (GPIO.input(self.ECHO[sensor_number])==1):
			dt = time.time() - start_time
			if(dt>self.out_of_sight_time):
				return [self.out_of_sight_value, time.time()]

		# save measurement time

		time_stamp = time.time()

		# RETURN DISTANCE
		dist = dt*self.dt_to_distance
		time.sleep(self.relaxation_time_after)

		# tell, that there is no measure now

		self.is_at_measure = False

		# save the result

		result = [dist, time_stamp]
		self.

		# return distance in cm

		return result
		

	def move_servo(value):



	def run(self):
		self.running = True
		if (self.pins_set == False):
			self.set_PINS()

		# bla CODE
		


	def pause(self):
		if(self.running == True):
			self.running = False





sens = sensors(modus)
sens.start()
