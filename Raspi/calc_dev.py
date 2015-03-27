import numpy

for i in [1,2]:
	filex = open("GPS_DATA0" + str(i) + ".txt", "r")

	lat_dat = []
	long_dat = []

	for line in filex:
		raw_dat=((line.replace(" ", "")).replace("\n","")).split(",")
		lat_dat.append(float(raw_dat[0]))
		long_dat.append(float(raw_dat[1]))

	filex.close()

	print "\n"
	print "file " + str(i) + ", latitude:  " + str(numpy.mean(lat_dat)) + " +/- " + str(numpy.std(lat_dat))
	print "file " + str(i) + ", longitude: " + str(numpy.mean(long_dat)) + " +/- " + str(numpy.std(long_dat))
	print "\n"
