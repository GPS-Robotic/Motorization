from RPIO import PWM
from time import sleep

servo = PWM.Servo()

#define Servopositions for steering
#check this
Left = 700
Half_left = 900 #needed?
Straight = 1100
Half_right = 1300 #needed?
Right = 1500  

#define Servopositions for steering
Null = 1500
Slow = 100
Middle = 200
Fast = 300

# Clear servo on GPIO17
#servo.stop_servo(17)


# steering function, current_status and desired_status are lists, containing the vehicle status
# status = [direction,velocity,steer position] where direction means forward or backwards
def steer(current_status, desired_status):
	if current_status[0]=='forward':
		if desired_status[2]=='left':
			# Set steering servo on GPIO17 to left
			servo.set_servo(17, Left)
		elif desired_status[2]=='half_left';
			# Set steering servo on GPIO17 to half right
			servo.set_servo(17, Half_left)
		elif desired_status[2]=='right';
			# Set steering servo on GPIO17 to right
			servo.set_servo(17, Right)
		elif desired_status[2]=='half_right';
			# Set steering servo on GPIO17 to half right
			servo.set_servo(17, Half_right)
		elif desired_status[2]=='straight'
			servo.set_servo(17, Straight)
		else:
			print 'Non directional information passed to steering function!'
	elif current_status[0]=='backward':
		if desired_status[2]=='left':
			# Set steering servo on GPIO17 to left
			servo.set_servo(17, Right)
		elif desired_status[2]=='half_left';
			# Set steering servo on GPIO17 to half right
			servo.set_servo(17, Half_right)
		elif desired_status[2]=='right';
			# Set steering servo on GPIO17 to right
			servo.set_servo(17, Left)
		elif desired_status[2]=='half_right';
			# Set steering servo on GPIO17 to half right
			servo.set_servo(17, Half_left)
		elif desired_status[2]=='straight'
			servo.set_servo(17, Straight)
		else:
			print 'Non directional information passed to steering function!'
	else:
		print 'Unknown driving direction passed to steering function!'

#motor function
def accelerate(current_status, desired_status):
	if current_status[0]=='forward':
		if desired_status[0]=='break':
			# Set motor on GPIO18 to fast backward
			servo.set_servo(18, (Null-Fast))
			sleep(2)
			servo.set_servo(18, Null)
		if desired_status[0]=='forward':
			if desired_status[1]=='fast':
				# Set motor on GPIO18 to fast
				servo.set_servo(18, (Null+Fast))
			elif desired_status[2]=='middle';
				# Set motor on GPIO18 to middle
				servo.set_servo(18, (Null+Middle))
			elif desired_status[2]=='slow';
				# Set motor on GPIO18 to slow
				servo.set_servo(18, (Null+Slow))
			else:
				print 'Non speed information passed to steering function!'

		elif desired_status[0]=='backward':
			if desired_status[1]=='fast':
				# Set motor on GPIO18 to fast backwards
				servo.set_servo(18, Null)
				sleep(1)
				servo.set_servo(18, (Null-Fast))
			elif desired_status[2]=='middle';
				# Set motor on GPIO18 to middle backwards
				servo.set_servo(18, Null)
				sleep(1)
				servo.set_servo(18, (Null-Middle))
			elif desired_status[2]=='slow';
				# Set motor on GPIO18 to slow backwards
				servo.set_servo(18, Null)
				sleep(1)
				servo.set_servo(18, (Null-Slow))
			else:
				print 'Non speed information passed to steering function!'
		else:
			print  'Unknown driving direction passed to steering function!'

	elif current_status[0]=='backward':
		if desired_status[0]=='break':
			# Set motor on GPIO18 to fast backward
			servo.set_servo(18, (Null+Fast))
			sleep(2)			#maybe too long, check
			servo.set_servo(18, Null)
		if desired_status[0]=='backward':
			if desired_status[1]=='fast':
				# Set motor on GPIO18 to fast
				servo.set_servo(18, (Null-Fast))
			elif desired_status[2]=='middle';
				# Set motor on GPIO18 to middle
				servo.set_servo(18, (Null-Middle))
			elif desired_status[2]=='slow';
				# Set motor on GPIO18 to slow
				servo.set_servo(18, (Null-Slow))
			else:
				print 'Non speed information passed to steering function!'

		elif desired_status[0]=='forward':
			if desired_status[1]=='fast':
				# Set motor on GPIO18 to fast backwards
				servo.set_servo(18, Null)
				sleep(1)
				servo.set_servo(18, (Null+Fast))
			elif desired_status[2]=='middle';
				# Set motor on GPIO18 to middle backwards
				servo.set_servo(18, Null)
				sleep(1)
				servo.set_servo(18, (Null+Middle))
			elif desired_status[2]=='slow';
				# Set motor on GPIO18 to slow backwards
				servo.set_servo(18, Null)
				sleep(1)
				servo.set_servo(18, (Null+Slow))
			else:
				print 'Non speed information passed to steering function!'
		else:
		print 'Unknown driving direction passed to steering function!'
	else:
		print 'Unknown driving direction passed to steering function!'

