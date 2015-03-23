# NOTE! sometimes you have to delete all *.pyc for changes to become valid!!!!!
#from i2clibraries import i2c_hmc5883l
#HMC = i2c_hmc5883l.i2c_hmc5883l(1)
#HMC.setContinuousMode()
#HMC.setDeclination(2,6)

import time
#from drive import *
from log import log
#from direction import get_direction
#from distance_target import *
import math	# for checking whether GPS is a number
import gpsdData as GPS

print ("[01] start GPS")
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

gps_waiting_time = 0.5 # time in seconds in while-loop for waiting for valid GPS
update_time = 1 # time in seconds in while-loop for updating gps, current_status & desired_status

global accuracy
accuracy = 7 # when is the target reached?? accuracy in meter
global current_distance
current_distance = accuracy * 10 # dummy value for current distance in meter

# NOTE: better init() is needed!

log_file_name='log/RC_log'+str(time.time())+'.txt'
log_file = log(log_file_name)

print ("[02] file opened: " + log_file_name)

print ("[03] Waiting for valid GPS-information:")
print (gpsp.data)

while (math.isnan(gpsp.data[0])):
	time.sleep(gps_waiting_time)
	print ("still waiting... ")
	print (gpsp.data)
#	print ("HEADING: " + str(HMC.getHeading()[0] + HMC.getHeading()[1]/60.0))

print ("[04] got valid GPS-data:")
print (gpsp.data)
#print ("HEADING: " + str(HMC.getHeading()[0] + HMC.getHeading()[1]/60.0))

print ("[05] start routine")

while current_distance > accuracy:
	print ("wrote log-entry:")
	dat = gpsp.data
#	dat.append(HMC.getHeading()[0]+HMC.getHeading[1]/60.0)
	print (log_file.add_log(current_status, dat))
#	desired_status = get_direction(GPS_destination, gpsp.data)
#	current_distance = get_target_distance(GPS_destination[0], GPS_destination[1], gpsp.data[0], gpsp.data[1]) # current_distance needs to be calculated more acurate, i.e. with altitude...
	print ("[06] updated desired_status (time: " + str(time.time()) + "), new distance: " + str(current_distance) + "m")

	# Pause if GPS-Position is lost:
#	if (math.isnan(gpsp.data[1])):
#		print "GPS position lost! Stopping car and waiting for valid GPS-information:"
#		driving(current_status, ['break', 'slow', 'straight'])
#		print gpsp.data
#		while (math.isnan(gpsp.data[0])):
#			time.sleep(gps_waiting_time)
#			print "still waiting... "
#			print gpsp.data
#
#		print "[04] got valid GPS-data, continue driving:"
#		print gpsp.data
#
#	driving(current_status, desired_status)
#	print desired_status
	time.sleep(update_time)

print ("[07] destination reached. stop.")

log_file.stop()
