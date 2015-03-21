import sensors
import time
from navigation import navigate
from drive import *

global current_status
global desired_status 

sens = sensors.sensors(mode=2, start=True)

current_status = ['break', 'slow', 'straight'] # actually one has to initialize to that!
desired_status = current_status
driving(current_status,desired_status) #init Fahrtregler
time.sleep(5)

#obstacle distance
obstacle = 100 #cm
#direction to goal in degree
reference_direction=0 #means straight, negative left, positive right!
segment_number = sens.servo_segments
segment_width = 180./float(segment_number) #we defined our servo to scan 180 degrees

raw_input("Press enter to start")

while([x[0] for x in sens.measurements[1]].min() == 0):
	pass

while True:
	if sens.measurements[0][0] < obstacle or sens.measurements[2][0] < obstacle or sens.measurements[1][0][0] < obstacle/2.0 or sens.measurements[1][-1][0] < obstacle/2.:
		desired_status = ['break', 'slow', 'straight']
		driving(current_status,desired_status) #put this here to make reaction to obstacles faster
		time.sleep(1) 	#maybe wait for actual time needed to update all measurements
		if sens.measurements[0][0] < obstacle or sens.measurements[2][0] < obstacle:
		#time.sleep(1)
			desired_status = ['forward', 'slow', 'straight']
			left90(current_status,desired_status)
		else:
			desired_status = ['forward', 'slow', 'straight']
	else:
		steering_direction = navigate(sens.measurements[1],obstacle,reference_direction,segment_width,segment_number)
		#if steering_direction == reference_direction: #do nothing?
		if steering_direction == -1:
			desired_status = ['forward', 'slow', 'straight']
			left90(current_status,desired_status)
		elif steering_direction > reference_direction: #0 is on the left side while 10 is right.
		#steer right
			desired_status = ['forward','slow','half-right']
		elif steering_direction < reference_direction: #0 is on the left side while 10 is right.
		#steer left
			desired_status = ['forward','slow','half-left']
		elif steering_direction == reference_direction:
			desired_status = ['forward', 'slow', 'straight']
		else:
			print 'deine Mutter hat ein Fehler gemacht, Junge!!!'
	driving(current_status,desired_status)
	#scan = sens.measurements[1]
    
	time.sleep(1)
	desired_status = ['forward', 'null', 'straight']
	driving(current_status,desired_status) 
	time.sleep(1)

	




