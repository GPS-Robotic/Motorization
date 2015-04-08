# This is a function to write log-data to a log-file
#
# The module can be used (after import log) by mylog = log.log(log_file_name),
# where log_file_name is the filename of the log-file which will be created
#
# The module automatically opens the given file on start-up to write data into it later.
# NOTE: the module only appends data to the file! so if there is already a file with the same name, the file won't be overwritten.
#
# by mylog.stop() the module will close the file. Nethertheless, afterwards data still can be written, the module simply opens the file again.
#
# log-data can be written to the file by mylog.add_log(current_status, GPS_data)
#
# The input-lists shall contain:
#	current_status = [direction, velocity, steer_position]
#	GPS_data = [gpsd.fix.latitude, gpsd.fix.longitude, gpsd.fix.altitude, gpsd.fix.track, gpsd.fix.satellites, fix_time]
#
# The data written & returned is:
#	time year month day hour minute second latitude longitude altitude track [satellites] GPS_time steering_direction steering_velocity steering_position
#	(seperated by the data-separator, which bei default is tab \t and can be adjusted by mylog.data_separator = new_separator)
#	[satallites] hereby is a list
# each call of add_log will generate one line in the file
#
# NOTE: track = heading = degree between north and direction (clockwise)
#	fix_time = GPS_time = time, when GPS position was aquired (in seconds since 1970 or somewhat... form time.time()) <-- not sure about that

from __main__ import lg
import time	# maybe needs to be in add_log??

class gpslog:
	# initialize: open file, set to open, set separator
	def __init__(self, log_file_name):
		self.log_file=open(log_file_name, 'a')
		self.opened = True
		self.data_separator = "\t"

	# write log-data in specific format
	def add_log(self, current_status, GPS_data):
		if (self.opened == False):
			lg.prt("Warning: No file opened to write to! Probably it was closed before. Openening file again.", lv=10000, inst=__name__)
			self.log_file=open(log_file_name, 'a')
		gps_log = ''
		for entry in GPS_data:
			gps_log = gps_log + str(entry) + self.data_separator # concentrate GPS-data to string with spaces as separation

		status_log = ''
		for entry in current_status:
			status_log = status_log + entry + self.data_separator # concentrate current status to string with spaces as separation

		lt = time.localtime() # get local time information
		current_time = time.strftime("%Y" + self.data_separator + "%m" + self.data_separator + "%d" + self.data_separator + "%H" + self.data_separator + "%M" + self.data_separator + "%S" + self.data_separator, lt) # concentrate local time to string

		log_entry = str(time.time()) + self.data_separator + current_time + gps_log + status_log # generate output string with all data (spaces for seperation)
		self.log_file.write(log_entry + '\n') # write output
		return log_entry # return output

	# close file, set to closed
	def stop(self):
		self.log_file.close()
		self.opened = False
