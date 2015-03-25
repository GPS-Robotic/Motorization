#from log import *
import sensors
import time
from navigation import * 
from drive import *
import math	# for checking whether GPS is a number
import gpsdData as GPS


#----------------------------------------------------------------------------------------#
#definitions

output = True # gives output if True

print_log_obj = open('print_log.txt', 'w')

def print_log(message):
	print message
	print_log_obj.write(message)

global current_status
global desired_status 

#obstacle distance
obstacle = 75.0 #cm

global GPS_destination
GPS_destination = [49.418045, 8.669307] 

gps_waiting_time = 0.5 # time in seconds in while-loop for waiting for valid GPS
update_time = 1 # time in seconds in while-loop for updating gps, current_status & desired_status

log_file_name='log/RC_log'+str(time.time())+'.txt'

# distance to target
accuracy = 0.000001 # when is the target reached?? accuracy in meter
current_distance = accuracy * 10 # dummy value for current distance in meter#

#Turn variable to remember turning right or left 
Turn = False

#----------------------------------------------------------------------------------------#

#initialization

#start sensors
sens = sensors.sensors(mode=3, start=True)

# start GPS
print "[01] start GPS"
gpsp=GPS.GpsPoller()

# initialisiere Fahrtregler
current_status = ['break', 'slow', 'straight'] # actually one has to initialize to that!
desired_status = current_status
driving(current_status,desired_status) #init Fahrtregler
time.sleep(2)

#log_file = log_class(log_file_name)

print "[02] file opened: " + log_file_name

print "[03] Waiting for valid GPS-information:"
time.sleep(2)
print gpsp.data

while (math.isnan(gpsp.data[0])):
	time.sleep(gps_waiting_time)
	print "still waiting... "
	print gpsp.data

print "[04] got valid GPS-data:"
print gpsp.data

print "[05] drive straight to find heading"
GPS_memory = [0, 0]      # [newest data, second latest data]
start_go = time.time()
wait_go = 7.5

GPS_memory[0] = gpsp.data[0:2]
print 'start finding heading/n/n'
while sens.measurements[0][0] > obstacle and sens.measurements[2][0] > obstacle and time.time() - start_go < wait_go:
	driving(current_status, ['forward', 'slow', 'straight'])
	time.sleep(1)
	driving(current_status, ['forward', 'null', 'straight'])
	time.sleep(1)

driving(current_status, ['break', 'slow', 'straight'])

GPS_memory[1] = gpsp.data[0:2]

print "[06] start routine"



#----------------------------------------------------------------------------------------#
# Main loop to navigate to target
#x = raw_input("Press enter to start")

#while([x[0] for x in sens.measurements[1]].min() == 0):
#	pass

if output: print_log ( 'While loop starts\n')
while current_distance > accuracy:
	print "wrote log-entry:"
	#print log_file.add_log(current_status, gpsp.data)
	if output: print_log ("beginn of loop\n__________________________________\n\n")
	
	if sens.measurements[0][0] < obstacle or sens.measurements[2][0] < obstacle: #or sens.measurements[1][0][0] < obstacle/3.0 or sens.measurements[1][-1][0] < obstacle/3.0:
		if output: print_log ( 'potential obstacle found!\n\n')
		desired_status = ['break', 'slow', 'straight']
		driving(current_status,desired_status) #put this here to make reaction to obstacles faster
		time.sleep(1) 	#maybe wait for actual time needed to update all measurements
		if sens.measurements[0][0] < obstacle or sens.measurements[2][0] < obstacle:
		#time.sleep(1)
			if output: print_log ( 'real obstacle found!\n\n')
			desired_status = ['break', 'slow', 'straight']
			if output: print_log ( 'steer left 90 after break!\n\n')
			left90(current_status,desired_status)
			time.sleep(.5)
		else:
			if output: print_log ( 'no real obstacle found!\n\n')
			desired_status = ['forward', 'slow', 'straight']
	else:
		if not Turn:
			print 'get direction from GPS!'
			reference_direction = get_direction(GPS_destination, gpsp.data, GPS_memory)
		
		#if you have to steer more than 90 degree right or left do it manually in the main function
		if reference_direction <= -90:					 
			desired_status = ['break', 'slow', 'straight']
			left90(current_status,desired_status,speed='middle')
			time.sleep(1)
			reference_direction += 90
			Turn = True
		elif reference_direction >= 90:
			desired_status = ['break', 'slow', 'straight']
			right90(current_status,desired_status,speed='middle')
			time.sleep(1) 
			reference_direction -= 90
			Turn = True	
		else:
			print 'driving towards goal!'
			Turn = False
			#steering direction in degree.
			desired_status = navigate(sens.measurements[1], 0*obstacle, reference_direction)
			if desired_status == -1:					 
				desired_status = ['break', 'slow', 'straight']
				left90(current_status,desired_status,speed='middle')
				time.sleep(1)
				reference_direction += 90
				Turn = True
			else:
				driving(current_status,desired_status)
				time.sleep(0.5)
				out = str(sens.running) + ": " + str(sens.measurements[0][0]) + ", ("
			        for entry in sens.measurements[1]:
			                out = out + str(entry[0]) + ", "
				out = out + "), "  + str(sens.measurements[2][0])
				if output: print_log ( out + "\n")
				if output: print_log ( "let it roll a bit, for 1 second.\n")
				desired_status = ['forward', 'null', 'straight']
				driving(current_status,desired_status) 
				time.sleep(0.5)			

				# Pause if GPS-Position is lost:
				if (math.isnan(gpsp.data[1])):
					print "GPS position lost! Stopping car and waiting for valid GPS-information:"
					driving(current_status, ['break', 'slow', 'straight'])
					print gpsp.data
					while (math.isnan(gpsp.data[0])):
						time.sleep(gps_waiting_time)
						print "still waiting... "
						print gpsp.data			

					print "[04] got valid GPS-data, continue driving:"
					print gpsp.data			

				current_distance = math.sqrt((GPS_destination[0]-gpsp.data[0])*(GPS_destination[0]-gpsp.data[0])+(GPS_destination[1]-gpsp.data[1])*(GPS_destination[1]-gpsp.data[1]))			
				print 'calculate new distance to target: ' + str(current_distance)
				if (gpsp.data[0] - GPS_memory[1][0]) < accuracy/10. or (gpsp.data[1] - GPS_memory[1][1]) < accuracy/10.:
					GPS_memory[0] = GPS_memory[1]
			    	GPS_memory[1] = gpsp.data[0:2]
			    
	print GPS_memory

print "[08] destination reached. stop."

#log_file.stop()	




