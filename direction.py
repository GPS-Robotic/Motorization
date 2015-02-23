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

# MAYBE THE ANGLE-IF-STATEMENTS ARE WRONG AND WE NEED MODULUS HERE!
# AND WE HAVE TO CHECK WHETER BOTH ARE RADIANT / DEGREE!

def get_direction(GPS_destination, GPS_data, desired_status):
	tolerance =  # define tolarance in angle for straight-assumption
	# transform origin into current position:
	coord = [GPS_destination[1]-GPS_data[1], GPS_destination[0]-GPS_data[0]] # [x, y] of target -> current_position: origin [0, 0]
	phi = math.atan(coord[0]/coord[1]) # angle phi of target position (NOT polar-angle; angle between y-axis and vector)
	if (abs(phi-GPS_data[3])<tolerance): # if we (nearly) head on target: drive straight, medium pace
		desired_status=['forward', 'middle', 'straight']
	elif (((phi-GPS_data[3])%360)<180): # current angle is less than target-angle -> turn right
		desired_status=['forward', 'slow', 'right']
	elif (((phi-GPS_data[3])%360)>=180): # current angle is bigger than target-angle -> turn left
		desired_status=['forward', 'slow', 'left']
	else:
		print "Error: couldn't calculate direction. There is something deeply wrong in your script!"
