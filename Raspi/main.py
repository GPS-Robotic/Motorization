import time
import drive
from log import add_log
from gpsdData_TEST2 import *
#import direction
import distance_target

global GPS_data
GPS_data = [0, 0, 0, 0, 0, 0]
	# [gpsd.fix.latitude, gpsd.fix.longitude, gpsd.fix.altitude, gpsd.fix.track, gpsd.fix.satellites, gps.fixing.time]
global GPS_destination
GPS_destination = [49.418045, 8.669307] 
	# [latitude, longitude]; [49.418045, 8.669307] is near the entrance of the Otto-Meyerhofer-Center
global current_status
current_status = ['break', 'slow', 'straight'] # actually one has to initialize to that!
global desired_status
# status = [direction,velocity,steer position] with:
#	direction = break, forward or backward
#	velocity = fast, middle or slow
#	steer position = left, half-left, straight, half-right or right

global accuracy
accuracy = 7 # when is the target reached?? accuracy in meter
global current_distance
current_distance = accuracy * 10 # dummy value for current distance in meter

# NOTE: better init() is needed!

log_file_name='log/RC_log'+str(time.time())+'.txt'
log_file=open(log_file_name, 'a')

print "[01] file opened: " + log_file_name

#get_gps(GPS_data) # start continous GPS-Input-Stream (background-thread, hopefully...)

gpsp = GpsPoller() # create the thread
try:
  gpsp.start() # start it up
  while True:
    #It may take a second or two to get good data
    #print gpsd.fix.latitude,', ',gpsd.fix.longitude,'  Time: ',gpsd.utc
#    os.system('clear')
    # edit by Max: don't know if this works in order to get the output as data
    # track = heading in degrees
#      return gpsd.fix.latitude, gpsd.fix.longitude, gpsd.fix.altitude, gpsd.fix.track, gpsd.fix.satellites
    # edit by Phil: lists can be produced by list=[...., ..., ...]
    #		      return ... terminates the function, so that is no option
    # 	      I renamed this file to gpsdData.py.backup and implemented a new one...
 
    print
    print ' GPS reading'
    print '----------------------------------------'
    print 'latitude    ' , gpsd.fix.latitude
    print 'longitude   ' , gpsd.fix.longitude
    print 'time utc    ' , gpsd.utc,' + ', gpsd.fix.time
    print 'altitude (m)' , gpsd.fix.altitude
    print 'eps         ' , gpsd.fix.eps
    print 'epx         ' , gpsd.fix.epx
    print 'epv         ' , gpsd.fix.epv
    print 'ept         ' , gpsd.fix.ept
    print 'speed (m/s) ' , gpsd.fix.speed
    print 'climb       ' , gpsd.fix.climb
    print 'track       ' , gpsd.fix.track     
    print 'mode        ' , gpsd.fix.mode
    print
    print 'sats        ' , gpsd.satellites
 
    time.sleep(1) #set to whatever
 
except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
  print "\nKilling Thread..."
  gpsp.running = False
  gpsp.join() # wait for the thread to finish what it's doing
print "Done.\nExiting."


print "[02] GPS-Input-Stream started, waiting for correct information..."

while GPS_data[0] == 0:
	time.sleep(0.5)
	print "still waiting... " + str(GPS_data[0])

print "[03] got GPS-data:\n"

for entry in GPS_data:
	print entry

print "[04] start routine"

while current_distance > accuracy:
	add_log(current_status, GPS_data)
	#get_direction(GPS_destination, GPS_data, desired_status)
	#driving(current_status, desired_status)
	#current_distance = get_target_distance(GPS_destination[0], GPS_destination[1], GPS_data[0], GPS_data[1]) # current_distance needs to be calculated more acurate, i.e. with altitude...
	print "[05] updated desired_status (time: " + str(time.time()) + "), new distance: " + str(current_distance) + "m"
	time.sleep(2)

print "[06] destination reached. stop."

log_file.close()
