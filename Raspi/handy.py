# Program for remote-controlling the RC-car via cell-phone

import sys
from RPIO import PWM
from time import sleep

print
if len(sys.argv)!=2:
	print "too many/few arguments, exit program...."
else:
	GPIO_Servo=17
	GPIO_Motor=4
	servo = PWM.Servo()
	arg=sys.argv[1]

	#define Servopositions for steering
	#	values adjusted to incrementer 10us (micro-seconds)
	Offset = 50
	Left = 1900+Offset
	Half_Left = 1700+Offset #needed?
	Straight = 1500+Offset
	Half_Right = 1300+Offset #needed?
	Right = 1100+Offset

	#define Servopositions for steering
	#	values adjusted to incrementer 10us (micro-seconds)
	Null = 1500
	Slow = 100	#check these values!!! starts from 1550
	Middle = 200
	Fast = 300

	#define waiting time between stop and steer in seconds
	Sleeping_Time=.5

	if arg=="break":
		servo.set_servo(GPIO_Motor, (Null-Fast))
		sleep(Sleeping_Time)
		servo.set_servo(GPIO_Motor, (Null))
		print "breaking..."
	elif arg=="roll-off":
		servo.set_servo(GPIO_Motor, (Null))
		print "turning off the motor...."

	elif arg=="slow-forward":
		servo.set_servo(GPIO_Motor, (Null+Slow))
		print "driving forward slowly..."
	elif arg=="middle-forward":
		servo.set_servo(GPIO_Motor, (Null+Middle))
		print "driving forward with medium speed..."
	elif arg=="fast-forward":
		servo.set_servo(GPIO_Motor, (Null+Fast))
		print "driving forward fast..."

	elif arg=="slow-backward":
		servo.set_servo(GPIO_Motor, (Null-Fast))
		sleep(Sleeping_Time)
		servo.set_servo(GPIO_Motor, (Null))
		sleep(Sleeping_Time)
		servo.set_servo(GPIO_Motor, (Null-Slow))
		print "driving backward slowly..."
	elif arg=="middle-backward":
		servo.set_servo(GPIO_Motor, (Null-Fast))
		sleep(Sleeping_Time)
		servo.set_servo(GPIO_Motor, (Null))
		sleep(Sleeping_Time)
		servo.set_servo(GPIO_Motor, (Null-Middle))
		print "driving backward with medium speed..."
	elif arg=="fast-backward":
		servo.set_servo(GPIO_Motor, (Null-Fast))
		sleep(Sleeping_Time)
		servo.set_servo(GPIO_Motor, (Null))
		sleep(Sleeping_Time)
		servo.set_servo(GPIO_Motor, (Null-Fast))
		print "driving backward fast..."

	elif arg=="left":
		servo.set_servo(GPIO_Servo, Left)
		print "steering full left..."
	elif arg=="half-left":
		servo.set_servo(GPIO_Servo, Half_Left)
		print "steering half left..."
	elif arg=="straight":
		servo.set_servo(GPIO_Servo, Straight)
		print "steering straight..."
	elif arg=="right":
		servo.set_servo(GPIO_Servo, Right)
		print "steering full right..."
	elif arg=="half-right":
		servo.set_servo(GPIO_Servo, Half_Right)
		print "steering half right..."
	else:
		print "unknown argument, exit program...."
sleep(1)
print
