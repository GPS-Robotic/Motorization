# this function shall calculate the distance between to points on a sphere given the longitudes and latitudes. (in meter)
# from http://www.johndcook.com/blog/python_longitude_latitude/
#
# mean earth-radius: 6371km (from http://www.movable-type.co.uk/scripts/latlong.html)

import math
 
def distance_on_unit_sphere(lat1, long1, lat2, long2):
 
    # Convert latitude and longitude to
    # spherical coordinates in radians.
    degrees_to_radians = math.pi/180.0
         
    # phi = 90 - latitude
    phi1 = (90.0 - lat1)*degrees_to_radians
    phi2 = (90.0 - lat2)*degrees_to_radians
         
    # theta = longitude
    theta1 = long1*degrees_to_radians
    theta2 = long2*degrees_to_radians
         
    # Compute spherical distance from spherical coordinates.
         
    # For two locations in spherical coordinates
    # (1, theta, phi) and (1, theta, phi)
    # cosine( arc length ) =
    #    sin phi sin phi' cos(theta-theta') + cos phi cos phi'
    # distance = rho * arc length
     
    cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) +
           math.cos(phi1)*math.cos(phi2))
    arc = math.acos( cos )
 
    # Remember to multiply arc by the radius of the earth
    # in your favorite set of units to get length.
    return arc

def get_target_distance(lat1, long1, lat2, long2):
	return (distance_on_unit_sphere(lat1, long1, lat2, long2) * 6371000) # not sure if correct: anymore factors needed?? seems to work...


# just for tests:

#lat1 = float(raw_input("Latitude 1: "))
#long1 = float(raw_input("Longitude 1: "))
#lat2 = float(raw_input("Latitude 2: "))
#long2 = float(raw_input("Longitude 2: "))

#print str(get_target_distance(lat1, long1, lat2, long2)) + 'm'
