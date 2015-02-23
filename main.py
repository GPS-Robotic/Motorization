import time
import "drive.py"
import "log.py"
import "gpsdData.py"
import "direction.py"
import "distance_target.py"

global GPS_data = [0, 0, 0, 0, 0, 0]
	# [gpsd.fix.latitude, gpsd.fix.longitude, gpsd.fix.altitude, gpsd.fix.track, gpsd.fix.satellites, gps.fixing.time]
global GPS_destination = [49.418045, 8.669307] 
	# [latitude, longitude]; [49.418045, 8.669307] is near the entrance of the Otto-Meyerhofer-Center
global current_status = ['break', 'slow', 'straight'] # actually one has to initialize to that!
global desired_status
# status = [direction,velocity,steer position] with:
#	direction = break, forward or backward
#	velocity = fast, middle or slow
#	steer position = left, half-left, straight, half-right or right

global accuracy = 7 # when is the target reached?? accuracy in meter
global current_distance = accuracy * 10 # dummy value for current distance in meter

# NOTE: better init() is needed!

log_file_name='log/RC_log'+str(time.time())+'.txt'
log_file=open(log_file_name, 'a')

print "[01] file opened: " + log_file_name

get_gps(GPS_data) # start continous GPS-Input-Stream (background-thread, hopefully...)

print "[02] GPS-Input-Stream started, waiting for correct information..."

while GPS_data[0] == 0:
	time.sleep(0.5)

print "[03] got GPS-data:\n"

for entry in GPS_data:
	print entry

print "[04] start routine"

while current_distance > accuracy:
	add_log(current_status, GPS_data)
	get_direction(GPS_destination, GPS_data, desired_status)
	driving(current_status, desired_status)
	distance = get_target_distance(GPS_destination[0], GPS_destination[1], GPS_data[0], GPS_data[1]) # current_distance needs to be calculated more acurate, i.e. with altitude...
	print "[05] updated desired_status (time: " + str(time.time()) + "), new distance: " + str(current_distance) + "m"

print "[06] destination reached. stop."

log_file.close()
