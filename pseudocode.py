# Pseudocode zur Strukturierung

drive.py

drive.steer(current_status, desired_status)         # status = [direction,velocity,steer position]
drive.accelerate(current_status, desired_status)
drive.print_status(status)
drive.driving(current_status, desired_status)       # first accelerate, then steer
drive.right90(current_status, desired_status, speed='middle')
drive.left90(current_status, desired_status, speed='middle')
drive.turn180(current_status, desired_status, speed='middle')


log.py

add_log(current_status, GPS_data) # saves all neccessary data to file. see log.py for details


gpsData.py      # Max: made edit which should output important data. Not sure though.
		# Phil: corrected that one. should work now


direction.py

get_direction(GPS_destination, GPS_data, desired_status) # Function which shall calculate the desired direction
		#NOTE: get_direction maybe needs to be modified including current_status in order to drive better curves....


distance_target.py

get_target_distance(lat1, long1, lat2, long2) # calculates distance between two points on earth 
					      # (accuracy unknown, does not use altitude, assumes perfect sphere)
distance_on_unit_sphere(lat1, long1, lat2, long2) # calculates distance of two points on unit-sphere


init.py

init() # for initialization (what would we need??)


main.py	# overall function to test everything
