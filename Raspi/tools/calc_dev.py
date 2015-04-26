# This script calculates the average & standard-deviation of GPS-data given in a file
# in the format latitude,longitude (linewise)

import numpy

print "calculate average lat/long with error"
fn = raw_input("filename? i.e. GPS_DATA1.txt ")
print

filex = open(fn, "r")

lat_dat = []
long_dat = []

for line in filex:
	raw_dat=((line.replace(" ", "")).replace("\n","")).split(",")
	lat_dat.append(float(raw_dat[0]))
	long_dat.append(float(raw_dat[1]))

filex.close()

print "\n"
print "latitude:  " + str(numpy.mean(lat_dat)) + " +/- " + str(numpy.std(lat_dat))
print "longitude: " + str(numpy.mean(long_dat)) + " +/- " + str(numpy.std(long_dat))
print "\n"
