# NOTE! sometimes you have to delete all *.pyc for changes to become valid!!!!!

import time
from drive import *
from log import log
from direction import get_direction
from distance_target import *
import math	# for checking whether GPS is a number
import gpsdData as GPS
import sensors

print "[01] start GPS"
gpsp=GPS.GpsPoller()

global GPS_destination
GPS_destination = [49.418045, 8.669307] 
	# [latitude, longitude]; [49.418045, 8.669307] is near the entrance of the Otto-Meyerhofer-Center
global current_status
current_status = ['break', 'slow', 'straight'] # actually one has to initialize to that!
global desired_status 
desired_status = current_status
# status = [direction,velocity,steer position] with:
#	direction = break, forward or backward
#	velocity = fast, middle or slow
#	steer position = left, half-left, straight, half-right or right

#initialize Fahrtregler:
driving(current_status,desired_status)

gps_waiting_time = 0.5 # time in seconds in while-loop for waiting for valid GPS
update_time = 1 # time in seconds in while-loop for updating gps, current_status & desired_status

global accuracy
accuracy = 7 # when is the target reached?? accuracy in meter
global current_distance
current_distance = accuracy * 10 # dummy value for current distance in meter

# NOTE: better init() is needed!

log_file_name='log/RC_log'+str(time.time())+'.txt'
log_file = log(log_file_name)

print "[02] file opened: " + log_file_name

print "[03] Waiting for valid GPS-information:"
print gpsp.data

while (math.isnan(gpsp.data[0])):
	time.sleep(gps_waiting_time)
	print "still waiting... "
	print gpsp.data

print "[04] got valid GPS-data:"
print gpsp.data


sensor = sensors.sensors() # start sensor thread
sensor.start()

print "[05] drive straight to find heading"
GPS_memory = [0, 0]      # [newest data, second latest data]
start_go = time.time()
wait_go = 4.

GPS_memory[0] = gpsp.data[0:2]

driving(current_status, ['forward', 'slow', 'straight'])
while ((((sensor.measurements[0])[0] > 70.) and 
        ((sensor.measurements[2])[0] > 70.)) and 
        (time.time() - start_go < wait_go)):
    time.sleep(0.1)
driving(current_status, ['break', 'slow', 'straight']

GPS_memory[1] = gpsp.data[0:2]

print "[06] start routine"

while current_distance > accuracy:

	print "wrote log-entry:"
	print log_file.add_log(current_status, gpsp.data)
	desired_status = get_direction(GPS_destination, gpsp.data)
	current_distance = get_target_distance(GPS_destination[0], GPS_destination[1], gpsp.data[0], gpsp.data[1]) # current_distance needs to be calculated more acurate, i.e. with altitude...
	print "[06] updated desired_status (time: " + str(time.time()) + "), new distance: " + str(current_distance) + "m"
	print "write log-entry:"
	print log_file.add_log(current_status, GPS.gpsp.data)
	desired_status = get_direction(GPS_destination, GPS.gpsp.data,GPS_memory)
	current_distance = get_target_distance(GPS_destination[0], GPS_destination[1], GPS.gpsp.data[0], GPS.gpsp.data[1]) # current_distance needs to be calculated more acurate, i.e. with altitude...
	print "[07] updated desired_status (time: " + str(time.time()) + "), new distance: " + str(current_distance) + "m"

	# Pause if GPS-Position is lost:
	if (math.isnan(gpsp.data[1])):
		print "GPS position lost! Stopping car and waiting for valid GPS-information:"
		driving(current_status, ['break', 'slow', 'straight'])
		print gpsp.data
		while (math.isnan(gpsp.data[0])):
			time.sleep(gps_waiting_time)
			print "still waiting... "
			print gpsp.data

		print "[04] got valid GPS-data, continue driving:"
		print gpsp.data

	driving(current_status, desired_status)
	print desired_status
	time.sleep(update_time)

    GPS_memory[0] = GPS_memory[1]
    GPS_memory[1] = GPS.gpsp.data[0:2]

print "[08] destination reached. stop."

log_file.stop()
