from range_sensor import get_distance
import time
import drive
from RPIO import PWM

servo = PWM.Servo()
SERVO = 6 # for moving sensor 2 (GPIO-Numbering, NOT BOARD-Numbering)

NULL = 1490
MAX = 2000
MIN = 1000
STEP = 50

current_status = ["break","slow","straight"]
desired_status = ["forward","slow","straight"]
abstand = 25
temp = [0,0,0]
temp2 = [0,0,0]
dist2 = [0,0,0]
servo.set_servo(SERVO, NULL)

raw_input("Press anything to continue!")

while True:
	drive.driving(current_status,desired_status)
	for value in range(MIN, MAX-STEP, STEP):
		servo.set_servo(SERVO, value)
		#print(chr(27) + "[2J")
		dist=""
		for i in [1,2]:
			temp[i] = get_distance(i)
		for i in [1,2]:
			temp2[i] = get_distance(i)
			dist2[i] = (temp[i] + temp2[i])/2. 
			dist=dist + str(round(dist2[i],2)) + "\t "
			if dist2[i] <= abstand:
				desired_status=['break','slow','straight']
        		        drive.driving(current_status,desired_status)
      			        print str(dist2[i])
				print str(i)
				time.sleep(10)
                		desired_status=['forward','slow','straight']
                		drive.driving(current_status,desired_status)
		print "Servo= " + str(value) + ", Distances[cm]= " + str(dist)

	for value in range(MAX, MIN+STEP, -STEP):
		servo.set_servo(SERVO, value)
		dist=""
		for i in [1,2]:
                	temp[i] = get_distance(i)
		for i in [1,2]:
        	        temp2[i] = get_distance(i)
                        dist2[i] = (temp[i] + temp2[i])/2.
                        dist=dist + str(round(dist2[i],2)) + "\t "
                        if dist2[i] <= abstand:
                                desired_status=['break','slow','straight']
                                drive.driving(current_status,desired_status)
                                print str(dist2[i])
				print str(i)
				time.sleep(10)
                                desired_status=['forward','slow','straight']
                                drive.driving(current_status,desired_status)
		print "Servo= " + str(value) + ", Distances[cm]= " + str(dist)
