import math

def comp_heading(GPS_from, GPS_goingto):
    "calculate heading, based on two GPS-points"
    
    # latitude = y-coord. longitude = x-coord.
    # coord = [x-coord, y-coord] in the reference frame of the car -> current_position: origin [0, 0] 
    coord = [0., 0.]
    coord[0] = GPS_goingto[1] - GPS_from[1]
    coord[1] = GPS_goingto[0] - GPS_from[0]

    phi = math.atan2(coord[1], coord[0])

    return phi*180/math.pi  #phi is angle between x-axis and direction to target, between -180 degree and 180 degree 


def comp_get_direction(GPS_destination, GPS_data):
	
	tolerance = 10*math.pi/180 # define tolarance in angle for straight-assumption (in radiant)
	
        # phi is the angle between the car's position and the destination
	phi = comp_heading(GPS_data, GPS_destination)

	# head is the car's angle, between -180 and 180
	head = (90 - GPS_data[3])
	if head > 180:
		head = head - 360
	elif head <= -180:
		head = head + 360
	print "heading to north according to compass: " + str(head)

	theta = head - phi
	if theta > 180: 			#test for smallest angle to target
		theta = theta - 360		# according to navigate function and sensor design: left negative values, right positive
	elif theta < -180:
		theta = theta + 360
	return theta 				#between -180 degree (left) and 180 degree (right)

