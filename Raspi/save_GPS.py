import time
import gpsdData

gps = gpsdData.GpsPoller()

filex = open("GPS_DATA" + str(time.time) + ".txt", "w")

for i in range(240):
	print i
	filex.write(str(gps.data[0:2]))
	time.sleep(0.5)
