import sensors
import time
import navigation
from drive import *

global current_status
current_status = ['break', 'slow', 'straight'] # actually one has to initialize to that!
global desired_status 
desired_status = current_status

driving(current_status,desired_status)

time.sleep(1)

sens = sensors.sensors(mode=1, start=False)

#obstacle distance
obstacle = 50 #cm
#direction to goal in degree or scanning segment of sensor 2
reference_direction=5
#

raw_input("Press enter to start")
sens.start()

time.sleep(1)

while True:
	scan = sens.measurements[1]
	if sens.measurements[0][0] < obstacle/2. or sens.measurements[2][0] < obstacle/2.:
		desired_status = ['break', 'slow', 'straight']
		driving(current_status,desired_status) #put this here to make reaction to obstacles faster
		time.sleep(1)
		desired_status = ['backward', 'slow', 'straight']
		time.sleep(1)
		#for proper u-turn implement something like second best choice last time a direction adjustment was made.
		desired_status = ['backward', 'slow', 'left']
	else:
		steering_direction = navigate(scan,obstacle,reference_direction)
		#if steering_direction == reference_direction: #do nothing?
		if steering_direction > reference_direction: #0 is on the left side while 10 is right.
		#steer right
		desired_status = ['forward','slow','half-right']
		elif steering_direction < reference_direction: #0 is on the left side while 10 is right.
		#steer left
		desired_status = ['forward','slow','half-left']
	driving(current_status,desired_status)





