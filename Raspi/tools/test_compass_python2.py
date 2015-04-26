import gpsdData
import time

gpsp = gpsdData.GpsPoller()

try:
	while True:
		print gpsp.data[3]
		time.sleep(0.1)
except:
	gpsp.running = False
