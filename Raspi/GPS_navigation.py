

import time

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
# Parameters: debug_level=0, save_debug=False, filename="", save_level="", time_stamp=False
from debug_log import debug_print
lg = debug_print(debug_level=100, save_level=0, save_debug=True, filename="debugprint"+str(time.time())+".txt", time_stamp=True)

import GPS_log			# to log the GPS-data in some file 'log/RC_log'+str(time.time())+'.txt'
import sensors			# to let the sensors work in the background
from navigation import * 	# to calculate best direction
from drive import *		# to be able to steet motor and wheels
import math	# for checking whether GPS is a number
import gpsdData as GPS		# to get GPS-data and compass-value

#----------------------------------------------------------------------------------------#
#definitions

#obstacle distance
obstacle = 50 # for test without sensors. 75.0 #cm
free_path = 200
sens_min = 7 # minimal possible distance for sensors (below: ignore)

global GPS_destination
GPS_destination = [49.418096, 8.669395]  # [49.41739, 8.66894] # [49.418080, 8.66939] 

gps_waiting_time = 0.5 # time in seconds in while-loop for waiting for valid GPS
update_time = 1 # time in seconds in while-loop for updating gps, current_status & desired_status

log_file_name='log/RC_log'+str(time.time())+'.txt'

# distance to target
accuracy = 0.000015 # when is the target reached?? 2*sigma for average of 10 GPS-data; in degree (0.000015 = 1,7m)
current_distance = accuracy * 10 # dummy value for current distance in meter#

#Turn variable to remember turning right or left 
Turn = False

#----------------------------------------------------------------------------------------#

#initialization

#start sensors
sens = sensors.sensors(mode=2, start=True, sensors_min=sens_min)

# start GPS
lg.prt("[01] start GPS & initialize speed control", inst=__name__, lv=200)
gpsp=GPS.GpsPoller()

# initialisiere Fahrtregler
current_status = ['break', 'slow', 'straight'] # actually one has to initialize to that!
desired_status = current_status
driving(current_status,desired_status) #init Fahrtregler
time.sleep(4)

lg.prt("[02] open GPS-log-file: " + log_file_name, inst=__name__, lv=200)
log_file = GPS_log.gpslog(log_file_name)

lg.prt("[03] Waiting for valid GPS-information", inst=__name__, lv=200)
time.sleep(2)
lg.prt(gpsp.data, inst=__name__, lv=100)

while (math.isnan(gpsp.data[0])):
	time.sleep(gps_waiting_time)
	lg.prt("still waiting... ", inst=__name__, lv=100)
	lg.prt(gpsp.data, inst=__name__, lv=100)

lg.prt("[04] got valid GPS-data; wait further 10s for better data", inst=__name__, lv=200)
lg.prt(gpsp.data, lv=100, inst=__name__)
time.sleep(10)
lg.prt(gpsp.data, lv=100, inst=__name__)
lg.prt("[05] start driving-routine", inst=__name__, lv=200)



#----------------------------------------------------------------------------------------#
# Main loop to navigate to target

while abs(current_distance) > accuracy:
	turn = False
	lg.prt("beginn of loop\n____________________________________________\n\n", inst=__name__, lv=1000)
	
	GPS_tmp = gpsp.fetch()
	log_file.add_log(current_status, GPS_tmp)
	lg.prt("wrote log-entry:", lv=100, inst=__name__)

	lg.prt("sensors: ", sens.measurements[0][0], [x[0] for x in sens.measurements[1]], sens.measurements[2][0], lv=1000, inst=__name__)

	if sens.measurements[0][0] < obstacle or sens.measurements[2][0] < obstacle: #or sens.measurements[1][0][0] < obstacle/3.0 or sens.measurements[1][-1][0] < obstacle/3.0:
		lg.prt( 'potential obstacle found!\n\n', lv=1000, inst=__name__)
		desired_status = ['break', 'slow', 'straight']
		driving(current_status,desired_status) #put this here to make reaction to obstacles faster
		time.sleep(3) 	#maybe wait for actual time needed to update all measurements
		if sens.measurements[0][0] < obstacle or sens.measurements[2][0] < obstacle:
		#time.sleep(1)
			lg.prt('real obstacle found!\n\n', lv=1000, inst=__name__)
			#just a debug-output
			out = "sensors: " + str(sens.measurements[0][0]) + ", ("
		        for entry in sens.measurements[1]:
		                out = out + str(entry[0]) + ", "
			out = out + "), "  + str(sens.measurements[2][0])
			lg.prt(out, inst=__name__, lv=1000)

			desired_status = ['break', 'slow', 'straight']

			if (not gpsp.is_new):
				lg.prt("WAITING FOR OUT OF 2 SIGMA", lv=1000, inst=__name__)
			else:
				GPS_tmp = gpsp.fetch()
			reference_direction = comp_get_direction(GPS_destination, GPS_tmp) #get direction to target
			desired_status = navigate(sens.measurements[1], free_path, reference_direction) #take environment scan and get steering direction
			if desired_status == -1: #no free segment found take smaller distance
				lg.prt("NO FREE SEGMENT IN LARGE DISTANCE FOUND\nTRY WITH SMALLER DISTANCE", lv=1000, inst=__name__)
				time.sleep(3)
				desired_status = navigate(sens.measurements[1], obstacle, reference_direction)
				if desired_status == -1: #no free segment with small length found turn around
					lg.prt("NO FREE SEGMENT IN SMALL DISTANCE FOUND\nTURN AROUND", lv=1000, inst=__name__)
					turn180(current_status,desired_status,speed='middle')
					time.sleep(1)
					reference_direction -= 180
					Turn = True
			else:
				lg.prt("reference_direction: ", reference_direction, lv=1000, inst=__name__)
				if desired_status[2] == 'left' or desired_status[2] == 'half-left' :		
					left90(current_status,desired_status,speed='middle')
					time.sleep(1)
					reference_direction += 90
					Turn = True
				elif desired_status[2] == 'right' or desired_status[2] == 'half-right' :
					right90(current_status,desired_status,speed='middle')
					time.sleep(1)
					reference_direction -= 90
					Turn = True
				else:
					turn180(current_status,desired_status,speed='middle')
					time.sleep(1)
					reference_direction -= 180
					Turn = True
			time.sleep(.5)
		else:
			lg.prt ( 'no real obstacle found!\n\n', lv=1000, inst=__name__)
			if (not gpsp.is_new):
				lg.prt("WAITING FOR OUT OF 2 SIGMA", lv=1000, inst=__name__)
			else:
				GPS_tmp = gpsp.fetch()
			reference_direction = comp_get_direction(GPS_destination, GPS_tmp)
			desired_status = navigate(sens.measurements[1], free_path, reference_direction)
	else:
		lg.prt('driving towards goal!', lv=1000, inst=__name__)
		Turn = False
		#steering direction in degree.
		if (not gpsp.is_new):
			lg.prt("WAITING FOR OUT OF 2 SIGMA", lv=1000, inst=__name__)
		else:
			GPS_tmp = gpsp.fetch()
		reference_direction = comp_get_direction(GPS_destination, GPS_tmp)
		desired_status = navigate(sens.measurements[1], free_path, reference_direction)
		lg.prt("desired status: " + str(desired_status), lv=1000, inst=__name__)
		if desired_status == -1:	#no free path found with large distance	
			lg.prt("NO FREE SEGMENT IN LARGE DISTANCE FOUND\nTRY WITH SMALLER DISTANCE", lv=1000, inst=__name__)
			desired_status = navigate(sens.measurements[1], obstacle, reference_direction)
			#check again with smaller distance			 
			if desired_status == -1: #no free segment with small length found turn around
				lg.prt("NO FREE SEGMENT IN SMALL DISTANCE FOUND\nTURN AROUND", lv=1000, inst=__name__)
				turn180(current_status,desired_status,speed='middle')
				time.sleep(1)
				reference_direction -= 180
				Turn = True	
			else:
				lg.prt("reference_direction: ", reference_direction, lv=1000, inst=__name__)
				if desired_status[2] == 'straight':
					desired_status = ['forward', 'slow', 'straight']
				elif desired_status[2] == 'left' or desired_status[2] == 'half-left' :		
					left90(current_status,desired_status,speed='middle')
					time.sleep(1)
					reference_direction += 90
					Turn = True
				elif desired_status[2] == 'right' or desired_status[2] == 'half-right' :
					right90(current_status,desired_status,speed='middle')
					time.sleep(1)
					reference_direction -= 90
					Turn = True
				else:
					turn180(current_status,desired_status,speed='middle')
					time.sleep(1)
					reference_direction -= 180
					Turn = True
			time.sleep(.5)
		else:
			driving(current_status,desired_status)
			time.sleep(0.5)
			desired_status = ['forward', 'null', 'straight']
			driving(current_status,desired_status) 
			time.sleep(0.5)			

	# Pause if GPS-Position is lost:
	if (math.isnan(gpsp.data[1])):
		lg.prt("GPS position lost! Stopping car and waiting for valid GPS-information:", lv=200, inst=__name__)
		driving(current_status, ['break', 'slow', 'straight'])
		lg.prt(gpsp.data, lv=100, inst=__name__)
		while (math.isnan(gpsp.data[0])):
			time.sleep(gps_waiting_time)
			lg.prt("still waiting... ", lv=100, inst=__name__)
			lg.prt(gpsp.data, lv=100, inst=__name__)

		lg.prt("[04] got valid GPS-data, continue driving.", lv=200, inst=__name__)
		lg.prt(gpsp.data, lv=100, inst=__name__)
	current_distance = math.sqrt((GPS_destination[0]-gpsp.data[0])*(GPS_destination[0]-gpsp.data[0])+(GPS_destination[1]-gpsp.data[1])*(GPS_destination[1]-gpsp.data[1]))			
	lg.prt(   'calculate new distance to target / accuracy: ' + str(current_distance) + " / " + str(accuracy) + "; in meter: " + str(  round(current_distance*6300000.*2.*math.pi/360., 1)) + "m", lv=1000, inst=__name__)

lg.prt("[08] destination reached. stop.", lv=200, inst=__name__)
sens.pause()
gpsp.running = False
log_file.stop()
