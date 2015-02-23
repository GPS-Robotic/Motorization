import time
import drive

waiting_time=0.5

print ' '
print 'Starting Test....'

current_status=['break','slow','straight']
desired_status=['break','slow','straight']

print ' '
print 'go to starting position: break, straight'

drive.driving(current_status,desired_status)

time.sleep(waiting_time)

#hr
desired_status[2]='half-right'
print 'current:'
drive.print_status(current_status)
print 'desired:'
drive.print_status(desired_status)
drive.driving(current_status,desired_status)
time.sleep(waiting_time)

#r
desired_status[2]='right'
print 'current:'
drive.print_status(current_status)
print 'desired:'
drive.print_status(desired_status)
drive.driving(current_status,desired_status)
time.sleep(waiting_time)

#l
desired_status[2]='left'
print 'current:'
drive.print_status(current_status)
print 'desired:'
drive.print_status(desired_status)
drive.driving(current_status,desired_status)
time.sleep(waiting_time)

#hl
desired_status[2]='half-left'
print 'current:'
drive.print_status(current_status)
print 'desired:'
drive.print_status(desired_status)
drive.driving(current_status,desired_status)
time.sleep(waiting_time)

#s
desired_status[2]='straight'
print 'current:'
drive.print_status(current_status)
print 'desired:'
drive.print_status(desired_status)
drive.driving(current_status,desired_status)
time.sleep(waiting_time)

#hr slow fow
desired_status[2]='straight'
desired_status[0]='forward'
desired_status[1]='slow'
print 'current:'
drive.print_status(current_status)
print 'desired:'
drive.print_status(desired_status)
drive.driving(current_status,desired_status)
time.sleep(waiting_time)

#hr
desired_status[2]='straight'
desired_status[0]='backward'
print 'current:'
drive.print_status(current_status)
print 'desired:'
drive.print_status(desired_status)
drive.driving(current_status,desired_status)
time.sleep(2*waiting_time)


desired_status[0]='break'
drive.driving(current_status,desired_status)


while(True):
	desired_status[0]=raw_input('direction?')
	desired_status[1]=raw_input('velocity?')
	desired_status[2]=raw_input('steering?')
	delay=raw_input('delay time before stopping?')
	print 'current:'
	drive.print_status(current_status)
	print 'desired:'
	drive.print_status(desired_status)
	drive.driving(current_status,desired_status)
	time.sleep(int(delay))
	raw_input('hit enter')	
	desired_status[0]='break'
	desired_status[2]='straight'
	drive.driving(current_status,desired_status)
