# this function shall generate a desired_status in order to reach the destination (including curves etc)

# this is a first, very simple approach. basically the function shall only determine wheter it is needed to turn left, right or to accelerate....
# in this first approach we only use slow speed (for turning) and medium speed (for straight driving) and no backward driving

# also we assume that (because of small distances), the longitude and latitude basically are equal to normal coordinates (ortothogonal)
#	=> latitude = y-coord. longitude = x-coord.

# status = [direction,velocity,steer position] with:
#	direction = break, forward or backward
#	velocity = fast, middle or slow
#	steer position = left, half-left, straight, half-right or right
# GPS_data = [gpsd.fix.latitude, gpsd.fix.longitude, gpsd.fix.altitude, gpsd.fix.track, gpsd.fix.satellites, gps.fixing.time]
# GPS_destination = [latitude, longitude]

import math

# Note: atan returns only values between -90 and 90 degrees, even if target is behind car (i.e. phi=180 degrees)
#       to fix this, we will check, whether y is negative!

# Caution: GPS-heading is delivered in degrees, not in radiant!

def get_direction(GPS_destination, GPS_data):
	tolerance = 10*math.pi/180 # define tolarance in angle for straight-assumption (in radiant)
	# transform origin into current position:
	coord = [GPS_destination[1]-GPS_data[1], GPS_destination[0]-GPS_data[0]] # [x, y] of target -> current_position: origin [0, 0]

	# phi is the target's angle, between -pi and pi
	if ( coord[1] == 0.0 ): # if y == 0
		coord[1] = 0.00000000001
	phi = math.atan(coord[0]/coord[1]) # angle phi of target position (NOT polar-angle; angle between y-axis and vector) (in radiant)

	if ( coord[1] < 0.0 ): # check whether target is behind us and correct angle phi
		phi = phi + math.pi
		phi = phi % (2*math.pi)
	if (phi > math.pi): # we want phi to be between -pi and pi
		phi = phi - 2*math.pi

	# head is the car's angle, between -pi and pi
	head = math.pi*GPS_data[3]/180 # transform GPS-heading into radiant
	if (head > math.pi):
		head = head - 2*math.pi # we want head to be between -pi and pi

	if (abs( phi - (math.pi*GPS_data[3]/180) ) < tolerance): # if we (nearly) head on target: drive straight, medium pace
		desired_status=['forward', 'middle', 'straight']
	elif ( ( phi - head) > 0): # current angle is less than target-angle -> turn right
		desired_status=['forward', 'slow', 'right']
	elif ( ( phi - head) < 0): # current angle is bigger than target-angle -> turn left
		desired_status=['forward', 'slow', 'left']
	else:	# any error
		desired_status=['break', 'slow', 'straight']
		print "Error: couldn't calculate direction. There is something deeply wrong in your script! Stopped."
	return desired_status
