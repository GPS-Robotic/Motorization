import math

def heading(GPS_points):
    "calculate heading, based on two GPS-points"
    
    # lat_new, long_new = GPS_points[0][0], GPS_points[0][1]
    # lat_old, long_old = GPS_points[1][0], GPS_points[1][1]

    # latitude = y-coord. longitude = x-coord.
    # coord = [x-coord, y-coord] in the reference frame of the car -> current_position: origin [0, 0] 
    coord = [0., 0.]
    coord[0] = GPS_points[0][1] - GPS_points[1][1]
    coord[1] = GPS_points[0][0] - GPS_points[1][0]

    phi = math.atan2(coord[1], coord[0])

    return phi
