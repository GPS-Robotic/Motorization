# This file is the main routine for the automotive robot to find it's destination via GPS-data.
# start this file by 'sudo GPS_navigation.py' directly on the raspberry pi (or put it on auto-start somehow) for the robot to seek the given GPS-position.
# the target-GPS-position can be set some lines below as GPS_destination = [49.418096, 8.669395]
# Note, that some other modules are used by this script.

import time

# To use the advanced-output routine, use the following module (debug_log)
# It allows to set different output levels for every output. (use lg.prt instead of print, then)
#
# How does this work?
#	-> from debug_log import debug_print
#	-> create debug_print-instance and set global debug-level & global save-level
#	-> put output-messages into your script via lg.prt instead of print
#		lg.prt ( --messages & objects--, lv = --LEVEL--, instance=__name__)
#		Only messages with LEVEL >= global debug-level will be print on console
#		Only messages with LEVEL >= global save-level will be safed to file
#		instance=__name__ gives an additional info about which module sent the message
#	-> to use this output-control in other modules, too, simply put 'from __main__ import lg' in the beginning of that module
#
#	-> EXAMPLE:
#		from debug_log import debug_print
#		lg = debug_print(debug_level=150, save_level=0, save_debug=True, filename="debug_print/debugprint"+str(time.time())+".txt", time_stamp=False)
#		lg.prt("still waiting... ", inst=__name__, lv=100)
#
#		--> debug_level is set to 150, all messages with lv >= 150 will be print on screen
#		--> save_level is set to 0, all messages will be saved to file
#		--> save_debug=True, if False, messages won't be saved
#		--> filename="...", here the messages will be saved to
#		--> time_stamp=False, if Ture, the time, when the messages was sent, will be saved and print, too
#
#	-> for more details see module-file

#
# use the following for output:
# from __main__ import lg 	(not in this file)
# lg.prt( --messages & objects--, lv = --LEVEL--, inst=__name__)
# SUGGESTED LEVELS:
#
#	10	useless, any
#	100	info
#	1000	debug
#	10000	warning
#	100000	error
#
# possible Parameters: debug_level=0, save_debug=False, filename="", save_level="", time_stamp=False

from debug_log import debug_print # must be imported as first module directly after time!
lg = debug_print(debug_level=150, save_level=0, save_debug=True, filename="debug_print/debugprint"+str(time.time())+".txt", time_stamp=False) # create output-control-instance

import GPS_log			# to log the GPS-data in some file 'log/RC_log'+str(time.time())+'.txt'
import sensors			# to let the sensors work in the background
from navigation import * 	# to calculate best direction
from drive import *		# to be able to steet motor and wheels, and init Fahrtregler
import math			# for checking whether GPS is a number
import gpsdData as GPS		# to get GPS-data and compass-value

#----------------------------------------------------------------------------------------#

# definitions

obstacle = 50 		# trigger-distance (in cm) for left & right sensor (0 & 2) to break, if there is an obstacle too close
free_path = 200		# distance (in cm) for the navigation-algorithm to set the path as occupied/blocked
sens_min = 7 		# minimal possible distance (in cm) for sensors (closer objects: ignore result of sensor)
			#	EXPLANATION: 	we assume our robot to never reach objects closer than this
			#			in this way we avoid some sensor-errors

GPS_destination = [49.418096, 8.669395] # SET target-GPS-position HERE!!!! 
					#	[latitude, longitude]
					# 	(some target near the robotic's lab: [49.418096, 8.669395])

gps_waiting_time = 0.5 # time in seconds in while-loop for waiting for valid GPS
log_file_name='log/RC_log'+str(time.time())+'.txt'	# log-file-name for the GPS-data (not for debug-messages)
accuracy = 0.00003 		 # when is the target reached?? define target-radius here; in degree! (0.000015 ~ 1,7m)
current_distance = accuracy * 10 # dummy value for current distance in meter (only needed for script to start)

Extra_Wait = False 	# Extra_Wait variable to remember that it is needed to wait longer in special cases
GPS_waiting_time = 0.1	# extra GPS-waiting time: for better average in GPS-data


#----------------------------------------------------------------------------------------#

#initialization

# start sensors
sens = sensors.sensors(mode=2, start=True, sensors_min=sens_min) # mode 2 seems to be the best mode: scanning

# start GPS
lg.prt("[01] start GPS & initialize speed control", inst=__name__, lv=200)
gpsp=GPS.GpsPoller()

# open GPS-log-file
lg.prt("[02] open GPS-log-file: " + log_file_name, inst=__name__, lv=200)
log_file = GPS_log.gpslog(log_file_name)

# waiting for GPS to fix
lg.prt("[03] Waiting for valid GPS-information", inst=__name__, lv=200)
time.sleep(2)
lg.prt(gpsp.data, inst=__name__, lv=100)

while (math.isnan(gpsp.data[0])):
	time.sleep(gps_waiting_time)
	lg.prt("still waiting... ", inst=__name__, lv=100)
	lg.prt(gpsp.data, inst=__name__, lv=100)

# save current GPS-data for further use
lg.prt("[04] got valid GPS-data; wait further 4s for better data", inst=__name__, lv=200)
time.sleep(4)
lg.prt(gpsp.data, lv=100, inst=__name__)
GPS_tmp = gpsp.fetch()
lg.prt("[05] start driving-routine", inst=__name__, lv=200)




#----------------------------------------------------------------------------------------#

# main loop to navigate to target

while abs(current_distance) > accuracy: # stop if we are close enough to target-position

	Extra_Wait = False
	lg.prt("\n_________________________________________________________________________\n\n", inst=__name__, lv=1000)

	time.sleep(GPS_waiting_time)
	if (not gpsp.is_new): # check for new gps-data 
			      #		(due to fluctuations in GPS and averaging in GPS-thread 
			      #		 it is useful to wait for new GPS-data that is far enough away from old one) 
		lg.prt("----------WAITING FOR OUT OF 2 SIGMA----------", lv=1000, inst=__name__)
	else:
		GPS_tmp = gpsp.fetch() # save current GPS-data as up-to-date one for further use
		lg.prt("----------GOT NEW GPS:",GPS_tmp, lv=1000, inst=__name__)
		
	log_file.add_log(current_status, GPS_tmp) # save GPS-data to GPS-log-file
	lg.prt("wrote log-entry:", lv=100, inst=__name__)
	lg.prt("sensors:", round(sens.measurements[0][0],0), [round(x[0],0) for x in sens.measurements[1]], round(sens.measurements[2][0],0), lv=1000, inst=__name__)

	if sens.measurements[0][0] < obstacle or sens.measurements[2][0] < obstacle: # check if there is a close obstacle straight ahead
		# ---- MAYBE THERE IS A CLOSE OBSTACLE STRAIGHT AHEAD ---- #
		lg.prt('potential obstacle found!', lv=1000, inst=__name__)
		desired_status = ['break', 'slow', 'straight'] 
		driving(current_status,desired_status) # BREAK!
		time.sleep(3) 	# wait for more up-to-date sensor-data
			
		if sens.measurements[0][0] < obstacle or sens.measurements[2][0] < obstacle: # once more: 
								#   check if there is a close obstacle straight ahead
								#     (needed as sensors have many errors)
			# ---- THERE IS A CLOSE OBSTACLE STRAIGHT AHEAD FOR SURE ---- #
			lg.prt('real obstacle found!', lv=1000, inst=__name__)
			out = "\tsensors: " + str(round(sens.measurements[0][0],0)) + ", ("
			for entry in sens.measurements[1]:
			        out = out + str(round(entry[0],0)) + ", "
			out = out + "), "  + str(round(sens.measurements[2][0],0))
			lg.prt(out, inst=__name__, lv=1000)
				
			reference_direction = comp_get_direction(GPS_destination, GPS_tmp) # get direction to target
			desired_status = navigate(sens.measurements[1], free_path, reference_direction) # take environment scan and get steering direction
				
			if desired_status != -1:	# case -1 (if no way is found) is treated below
					
				lg.prt("\t making turn manoever, reference_direction from navigate (free_path): ", reference_direction, lv=1000, inst=__name__)
				if desired_status[2] == 'left' or desired_status[2] == 'half-left' :
					# ---- THERE IS A FREE WAY ON OUR LEFT ---- #		
					left45(current_status)
					desired_status = ['break', 'slow', 'straight']
				elif desired_status[2] == 'right' or desired_status[2] == 'half-right' :
					# ---- THERE IS A FREE WAY ON OUR RIGHT ---- #
					right45(current_status)
					desired_status = ['break', 'slow', 'straight']
				else:
					# ---- THERE IS NO FREE WAY ON OUR LEFT OR RIGHT ---- #
					lg.prt('\t driving backwards', lv= 1000, inst = __name__)
					desired_status = ['backward', 'slow', 'straight']

			Extra_Wait = True # as there was an obstacle: wait extra time at the end of loop for sensors to update

		else:
			# ---- THERE IS NO CLOSE OBSTACLE AHEAD ---- #
			lg.prt ( 'no real obstacle found!', lv=1000, inst=__name__)
			reference_direction = comp_get_direction(GPS_destination, GPS_tmp) # get direction to target
			desired_status = navigate(sens.measurements[1], free_path, reference_direction) # take environment scan and get steering direction

	else:
		# ---- NO PROBLEMS OR OBSTACLES: JUST KEEP ON DRIVING ---- #
		lg.prt('driving towards goal!', lv=1000, inst=__name__)

		reference_direction = comp_get_direction(GPS_destination, GPS_tmp) # get direction to target
		desired_status = navigate(sens.measurements[1], free_path, reference_direction) # take environment scan and get steering direction

	#-------------------------------
	# Exception handling
	if desired_status == -1: # no free segment found, try with smaller obstacle-distance
		lg.prt("\tNO FREE SEGMENT IN LARGE DISTANCE FOUND --> TRY WITH SMALLER DISTANCE", lv=1000, inst=__name__)
		time.sleep(5)
		desired_status = navigate(sens.measurements[1], obstacle, reference_direction) # take environment scan and get steering direction
					
		if desired_status == -1: # no free segment with smaller obstacle-distance found, back-up!
			desired_status = ['backward', 'slow', 'straight']
			lg.prt("\t\tNO FREE SEGMENT IN SMALL DISTANCE FOUND --> directional back-up", lv=1000, inst=__name__)
		else:
			desired_status[0] = 'backward' # free segment found, but the obstacle is close --> drive backwards in given direction
				
	#-------------------------------
	# Execute 
	lg.prt("desired status: " + str(desired_status), lv=1000, inst=__name__)				
	driving(current_status,desired_status) # drive in desired direction
	time.sleep(0.5)
	desired_status = ['forward', 'null', 'straight']
	driving(current_status,desired_status) # roll a little bit further
	if Extra_Wait:
		time.sleep(4) # wait a little bit longer as there were obstacles
	time.sleep(1)			

	#-------------------------------
	# Pause if GPS-Position is lost:
	if (math.isnan(gpsp.data[1])):
		lg.prt("----------GPS position lost! Stopping car and waiting for valid GPS-information.----------", lv=200, inst=__name__)
		driving(current_status, ['break', 'slow', 'straight'])
		lg.prt(gpsp.data, lv=100, inst=__name__)
		while (math.isnan(gpsp.data[0])): # wait for valid GPS-data
			time.sleep(gps_waiting_time)
			lg.prt("still waiting... ", lv=100, inst=__name__)
			lg.prt(gpsp.data, lv=100, inst=__name__)

		lg.prt("[04] got valid GPS-data, continue driving.", lv=200, inst=__name__)
		lg.prt(gpsp.data, lv=100, inst=__name__)

	current_distance = math.sqrt((GPS_destination[0]-gpsp.data[0])*(GPS_destination[0]-gpsp.data[0])  +
				(GPS_destination[1]-gpsp.data[1])*(GPS_destination[1]-gpsp.data[1])) # calculate new distance to target		
	lg.prt('calculate new distance to target / accuracy: ' + str(current_distance) + " / " + str(accuracy) + "; in meter: " + 
			str(round(current_distance*6300000.*2.*math.pi/360., 1)) + "m", lv=1000, inst=__name__)


lg.prt("-----------------------------------------------------\n",
	"-----------------------------------------------------\n", "[08] DESTINATION REACHED! STOP!", lv=200, inst=__name__)
sens.pause() # stop background scripts at target-destination
gpsp.running = False
log_file.stop()
