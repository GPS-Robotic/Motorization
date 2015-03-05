import sensors
import time

sens = sensors.sensors(mode=1, start=True)
while True:
	print sens.measurements
	time.sleep(1)
