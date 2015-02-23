import time
import drive

current_status=['break','slow','straight']
desired_status=['break','slow','straight']


while True:
	raw_input("drive?")
	desired_status[0]='forward'
	drive.driving(current_status,desired_status)
	raw_input("stop?")
	desired_status[0]='break'
	drive.driving(current_status,desired_status)

