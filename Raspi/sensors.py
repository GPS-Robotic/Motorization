# This modul shall start a background instance of advanced sensor-control


import time
import threading
import RPi.GPIO as GPIO
from RPIO import PWM

servo = PWM.Servo()

class sensors(threading.Thread):
	def __init__(self, mode=0, start=False):

		# initialize background-thread (not yet started)
		threading.Thread.__init__(self)

		# set thread-mode (if background-thread is started)
		# mode:	0 = update all sensors in cycle 0-1-2-1-0-1-2-1-0-..., servo not moved
		#	1 = scanning all sensors in cycle 0-1-2-1-0-1-2-1-0-..., servo scans: from left to right to left to right...
		#	2 = scanning all sensors in cycle 0-1-2-1-0-1-2-1-0-..., servo scans: from left to right jump, form left to right, ...
		self.mode = mode 

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
		self.out_of_sight_time = 0.05 # max. waiting-time in seconds for echo-signal-duration
#		self.ECHO_in_timeout = 0.5 # max. waiting-time in seconds for echo-signal to come in
		self.out_of_sight_value = 10000000.0 # return value of distance measurement after out_of_sight_time
		self.relaxation_time_before = 0.04 # waiting time before measurement: to ensure sensor to be at rest
		self.dt_to_distance = 17000.0 # constant to convert time-difference to distance (standart: 17000cm/s; speed of sound/2)
#		self.relaxation_time_after = 0.04 # waiting time after measurement: to ensure no sensor overlap??
		self.queue_waiting_time = 0.00001 # time for waiting loop, if system is measuring and new measuring is waiting
		self.scan_relaxation_time = 0.3 # time between single scannings in scanning-mode

		# what are the most current distance values of the sensors and there measurement times?
		# [[first_sensor, time], [[first_segment, time], [second_segment, time], ...], [third_sensor, time]]
		# if you want to change servo_segment_size: update via update_segments(servo_segment_size)
		self.measurements = [[0, 0], [[0, 0]], [0, 0]]

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
		#    overall number of segments in scanning-mode & segment-size (in servo-values)
		#    if you want to change servo_segment_size: update via update_segments(servo_segment_size)
		self.servo_segments = 10 # NOTE: There is one more measurement than segments!
		self.servo_segment_size = 0
		self.servo_segment_values = []
		self.update_segments(0, new_segment_number=self.servo_segments)
		# set servo to zero-position
		servo.set_servo(self.SERVO, self.servo_NULL)

		# initialize PINS
		self.set_PINS()

		# relax servos in beginning
		for trig in self.TRIG:
			GPIO.output(trig, False)
		time.sleep(self.relaxation_time_before)

		# start background-thread
		if (start):
			self.start()

	def set_PINS(self, TRIG=[-1,-1,-1], ECHO=[-1,-1,-1], SERVO=-1):
		# USE GPIO-NUMBERING, NOT BOARD-NUMBERING!

		# if PIN-Values set to -1: no changes --> standart if called by set_PINS()
		#    else: change values
		if (TRIG!=[-1,-1,-1]):
			self.TRIG = TRIG
		if (ECHO!=[-1,-1,-1]):
			self.ECHO = ECHO
		if (SERVO!=-1):
			self.SERVO = SERVO

		# initialize PINS on Board

		GPIO.setmode(GPIO.BCM)

		for i in (0,1,2):
			GPIO.setup(self.TRIG[i], GPIO.OUT)
			GPIO.setup(self.ECHO[i], GPIO.IN)

		self.pins_set = True


	def get_sensor(self, sensor_number):
		# wait, if there is a measure at the moment

		while(self.is_at_measure==True):
			time.sleep(self.queue_waiting_time)

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

		# TRIGGER
		GPIO.output(self.TRIG[sensor_number], True)
		time.sleep(0.00001)
		GPIO.output(self.TRIG[sensor_number], False)
	
		# WAIT FOR ECHO
		echo_start = time.time()
#		start_time = 2*time.time() # debug! check loops
		while ( (GPIO.input(self.ECHO[sensor_number])!=1) ):#and (time.time()-echo_start < self.ECHO_in_timeout)):
			start_time = time.time()
	
		# MEASURE ECHO-DURATION
		dt = -1.0 # debug! check loops
		while (GPIO.input(self.ECHO[sensor_number])==1):
			dt = time.time() - start_time
			if(dt>self.out_of_sight_time):		## CHECK THIS!!!!
				self.is_at_measure = False
				return [self.out_of_sight_value, time.time()]

		# save measurement time
		time_stamp = time.time()

		# RETURN DISTANCE
		dist = dt*self.dt_to_distance
#		time.sleep(self.relaxation_time_after)

		# tell, that there is no measure now

		self.is_at_measure = False

		# save the result
		result = [dist, time_stamp]
		if (sensor_number == 1):
			current_segment=int((self.servo_position-self.servo_MIN)/self.servo_segment_size)
			try:
				(self.measurements[1])[current_segment]=result
			except:
				print "Error! Not possible to save measurement of servo-sensor in array. Check segment number:"
				print "current_segment=" + str(current_segment) + " of servo_segments=" + self.servo_segments
		else:
			self.measurements[sensor_number] = result

		# return distance (in cm) & measure-time in time.time()-format
		return result
		

	def move_servo(self, value, percentage=-1):
		# move servo to given position
		
		# ether by given servo-value
		if (percentage == -1):
			self.servo_position = value
			servo.set_servo(self.SERVO, value)

		# ether by percentage (value between 0 and 1), if given (0 = MIN, 1 = MAX)
		else:
			self.servo_position = self.servo_NULL + round(percentage*(self.servo_MAX-self.servo_MIN), -1)
			servo.set_servo(self.SERVO, self.servo_position)


	def update_segments(self, new_segment_size, new_segment_number=-1):
		# update servo's segment-size (in servo-values) & -number
		# CAUTION: ALL VALUES OF SENSOR 2 WILL BE DELETED HEREBY!
		# CAUTION: size must be multiple of 10 and number must be integer.
		#          also (number * size == MAX-MIN) must be true!

		# ether via segment-size
		if (new_segment_number == -1):
			self.servo_segment_size = round(new_segment_size, -1)
			self.servo_segments = int( (self.servo_MAX - self.servo_MIN) / self.servo_segment_size )

		# or via segment_number
		else:
			self.servo_segments = int(new_segment_number)
			self.servo_segment_size = round((self.servo_MAX - self.servo_MIN)/self.servo_segments, -1)

		if (self.servo_segments*self.servo_segment_size!=self.servo_MAX-self.servo_MIN):
			print "ERROR: Servo-Segment configuration not correct! Stop."
			quit()

		# update segment-servo-values & initialize measurement-list
		# NOTE: There is one more measurement than segments!
		self.servo_segment_values = []
		(self.measurements)[1] = []

		for i in range(0,self.servo_segments+1,1):
			self.servo_segment_values.append(self.servo_MIN + (i*self.servo_segment_size) )
			self.measurements[1].append([0,0])
		
		
	def set_mode(self, new_mode):
		self.running = False
		mode = new_mode

	def run(self):
		if (self.running==False):
			self.running = True
		if (self.pins_set == False):
			self.set_PINS()

		# define cycle-variable:
		i = 0 # position in scanning cycle: which sensor will be evaluated next?
		j = int(self.servo_segments/2) # position in segment cycle: which segment will be evaluated next?
		servo_direction = +1 # for scanning: which direction? +1 -> moves to right-hand-side -1 -> moves to left-hand-side

		# once more, check for correct segment-configuration; just for safety
		self.update_segments(0, new_segment_number=self.servo_segments)

		while (self.running == True):

			time.sleep(self.scan_relaxation_time)

			# mode 0 = update all sensors in cycle 0-1-2-1-0-1-2-1-0-..., servo not moved
			if (self.mode == 0):
				cycle=[0,1,2,1] # define cycle for current mode
				self.get_sensor(cycle[i]) # update next sensor
				
				# servo is not moved

				i=i+1 # count to next cycle-entry
				if (i>=len(cycle)): # jump to cycle-beginning
					i=0				

			# mode 1 = scanning all sensors in cycle 0-1-2-1-0-1-2-1-0-...,
			#          servo scans: from left to right to left to right... starting at center
			elif (self.mode == 1):
				cycle=[0,1,2,1] # define cycle for current mode
				self.get_sensor(cycle[i]) # update next sensor
				
				if (cycle[i] == 1): # move servo to next position

					if ( (j == 0) and (servo_direction == -1) ): # servo is at left end and wants to move further left
						servo_direction = +1 # from now: move right!
					elif ( (j == self.servo_segments) and (servo_direction == +1) ) : # servo is at right end and wants to move further right
						servo_direction = -1 # from now: move left!

					# move servo to next position
					j = j + servo_direction
					self.move_servo(self.servo_segment_values[j])

				i=i+1 # count to next cycle-entry
				if (i>=len(cycle)): # jump to cycle-beginning
					i=0
				

			# mode 2 = scanning all sensors in cycle 0-1-2-1-0-1-2-1-0-...,
 			#          servo scans: from left to right jump, form left to right, ... starting at center
			elif (self.mode == 2):
				cycle=[0,1,2,1] # define cycle for current mode
				self.get_sensor(cycle[i]) # update next sensor
				
				if (cycle[i] == 1): # move servo to next position
					if (j == self.servo_segments) : # servo is at right end and wants to move further right
						j = -1 # jump to left end

					# move servo to next position
					j = j + servo_direction
					self.move_servo(self.servo_segment_values[j])

				i=i+1 # count to next cycle-entry
				if (i>=len(cycle)): # jump to cycle-beginning
					i=0
				
			else:
				print "Unknown mode set to sensor-scanning-thread! Waiting for corrent mode..."
		


	def pause(self):
		if(self.running == True):
			self.running = False



