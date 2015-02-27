# function to write log-data to a log-file
# the log-file needs to be opened via "log_file=open(log_file_name, 'a')" BEFORE the function is called!
# 			and can be closed afterwards via "log_file.close()"
# ATTENTION:	the variable's name has to be exactly "log_file", i.e. "log_file_name='log/RC_log'+str(time.time())+'.txt'"!
#
# The input-lists shall contain:
#	current_status = [direction, velocity, steer_position]
#	GPS_data = [gpsd.fix.latitude, gpsd.fix.longitude, gpsd.fix.altitude, gpsd.fix.track, gpsd.fix.satellites, fix_time]
#
# The data written & returned is:
#	time year month hour minute second latitude longitude altitude track satellites GPS_time steering_direction steering_velocity steering_position
#	(seperated by spaces)
#
# NOTE: track = heading = degree between north and direction (clockwise)
#	fix_time = GPS_time = time, when GPS position was aquired (in seconds since 1970 or somewhat... form time.time())

import time	# maybe needs to be in add_log??

def add_log(current_status, GPS_data):
	gps_log = ''
	for entry in GPS_data:
		gps_log = gps_log + ' ' + str(entry) # concentrate GPS-data to string with spaces as separation

	status_log = ''
	for entry in current_status:
		status_log = status_log + ' ' + entry # concentrate current status to string with spaces as separation

	lt = time.localtime() # get local time information
	current_time = time.strftime("%Y %m %d %H %M %S", lt) # concentrate local time to string

	log_entry = str(time.time()) + ' ' + current_time + gps_log + status_log # generate output string with all data (spaces for seperation)
	log_file.write(log_entry+ '\n') # write output
	return log_entry # return output

# Just for tests:

#log_file_name='log/RC_log'+str(time.time())+'.txt'
#log_file=open(log_file_name, 'a')
#print add_log(["forward", "nope", "yes"],["lat", "long", "alt", "track", "sattelites", time.time()])
#time.sleep(2)
#print add_log(["backward", "yeah!", "no"],["lat", "long", "alt", "track", "sattelites", time.time()])
#log_file.close()
