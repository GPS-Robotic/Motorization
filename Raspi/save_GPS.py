import time
import debug_log
lg = debug_log.debug_print()
import gpsdData
gps = gpsdData.GpsPoller()

fn=" "

while fn != 'no':
	print "save gps data as list"
	fn = raw_input("filename? i.e. GPS_DATA1.txt ")
	print

	filex = open(fn, "w")

	for i in range(240):
		print str(i) + ": "+ str(gps.data[0:2])
		filex.write(str(gps.data[0])+","+str(gps.data[1])+"\n")
		time.sleep(0.5)
	
	filex.close()

	fn = raw_input("no for quit")

gps.running = False
