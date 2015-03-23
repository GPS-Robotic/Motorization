#MAY THE BACKWARD STEERING BE CHANGED?? THIS MAY BECOME CONFUSING!
#NOTE driving-METHOD-COMMENTS

from RPIO import PWM
from time import sleep

servo = PWM.Servo()

#define PIN-Settings (Board-Numbering, not GPIO-Numbering)
#	actually not needed here as we use GPIO-Numbering
#PIN_Servo=11	#Servo-Signal
#PIN_Motor=7	#Motor-Signal
#PIN_SDA=3	#Kompass SDA
#PIN_SCL=5	#Kompass SCL
#PIN_TX=8	#GPS TX
#PIN_RX=10	#GPS RX

#define PIN-Settings (GPIO-Numbering, not Board-Numbering)
GPIO_Servo=17
GPIO_Motor=4
#GPIO_SDA=2	# not needed in this module
#GPIO_SCL=3
#GPIO_TX=14
#GPIO_RX=15

#define Servopositions for steering
#	values adjusted to incrementer 10us (micro-seconds)
Offset=50	#for fine-adjusting the steering
Left = 1900 + Offset
Half_Left = 1700 + Offset #needed?
Straight = 1500 + Offset
Half_Right = 1300 + Offset #needed?
Right = 1100 + Offset

#define Servopositions for steering
#	values adjusted to incrementer 10us (micro-seconds)
Null = 1500
Slow = 100	#check these values!!! starts from 1550
Middle = 200
Fast = 300
Slow_Offset = 10
#define waiting time between stop and steer in seconds
Sleeping_Time=.5

#define time needed for 90-degrees-turn (ADJUST!)
Sleeping_Time_90={"slow":0.63,"middle":0.2,"fast":0.083}

# Clear servo on GPIO_Servo
#servo.stop_servo(GPIO_Servo)


# steering function, current_status and desired_status are lists, containing the vehicle status
# status = [direction,velocity,steer position] with:
#	direction = break, forward or backward
#	velocity = fast, middle or slow
#	steer position = left, half-left, straight, half-right or right


def steer(current_status, desired_status):
	steering_error=0
	if (current_status[0]=='forward') or (current_status[0]=='break'):
		if desired_status[2]=='left':
			# Set steering servo on GPIO_Servo to left
			servo.set_servo(GPIO_Servo, Left)
		elif desired_status[2]=='half-left':
			# Set steering servo on GPIO_Servo to half left
			servo.set_servo(GPIO_Servo, Half_Left)
		elif desired_status[2]=='right':
			# Set steering servo on GPIO_Servo to right
			servo.set_servo(GPIO_Servo, Right)
		elif desired_status[2]=='half-right':
			# Set steering servo on GPIO_Servo to half right
			servo.set_servo(GPIO_Servo, Half_Right)
		elif desired_status[2]=='straight':
			# Set steering servo on GPIO_Servo to straight
			servo.set_servo(GPIO_Servo, Straight)
		else:
			steering_error=1
			print 'ERROR: Non directional information passed to steering function: current_status[0]=forward or break, desired_status[2]=' + desired_status[2] + ' is unknown!'

	elif current_status[0]=='backward':
		if desired_status[2]=='left':
			# Set steering servo on GPIO_Servo to left (backw.)
			servo.set_servo(GPIO_Servo, Right)
		elif desired_status[2]=='half-left':
			# Set steering servo on GPIO_Servo to half left (backw.)
			servo.set_servo(GPIO_Servo, Half_Right)
		elif desired_status[2]=='right':
			# Set steering servo on GPIO_Servo to right (backw.)
			servo.set_servo(GPIO_Servo, Left)
		elif desired_status[2]=='half-right':
			# Set steering servo on GPIO_Servo to half right (backw.)
			servo.set_servo(GPIO_Servo, Half_Left)
		elif desired_status[2]=='straight':
			# Set steering servo on GPIO_Servo to straight (backw.)
			servo.set_servo(GPIO_Servo, Straight)
		else:
			steering_error=1
			print 'ERROR: Non directional information passed to steering function: current_status[0]=backward, desired_status[2]=' + desired_status[2] + ' is unknown!'
	else:
		steering_error=1
		print 'ERROR: Unknown driving direction passed to steering function: currrent_status[0]=' + current_status[0] + ' is unknown!'

#	update current_status if operation succeeded
	if(steering_error==0):
		current_status[2]=desired_status[2]



#motor function
def accelerate(current_status, desired_status):
	acceleration_error=0
	if current_status[0]=='forward':
		if desired_status[0]=='break':
			# Set motor on GPIO_Motor to fast backward in order to break
			servo.set_servo(GPIO_Motor, (Null-Fast)) #break
			sleep(Sleeping_Time)
			servo.set_servo(GPIO_Motor, Null) #stop

		elif desired_status[0]=='forward':
			if desired_status[1]=='fast':
				# Set motor on GPIO_Motor to fast forward
				servo.set_servo(GPIO_Motor, (Null+Fast))
			elif desired_status[1]=='middle':
				# Set motor on GPIO_Motor to middle forward
				servo.set_servo(GPIO_Motor, (Null+Middle))
			elif desired_status[1]=='slow':
				# Set motor on GPIO_Motor to slow forward
				servo.set_servo(GPIO_Motor, (Null+Slow-Slow_Offset))
			elif desired_status[1]=='null':
				# Set motor on GPIO_Motor to null position #Leerlauf
				servo.set_servo(GPIO_Motor, (Null))
			else:
				acceleration_error=1
				print 'ERROR: Non speed information passed to accelerate function: current_status[0]=forward, desired_status[0]=forward, desired_status[1]=' + desired_status[1] + ' is unknown!'

		elif desired_status[0]=='backward':
			if desired_status[1]=='fast':
				# Break and then set motor on GPIO_Motor to fast backwards 
				servo.set_servo(GPIO_Motor, (Null-Fast)) #break
				sleep(Sleeping_Time)
				servo.set_servo(GPIO_Motor, (Null)) #stop
				sleep(Sleeping_Time)
				servo.set_servo(GPIO_Motor, (Null-Fast)) #fast backward
			elif desired_status[1]=='middle':
				# Break and then set motor on GPIO_Motor to middle backwards
				servo.set_servo(GPIO_Motor, (Null-Fast)) #break
				sleep(Sleeping_Time)
				servo.set_servo(GPIO_Motor, (Null)) #stop
				sleep(Sleeping_Time)
				servo.set_servo(GPIO_Motor, (Null-Middle)) #middle backward
			elif desired_status[1]=='slow':
				# Break and then set motor on GPIO_Motor to slow backward
				servo.set_servo(GPIO_Motor, (Null-Fast)) #break
				sleep(Sleeping_Time)
				servo.set_servo(GPIO_Motor, (Null)) #stop
				sleep(Sleeping_Time)
				servo.set_servo(GPIO_Motor, (Null-Slow-Slow_Offset)) #slow backward
			elif desired_status[1]=='null':
				# Set motor on GPIO_Motor to null position #Leerlauf
				servo.set_servo(GPIO_Motor, (Null))
			else:
				acceleration_error=1
				print 'ERROR: Non speed information passed to accelerate function: current_status[0]=forward, desired_status[0]=backward, desired_status[1]=' + desired_status[1] + ' is unknown!'
		else:
			acceleration_error=1
			print  'Unknown driving directive passed to accelerate function: current_status[0]=forward, desired_status[0]=' + desired_status[0] + ' is unknown!'

	elif current_status[0]=='backward':
		if desired_status[0]=='break':
			# Set motor on GPIO_Motor to null
			servo.set_servo(GPIO_Motor, Null)

		elif desired_status[0]=='backward':
			if desired_status[1]=='fast':
				# Set motor on GPIO_Motor to fast backward
				servo.set_servo(GPIO_Motor, (Null-Fast))
			elif desired_status[1]=='middle':
				# Set motor on GPIO_Motor to middle backward
				servo.set_servo(GPIO_Motor, (Null-Middle))
			elif desired_status[1]=='slow':
				# Set motor on GPIO_Motor to slow backward
				servo.set_servo(GPIO_Motor, (Null-Slow-Slow_Offset))
			elif desired_status[1]=='null':
				# Set motor on GPIO_Motor to null position #Leerlauf
				servo.set_servo(GPIO_Motor, (Null))
			else:
				acceleration_error=1
				print 'ERROR: Non speed information passed to accelerate function: current_status[0]=backward, desired_status[0]=backward, desired_status[1]=' + desired_status[1] + ' is unknown!'

		elif desired_status[0]=='forward':
			if desired_status[1]=='fast':
				# Set motor on GPIO_Motor to fast forward
				servo.set_servo(GPIO_Motor, (Null+Fast))
			elif desired_status[1]=='middle':
				# Set motor on GPIO_Motor to middle forward
				servo.set_servo(GPIO_Motor, (Null+Middle))
			elif desired_status[1]=='slow':
				# Set motor on GPIO_Motor to slow forward
				servo.set_servo(GPIO_Motor, (Null+Slow-Slow_Offset))
			elif desired_status[1]=='null':
				# Set motor on GPIO_Motor to null position #Leerlauf
				servo.set_servo(GPIO_Motor, (Null))
			else:
				acceleration_error=1
				print 'ERROR: Non speed information passed to accelerate function: current_status[0]=backward, desired_status[0]=forward, desired_status[1]=' + desired_status[1] + ' is unknown!'
		else:
			acceleration_error=1
			print 'ERROR: Unknown driving directive passed to accelerate function: current_status[0]=backward, desired_status[0]=' + desired_status[0] + ' is unknown!'

	elif current_status[0]=='break':
		if desired_status[0]=='break':
			servo.set_servo(GPIO_Motor, Null) #stop

		elif desired_status[0]=='forward':
			if desired_status[1]=='fast':
				# Set motor on GPIO_Motor to fast forward
				servo.set_servo(GPIO_Motor, (Null+Fast))
			elif desired_status[1]=='middle':
				# Set motor on GPIO_Motor to middle forward
				servo.set_servo(GPIO_Motor, (Null+Middle))
			elif desired_status[1]=='slow':
				# Set motor on GPIO_Motor to slow forward
				servo.set_servo(GPIO_Motor, (Null+Slow-Slow_Offset))
			elif desired_status[1]=='null':
				# Set motor on GPIO_Motor to null position #Leerlauf
				servo.set_servo(GPIO_Motor, (Null))
			else:
				acceleration_error=1
				print 'ERROR: Non speed information passed to accelerate function: current_status[0]=break, desired_status[0]=forward, desired_status[1]=' + desired_status[1] + ' is unknown!'

		elif desired_status[0]=='backward':
			if desired_status[1]=='fast':
				# Set motor on GPIO_Motor to fast backward
				servo.set_servo(GPIO_Motor, (Null-Fast))
			elif desired_status[1]=='middle':
				# Set motor on GPIO_Motor to middle backward
				servo.set_servo(GPIO_Motor, (Null-Middle))
			elif desired_status[1]=='slow':
				# Set motor on GPIO_Motor to slow backward
				servo.set_servo(GPIO_Motor, (Null-Slow-Slow_Offset))
			elif desired_status[1]=='null':
				# Set motor on GPIO_Motor to null position #Leerlauf
				servo.set_servo(GPIO_Motor, (Null))
			else:
				acceleration_error=1
				print 'ERROR: Non speed information passed to accelerate function: current_status[0]=break, desired_status[0]=backward, desired_status[1]=' + desired_status[1] + ' is unknown!'
		else:
			acceleration_error=1
			print 'ERROR: Unknown driving directive passed to accelerate function: current_status[0]=break, desired_status[0]=' + desired_status[0] + ' is unknown!'

	else:
		acceleration_error=1
		print 'ERROR: Unknown driving directive passed to accelerate function: current_status[0]=' + current_status[0] + ' is unknown!'

#	update current_status if operation succeeded
	if(acceleration_error==0):
		for i in (0,1):
			current_status[i]=desired_status[i]

#function to print out a given status
def print_status(status):
	print ' '
	print 'Status:'
	print '		direction=		' + status[0]
	print '		velocity=		' + status[1]
	print '		steering position=	' + status[2]
	print ' '

#driving function for both, steering first and accelerating afterwards
#CAUTION: It is important to call acceleration first to avoid wrong direction-steering
#	example: you drive forward and want to go left backward
#		 thus, calling "left" first will result in different ending than calling "backward" first!
#MAY THIS BE CHANGED???
def driving(current_status, desired_status):
	accelerate(current_status, desired_status)	#first accelerate
	steer(current_status, desired_status)	#then steer

#function for turning 90 degrees right & continue with desired_status
#speed=slow, middle, fast (for turning process only)
#CAUTION: time-delay....
def right90(current_status, desired_status, speed='slow'):
	accelerate(current_status, ['break',speed,'right'])	#break
	sleep(Sleeping_Time)
	driving(current_status, ['backward',speed,'right'])	#turn right backwards
	sleep(5.0*Sleeping_Time_90[speed])	#wait X-seconds to turn -> ADJUST!
	driving(current_status, ['forward',speed,'right'])	#turn right forward
	sleep(Sleeping_Time_90[speed])
	driving(current_status, desired_status)

#function for quickly turning 90 degrees right & continue with desired_status
#speed=slow, middle, fast (for turning process only)
#CAUTION: time-delay....
def left90(current_status, desired_status, speed='slow'):
	accelerate(current_status, ['break',speed,'left'])	#break
	sleep(Sleeping_Time)
	driving(current_status, ['backward',speed,'left'])	#turn right backwards
	sleep(5.0*Sleeping_Time_90[speed])	#wait X-seconds to turn -> ADJUST!
	driving(current_status, ['forward',speed,'left'])	#turn right forward
	sleep(Sleeping_Time_90[speed])
	driving(current_status, desired_status)

def left90test(current_status, desired_status, delay_time, speed='slow'):
	accelerate(current_status, ['break',speed,'left'])	#break
	sleep(Sleeping_Time)
	driving(current_status, ['backward',speed,'left'])	#turn right backwards
	sleep(5.0*delay_time)	#wait X-seconds to turn -> ADJUST!
	driving(current_status, ['forward',speed,'left'])	#turn right forward
	sleep(delay_time)
	driving(current_status, desired_status)


#function for quickly turning 90 degrees right & continue with desired_status
#speed=slow, middle, fast (for turning process only)
#CAUTION: time-delay....
def turn180(current_status, desired_status, speed='slow'):
	right90(current_status, desired_status, speed)
	right90(current_status, desired_status, speed)
	#sleep(Sleeping_Time_90[speed])
	#driving(current_status, desired_status)
