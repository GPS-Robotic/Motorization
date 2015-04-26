# This script starts gpsdData.py as background-thread and displays the compass-data.
# May be used to check wether the compass delivers valid data.

import gpsdData
import time

gpsp = gpsdData.GpsPoller()

try:
	while True:
		print gpsp.data[3]
		time.sleep(0.1)
except:
	gpsp.running = False
