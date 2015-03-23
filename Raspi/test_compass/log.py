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
#	time year month day hour minute second latitude longitude altitude track satellites GPS_time steering_direction steering_velocity steering_position
#	(seperated by spaces)
#
# NOTE: track = heading = degree between north and direction (clockwise)
#	fix_time = GPS_time = time, when GPS position was aquired (in seconds since 1970 or somewhat... form time.time())

import time	# maybe needs to be in add_log??

class log:
	def __init__(self, log_file_name):
		self.log_file=open(log_file_name, 'a')
		self.opened = True
		self.data_seperator = "\t"

	def add_log(self, current_status, GPS_data):
		if (self.opened == False):
			print ("Error: No file opened to write to! Exit.")
			return
		gps_log = ''
		for entry in GPS_data:
			gps_log = gps_log + str(entry) + self.data_seperator # concentrate GPS-data to string with spaces as separation

		status_log = ''
		for entry in current_status:
			status_log = status_log + entry + self.data_seperator # concentrate current status to string with spaces as separation

		lt = time.localtime() # get local time information
		current_time = time.strftime("%Y" + self.data_seperator + "%m" + self.data_seperator + "%d" + self.data_seperator + "%H" + self.data_seperator + "%M" + self.data_seperator + "%S" + self.data_seperator, lt) # concentrate local time to string

		log_entry = str(time.time()) + self.data_seperator + current_time + gps_log + status_log # generate output string with all data (spaces for seperation)
		self.log_file.write(log_entry + '\n') # write output
		return log_entry # return output

	def stop(self):
		self.log_file.close()
		self.opened = False
