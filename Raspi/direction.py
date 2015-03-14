# this function shall generate a desired_status in order to reach the destination (including curves etc)

# this is a first, very simple approach. basically the function shall only determine wheter it is needed to turn left, right or to accelerate....
# in this first approach we only use slow speed (for turning) and medium speed (for straight driving) and no backward driving

# also we assume that (because of small distances), the longitude and latitude basically are equal to normal coordinates (orthogonal)
#	=> latitude = y-coord. longitude = x-coord.

# status = [direction,velocity,steer position] with:
#	direction = break, forward or backward
#	velocity = fast, middle or slow
#	steer position = left, half-left, straight, half-right or right
# GPS_data = [gpsd.fix.latitude, gpsd.fix.longitude, gpsd.fix.altitude, gpsd.fix.track, gpsd.fix.satellites, gps.fixing.time]
# GPS_destination = [latitude, longitude]

import math

# Note: use atan2 to circumvent any trouble with atan :)

# Note: since GPS-heading is not working properly we calculate the heading between the last two GPS points we got.

def heading(GPS_from, GPS_goingto):
    "calculate heading, based on two GPS-points"
    
    # latitude = y-coord. longitude = x-coord.
    # coord = [x-coord, y-coord] in the reference frame of the car -> current_position: origin [0, 0] 
    coord = [0., 0.]
    coord[0] = GPS_goingto[1] - GPS_from[1]
    coord[1] = GPS_goingto[0] - GPS_from[0]

    phi = math.atan2(coord[1], coord[0])

    return phi


def get_direction(GPS_destination, GPS_data, GPS_memory):
	
    tolerance = 10*math.pi/180 # define tolarance in angle for straight-assumption (in radiant)
	
    # phi is the angle between the car's position and the destination
    phi = heading(GPS_destination, GPS_data)

	# head is the car's angle, between -pi and pi
	head = heading(GPS_memory[0],GPS_memory[1])	

	if (abs( phi - head ) < tolerance): # if we (nearly) head on target: drive straight, medium pace
		desired_status=['forward', 'middle', 'straight']
	elif ( ( phi - head) > 0): # current angle is less than target-angle -> turn right
		desired_status=['forward', 'slow', 'right']
	elif ( ( phi - head) < 0): # current angle is bigger than target-angle -> turn left
		desired_status=['forward', 'slow', 'left']
	else:	# any error
		desired_status=['break', 'slow', 'straight']
		print "Error: couldn't calculate direction. There is something deeply wrong in your script! Stopped."
	return desired_status
