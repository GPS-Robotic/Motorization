# ONLY FOR TOOLS-USE HERE! IF YOU WANT TO CHANGE THIS MODULE, YOU HAVE TO CHANGE IT IN MAIN DIRECTORY, TOO!

# This modul shall start a background instance of advanced sensor-control
#
# After "import sensors" the module can be started by
#	mysensors = sensors.sensors()	<-- mode = 0, background thread not running yet (start=False)
#	or
#	mysensors = sensors.sensors(mode = mymode, start=mystart)
#		(both parameters are optional are only important for the background-thread)
#
# There are two possiblities to use the background-module:
#	1) single-measurements
#		via 
#			mysensors.get_sensor(sensor_number)
#		(sensor_number is 0, 1 or 2) one can take a single measurement of one sensor.
#		The result will be returned in a list, containing the result and the time of the measurement: [result, time],
#		where the result is by default in cm (can be adjusted).
#		Also the result will be saved in mysensors.measurements (see below)
#	
#		via 
#			mysensors.move_servo(value, percentage=-1)
#		one can move the servo of sensor 1
#		the parameter percentage is optional, by default it is -1.
#		If percentage is set, it MUST be between 0 and 1, defining the position: value = MIN + percentage*(MAX-MIN)
#		IMPORTANT: Nevertheless, also value must be set, but will be overwritten, if percentage is not -1!!!
#		If percentage is not set or set to -1, value will be the value to which the servo will be adjusted.
#		Currently the Null-Position is at 1500, MAX at 2000 and MIN at 1000. This is set in
#		mysensors.servo_MIN / _MAX / _NULL and can be adjusted
#		
#		even when background mode is running (start=True), one can make single-measurements.
#		ALWAYS the module is waiting for one measurement to be finished before starting another!! (To avoid interference)
#
#		NOTE: There are some constants, which are given back as result for invalid measurements. Check them to avoid errors!
#			(They may need to be adjusted, also get_sensor() may need to be adjusted....)
#
#	2) background-thread:
#		If start=True at initialization, the background-measurement-mode is started immediately.
#		The background-measurement can also be started afterwards by mysensors.start()
#		The background-thread will steadily measure values from the sensors and save the update as a list in mysensors.measurements,
#		the design of the list depends on the various settings and will be explained as follows...
#
#		At the moment it is possible to set one of three background modes, they are:
#			mode = 0:
#				the servo won't be moved, but can be adjusted by mysensors.move_servo(value) (see above)
#				the measurements will be done in the following cycle: 0-1-2-1-0-1-2-1-...,
#				meaning that sensor 0 will be called first, then sensor 1, then sensor 2, then sensor 1 again, ...
#				the measurements will be saved in mysensors.measurements as:
#					[[dist0, time0], [[dist1, time1]], [dist2, time2]]
#				(disti = distance, measured from sensor i; timei = time-stamp of that measurement...)
#				CAUTION: The entry for sensor1 ALWAYS is a double list!
#				         In this case, it is a list with only one entry. In the other cases there are more entries: 
#				         One for each border between the segments (=segments+1 entries), see below
#			mode = 1:
#				the measurement-cycle for the sensors is the same as at mode = 0:
#				the measurements will be done in the following cycle: 0-1-2-1-0-1-2-1-...,
#				meaning that sensor 0 will be called first, then sensor 1, then sensor 2, then sensor 1 again, ...
#				This time the sensor moves after each measurement of sensor 1, thus resulting in a scanning of the area
#				(roughly 180 degrees)
#				Therefore the servo-settings must have been done before (can be adjusted always also)
#				mysensors.servo_MIN / _MAX / _NULL define the valid range
#				mysensors.servo_segments define the number of segments
#				mysensors.servo_segment_size defines the size of each segment
#				mysensors.servo_segment_values defines the positions at which the measurements are done
#				CAUTION: to change these segment-settings, please use 
#						mysensors.update_segments(new_segment_size, new_segment_number=-1)
#					 where new_segment_number is optional.
#					 If new_segment_number is set to -1 or no set, new_segment_size defines the size of the new segments
#					 If new_segment_number is set, the new segment size will be (MAX - MIN) / new_segment_number,
#					 nevertheless, in this case ANY value for new_segment_size must be given as parameter, but isn't used.
#				IMPORTANT: to avoid errors: the following equation must hold!
#					servo_MAX - servo_MIN = servo_segments * servo_segment_size
#				servo_MAX / _MIN / _NULL & _OFFSET can be adjusted simply by reassignment....
#
#				NOTE: The number of measurements in this mode is equal to (servo_segment_number + 1),
#				      because the measurements are done BETWEEN the segments....
#
#				In mode = 1 the servo moves from left to right to left to right to left .....
#
#				mysensors.measurements will be designed as follows:
#					[[dist0, time0], [ [meas0, time1_0], [meas1, time1_1], [meas2, time1_2], ... ], [dist2, time2]]
#				where measi & time1_i are the result of the measurement of sensor 1 at position i and its time
#
#			mode = 2:
#				This is essentially the same as mode = 1 (see description above).
#				The only difference is, that the servo moves from left to right and then jumps back to left
#
#			mode = 3:
#				This is essentially the same as mode = 2 (see description above)
#				The only difference is, that is is averaged over self.averaging_number measurements of each sensor
#
#			Maybe there will be implemented further modes later on, see at def run(self) or in initilization-section for details...
#			to change the mode, use
#				mysensors.set_mode(new_mode)
#
# The PIN-Settings of the boar are saved in mysensors.ECHO & mysensors.TRIG & mysensors.SERVO (the first one are lists for sensors 0, 1 & 2)
# To change these settings and activate in a valid way, use
#	mysensors.set_PINS(TRIG=new_TRIG, ECHO=new_ECHO, SERVO=new_SERVO)
# each parameter is optional here, but the lists must be complete
#
# The pre-definition can be seen in the __init__ section
#
#
# For questions, write to PhilippGernandt@web.de
#
#
# NOTE: SOME ERRORS MIGHT STILL COME FROM mysensors.get_sensor()
# ESPECIALLY: SOME ABBORT-CRITERIA ARE DIFFICULT....
#
# NOTE: No-Echo-In-Result will be returned, but not saved,
#	Out-Of-Sight-Result will be returned & saved
#	Wrong-Sensor-Number-Error will be returned, but not saved


from __main__ import lg # for output-control
import time
import threading
import RPi.GPIO as GPIO
from RPIO import PWM

servo = PWM.Servo()
PWM.set_loglevel(1)    # try to stop debug output

class sensors(threading.Thread):
	def __init__(self, mode=0, start=False, sensors_min=7): # ignore sensor-values below sensors_min

		self.lock = threading.Lock()

		# initialize background-thread (not yet started)
		threading.Thread.__init__(self)

		# set thread-mode (if background-thread is started)
		# mode:	0 = update all sensors in cycle 0-1-2-1-0-1-2-1-0-..., servo not moved
		#	1 = scanning all sensors in cycle 0-1-2-1-0-1-2-1-0-..., servo scans: from left to right to left to right...
		#	2 = scanning all sensors in cycle 0-1-2-1-0-1-2-1-0-..., servo scans: from left to right jump, form left to right, ...
	        #   3 = like mode 2, but averaging over two measurements
		self.mode = mode 

		# set standart-Sensor- & Servo- PINS
		# USE GPIO-NUMBERING, NOT BOARD-NUMBERING!
		self.TRIG = [7, 8, 25]
		self.ECHO = [11, 9, 10]
		self.SERVO = 24

		# are the pins initialized to the GPIO-Module?
		self.pins_set = False

		# is the background-thread running?
		self.running = False

		# is there a measurement ongoing?
		self.is_at_measure = False

		# constants for single distance-measurements
		self.ECHO_in_timeout = 0.05 # max. waiting-time in seconds for echo-signal to come in
		self.no_echo_in_value = -1.0 # return value if no echo is received after ECHO_in_timeout
		self.out_of_sight_time = 0.05 # max. waiting-time in seconds for echo-signal-duration
					       #   (according to data sheet: max 25ms for obstacle, exact 38ms for no-obstacle)
		self.out_of_sight_value = 500.0 # return value of distance measurement after out_of_sight_time
		self.dt_to_distance = 17000.0 # constant to convert time-difference to distance (standart: 17000cm/s; speed of sound/2)
		self.scan_relaxation_time = 0.05 # time between single scannings in scanning-mode
		self.unknown_error_value = 30000000.0 # return-value if unknown error occurs in get_sensor()
		self.measure_tries = 5 # number of tries for single measurement (on no-echo-in- or unknown-error)

		self.sensors_min = sensors_min # ignore sensor values below this

		self.averaging_number=3 # number of measurements for averaging in mode 3

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

		# start background-thread
		if (start):
			time.sleep(0.1)
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
			time.sleep(0.01)

		# tell, that there is measure now
		self.is_at_measure = True

		# MEASURE
		self.lock.acquire()
		# TRIGGER
		GPIO.output(self.TRIG[sensor_number], True)
		time.sleep(0.00001)
		GPIO.output(self.TRIG[sensor_number], False)

		# WAIT FOR ECHO
		try: # added because of error 'referrenced before assignement'

			echo_start = time.time() # serves also for time-stamp of measurement
			while ( (GPIO.input(self.ECHO[sensor_number])==0) ):
				start_time = time.time()
				if (time.time()-echo_start>self.ECHO_in_timeout):	## CHECK THIS!!!
					self.is_at_measure = False
					result = [self.no_echo_in_value, echo_start]

					# return distance (in cm) & measure-time in time.time()-format
					self.lock.release()
					return result
	
			# MEASURE ECHO-DURATION
			while (GPIO.input(self.ECHO[sensor_number])==1):
				dt = time.time() - start_time
				if(dt>self.out_of_sight_time):		## CHECK THIS!!!!
					self.is_at_measure = False
					result = [self.out_of_sight_value, echo_start]

					# return distance (in cm) & measure-time in time.time()-format
					self.lock.release()
					return result

			# tell, that there is no measure now
			self.is_at_measure = False

			# RETURN DISTANCE
			dist = dt*self.dt_to_distance

			# save the result
			result = [dist, echo_start]

			# return distance (in cm) & measure-time in time.time()-format
			self.lock.release()
			return result

		except: # any unknown error
			self.is_at_measure = False
			lg.prt("exception from sensor " + str(sensor_number + 1) + " of 3", inst=__name__, lv=10000) # + "): unknown error from sensor (probably \'referenced before assignment\')"
			GPIO.output(self.TRIG[sensor_number], False)
			time.sleep(0.2)
			self.lock.release()
			return [self.unknown_error_value, echo_start]
		

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
			lg.prt("ERROR: Servo-Segment configuration not correct! Stop.", lv=100000, inst=__name__)
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
		self.mode = new_mode
		self.start()

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
				result = self.get_sensor(cycle[i]) # update next sensor
				
				# on no-echo-in- or unknown-error: try again (5 times)
				tries = 1
				while (result[0]==self.no_echo_in_value or result[0]==self.unknown_error_value):
					if tries < self.measure_tries:
						result = self.get_sensor(cycle[i])
						tries += 1
					else:
						break

				#save the result
				if cycle[i] != 1:
					if result[0] > self.sensors_min: self.measurements[cycle[i]] = result
				else:
					if result[0] > self.sensors_min: self.measurements[cycle[i]] = [result]

				# servo is not moved

				i=i+1 # count to next cycle-entry
				if (i>=len(cycle)): # jump to cycle-beginning
					i=0				



















			# mode 1 = scanning all sensors in cycle 0-1-2-1-0-1-2-1-0-...,
			#          servo scans: from left to right to left to right... starting at center
			elif (self.mode == 1):
				cycle=[0,1,2,1] # define cycle for current mode
				result = self.get_sensor(cycle[i]) # update next sensor
				
				# on no-echo-in- or unknown-error: try again (5 times)
				tries = 1
				while (result[0]==self.no_echo_in_value or result[0]==self.unknown_error_value):
					if tries < self.measure_tries:
						result = self.get_sensor(cycle[i])
						tries += 1
					else:
						break

				#save the result
				if cycle[i] != 1:
					if result[0] > self.sensors_min: self.measurements[cycle[i]] = result
				else:
					current_segment=int((self.servo_position-self.servo_MIN)/self.servo_segment_size)
					if result[0] > self.sensors_min: self.measurements[cycle[i]][current_segment] = result


				if (cycle[i] == 1): # move servo to next position

					if ( (j == 0) and (servo_direction == -1) ): # servo is at left end and wants to move further left
						servo_direction = +1 # from now: move right!
					elif ( (j == self.servo_segments) and (servo_direction == +1) ) : # servo is at right end and wants to move further right
						servo_direction = -1 # from now: move left!

					# move servo to next position
					j = j + servo_direction
					self.move_servo(self.servo_segment_values[j])
					time.sleep(.1) # the servo needs time to move

				i=i+1 # count to next cycle-entry
				if (i>=len(cycle)): # jump to cycle-beginning
					i=0
				















			# mode 2 = scanning all sensors in cycle 0-1-2-1-0-1-2-1-0-...,
 			#          servo scans: from left to right jump, form left to right, ... starting at center
			elif (self.mode == 2):
				cycle=[0,1,2,1] # define cycle for current mode
				result = self.get_sensor(cycle[i]) # update next sensor
				
				# on no-echo-in- or unknown-error: try again (5 times)
				tries = 1
				while (result[0]==self.no_echo_in_value or result[0]==self.unknown_error_value):
					if tries < self.measure_tries:
						result = self.get_sensor(cycle[i])
						tries += 1
					else:
						break

				#save the result
				if cycle[i] != 1:
					if result[0] > self.sensors_min: self.measurements[cycle[i]] = result
				else:
					current_segment=int((self.servo_position-self.servo_MIN)/self.servo_segment_size)
					if result[0] > self.sensors_min: self.measurements[cycle[i]][current_segment] = result

				if (cycle[i] == 1): # move servo to next position
					if (j == self.servo_segments) : # servo is at right end and wants to move further right
						j = -1 # jump to left end

					# move servo to next position
					j = j + servo_direction
					self.move_servo(self.servo_segment_values[j])
					if (j == 0): # the servo needs time to come from right end to left end
						time.sleep(.6)
					else:
						time.sleep(.1)

				i=i+1 # count to next cycle-entry
				if (i>=len(cycle)): # jump to cycle-beginning
					i=0















         		# mode 3 = scanning all sensors in cycle 0-1-2-1-0-1-2-1-0-...,
 	    		#          servo scans: from left to right jump, form left to right, ... starting at center
   		        #          like mode 2, but averaging over 2 consecutive measurements
			elif (self.mode == 3):
				cycle=[0,1,2,1] # define cycle for current mode

				# do many measurements to average
				av_sum = 0

				time_stamp = time.time()
				nmb_of_measurements = 0
				for meas_nmb in range(self.averaging_number):
					has_error = False
					result = self.get_sensor(cycle[i]) # update next sensor
				
					# on no-echo-in- or unknown-error: try again (5 times)
					tries = 1
					while (result[0]==self.no_echo_in_value or result[0]==self.unknown_error_value):
						if tries < self.measure_tries:
							result = self.get_sensor(cycle[i])
							tries += 1
						else:
							has_error = True
							break

					if not has_error:
						av_sum += result[0]
						nmb_of_measurements += 1

				if nmb_of_measurements == 0:
					result = [self.unknown_error_value, time_stamp]
				else:
					result = [av_sum/nmb_of_measurements, time_stamp]
				
				#save the result
				if cycle[i] != 1:
					if result[0] > self.sensors_min: self.measurements[cycle[i]] = result
				else:
					current_segment=int((self.servo_position-self.servo_MIN)/self.servo_segment_size)
					if result[0] > self.sensors_min: self.measurements[cycle[i]][current_segment] = result

				if (cycle[i] == 1): # move servo to next position
					if (j == self.servo_segments) : # servo is at right end and wants to move further right
						j = -1 # jump to left end

					# move servo to next position
					j = j + servo_direction
					self.move_servo(self.servo_segment_values[j])
					if (j == 0): # the servo needs time to come from right end to left end
						time.sleep(.6)
					else:
						time.sleep(.1)

				i=i+1 # count to next cycle-entry
				if (i>=len(cycle)): # jump to cycle-beginning
					i=0




			else:
				lg.prt("Unknown mode set to sensor-scanning-thread! Waiting for corrent mode...", lv=100000, inst=__name__)
		


	def pause(self):
		if(self.running == True):
			self.running = False



