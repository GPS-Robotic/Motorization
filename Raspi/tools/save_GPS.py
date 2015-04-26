# This script continously saves GPS-data to a file in the format 'lat,long' for debbuging-issues
# for example one afterwards can calculate the average & standard-deviation via calc_dev.py

import time
import debug_log
lg = debug_log.debug_print()
import gpsdData
gps = gpsdData.GpsPoller()

fn=" "

while fn != 'no':
	print "save gps data as list"
	fn = raw_input("filename? e.g. GPS_DATA1.txt")
	print

	filex = open(fn, "w")

	for i in range(240):
		print str(i) + ": "+ str(gps.data[0:2])
		filex.write(str(gps.data[0])+","+str(gps.data[1])+"\n")
		time.sleep(0.5)
	
	filex.close()

	fn = raw_input("next filename? no for quit ")

gps.running = False
