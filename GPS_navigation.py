

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
lg = debug_print(debug_level=150, save_level=0, save_debug=True, filename="debug_print/debugprint"+str(time.time())+".txt", time_stamp=False)

import GPS_log			# to log the GPS-data in some file 'log/RC_log'+str(time.time())+'.txt'
import sensors			# to let the sensors work in the background
from navigation import * 	# to calculate best direction
from drive import *		# to be able to steet motor and wheels, and init Fahrtregler
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
accuracy_level=1
current_distance = accuracy * 10 # dummy value for current distance in meter#

#Extra_Wait variable to remember in special cases
Extra_Wait = False

# GPS-waiting time: for better average in GPS-data
GPS_waiting_time = 0.1

#----------------------------------------------------------------------------------------#

#initialization

#start sensors
sens = sensors.sensors(mode=2, start=True, sensors_min=sens_min)

# start GPS
lg.prt("[01] start GPS & initialize speed control", inst=__name__, lv=200)
gpsp=GPS.GpsPoller()

lg.prt("[02] open GPS-log-file: " + log_file_name, inst=__name__, lv=200)
log_file = GPS_log.gpslog(log_file_name)

lg.prt("[03] Waiting for valid GPS-information", inst=__name__, lv=200)
time.sleep(2)
lg.prt(gpsp.data, inst=__name__, lv=100)

while (math.isnan(gpsp.data[0])):
	time.sleep(gps_waiting_time)
	lg.prt("still waiting... ", inst=__name__, lv=100)
	lg.prt(gpsp.data, inst=__name__, lv=100)

lg.prt("[04] got valid GPS-data; wait further 4s for better data", inst=__name__, lv=200)
time.sleep(4)
lg.prt(gpsp.data, lv=100, inst=__name__)
GPS_tmp = gpsp.fetch()
lg.prt("[05] start driving-routine", inst=__name__, lv=200)


#----------------------------------------------------------------------------------------#
# Main loop to navigate to target

while accuracy_level < 4:

	while abs(current_distance) > accuracy:

		Extra_Wait = False
		lg.prt("\n_________________________________________________________________________\n\n", inst=__name__, lv=1000)

		time.sleep(GPS_waiting_time)
		if (not gpsp.is_new):
			lg.prt("----------WAITING FOR OUT OF 2 SIGMA----------", lv=1000, inst=__name__)
		else:
			GPS_tmp = gpsp.fetch()
			lg.prt("----------GOT NEW GPS:",GPS_tmp, lv=1000, inst=__name__)
		
		log_file.add_log(current_status, GPS_tmp)
		lg.prt("wrote log-entry:", lv=100, inst=__name__)

		lg.prt("sensors:", round(sens.measurements[0][0],0), [round(x[0],0) for x in sens.measurements[1]], round(sens.measurements[2][0],0), lv=1000, inst=__name__)

		if sens.measurements[0][0] < obstacle or sens.measurements[2][0] < obstacle: #or sens.measurements[1][0][0] < obstacle/3.0 or sens.measurements[1][-1][0] < obstacle/3.0:
			lg.prt('potential obstacle found!', lv=1000, inst=__name__)
			desired_status = ['break', 'slow', 'straight']
			driving(current_status,desired_status) #put this here to make reaction to obstacles faster
			time.sleep(3) 	#maybe wait for actual time needed to update all measurements
			
			if sens.measurements[0][0] < obstacle or sens.measurements[2][0] < obstacle:
				lg.prt('real obstacle found!', lv=1000, inst=__name__)
				out = "\tsensors: " + str(round(sens.measurements[0][0],0)) + ", ("
				for entry in sens.measurements[1]:
				        out = out + str(round(entry[0],0)) + ", "
				out = out + "), "  + str(round(sens.measurements[2][0],0))
				lg.prt(out, inst=__name__, lv=1000)
				
				reference_direction = comp_get_direction(GPS_destination, GPS_tmp) #get direction to target
				desired_status = navigate(sens.measurements[1], free_path, reference_direction) #take environment scan and get steering direction
				
				if desired_status != -1:	# case -1 is treated below
					
					lg.prt("\t making turn manoever, reference_direction from navigate(free_path): ", reference_direction, lv=1000, inst=__name__)
					if desired_status[2] == 'left' or desired_status[2] == 'half-left' :		
						left45(current_status)
						desired_status = ['break', 'slow', 'straight']
					elif desired_status[2] == 'right' or desired_status[2] == 'half-right' :
						right45(current_status)
						desired_status = ['break', 'slow', 'straight']
					else:
						lg.prt('\t driving backwards', lv= 1000, inst = __name__)
						desired_status = ['backward', 'slow', 'straight']

				Extra_Wait = True

			else:
				lg.prt ( 'no real obstacle found!', lv=1000, inst=__name__)
				reference_direction = comp_get_direction(GPS_destination, GPS_tmp)
				desired_status = navigate(sens.measurements[1], free_path, reference_direction)

		else:
			lg.prt('driving towards goal!', lv=1000, inst=__name__)

			reference_direction = comp_get_direction(GPS_destination, GPS_tmp)
			desired_status = navigate(sens.measurements[1], free_path, reference_direction)

		#-------------------------------
		# Exception handling
		if desired_status == -1: #no free segment found take smaller distance
			lg.prt("\tNO FREE SEGMENT IN LARGE DISTANCE FOUND --> TRY WITH SMALLER DISTANCE", lv=1000, inst=__name__)
			time.sleep(5)
			desired_status = navigate(sens.measurements[1], obstacle, reference_direction)
					
			if desired_status == -1: #no free segment with small length found, backup
				desired_status = ['backward', 'slow', 'straight']
				lg.prt("\t\tNO FREE SEGMENT IN SMALL DISTANCE FOUND --> directional backup", lv=1000, inst=__name__)
			else:
				desired_status[0] = 'backward'
				
		#-------------------------------
		# Execute 
		lg.prt("desired status: " + str(desired_status), lv=1000, inst=__name__)				
		driving(current_status,desired_status)
		time.sleep(0.5)
		desired_status = ['forward', 'null', 'straight']
		driving(current_status,desired_status) 
		if Extra_Wait:
			time.sleep(4)
		time.sleep(1)			

		#-------------------------------
		# Pause if GPS-Position is lost:
		if (math.isnan(gpsp.data[1])):
			lg.prt("----------GPS position lost! Stopping car and waiting for valid GPS-information.----------", lv=200, inst=__name__)
			driving(current_status, ['break', 'slow', 'straight'])
			lg.prt(gpsp.data, lv=100, inst=__name__)
			while (math.isnan(gpsp.data[0])):
				time.sleep(gps_waiting_time)
				lg.prt("still waiting... ", lv=100, inst=__name__)
				lg.prt(gpsp.data, lv=100, inst=__name__)

			lg.prt("[04] got valid GPS-data, continue driving.", lv=200, inst=__name__)
			lg.prt(gpsp.data, lv=100, inst=__name__)
		current_distance = math.sqrt((GPS_destination[0]-gpsp.data[0])*(GPS_destination[0]-gpsp.data[0])  +
					(GPS_destination[1]-gpsp.data[1])*(GPS_destination[1]-gpsp.data[1]))			
		lg.prt('calculate new distance to target / accuracy: ' + str(current_distance) + " / " + str(accuracy) + "; in meter: " + 
				str(round(current_distance*6300000.*2.*math.pi/360., 1)) + "m", lv=1000, inst=__name__)

	#-------------------------
	# When close to target, take more GPS data for better accuracy
	lg.prt("[08] Destination reached within accuracy level ", accuracy_level, "; change accuracy to 2sigma=",
			 (accuracy/2)*6370000*math.pi/180., lv=200, inst=__name__)
	lg.prt("wait 10sec for accurate gps-data", inst=__name__, lv=100)
	gpsp.average_number*=2
	gpsp.sigma /= 2
	gpsp.i = 0
	for i in range(gpsp.average_number - len(gpsp.lat_list)):
		gpsp.lat_list.append(float('nan'))
		gpsp.long_list.append(float('nan'))
		gpsp.alt_list.append(float('nan'))
	gpsp.is_new = True
	accuracy /= 2
	accuracy_level +=1
	GPS_extra_wait = gpsp.average_number * 0.2

	while math.isnan(gpsp.data[0]):
		time.sleep(5)


lg.prt("-----------------------------------------------------\n",
	"-----------------------------------------------------\n", "DESTINATION REACHED! STOP!", lv=200, inst=__name__)
sens.pause()
gpsp.running = False
log_file.stop()
