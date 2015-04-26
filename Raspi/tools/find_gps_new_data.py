#! /usr/bin/python
# Written by Dan Mandle http://dan.mandle.me September 2012
# License: GPL 2.0

# modified by GPS-Robotics-Team

# This module creates a gps-background instance (Thread), which constantly updates the current GPS-data.
# To include the module: import gpsdData
# To create an instance & start it immediately: gpsp = gpsdData.GpsPoller()
# To create an instance & start it later: gpsp = gpsdData.GpsPoller(start = False), start it later by gpsp.start()
# If the instance is started already, data can be read by: gpsp.data, this is up-to-data-data. It will return a list:
#
# data = [gpsd.fix.latitude, gpsd.fix.longitude, gpsd.fix.altitude, gpsd.fix.track, gpsd.satellites, time.time()]
#
# whereby time.time() is the time of the GPS-measurement
# if no valid data is received (also in the begining), all entries of data are float('nan').
# This can be checked by (import math) math.isnan(data[i]) or data[i] == data[i] (False if nan)

#from __main__ import lg
from gps import *
from time import *
import time
import threading
import smbus
import time
import math

bus = smbus.SMBus(1) # compass address (bus number)
address = 0x1e # compass address

def read_byte(adr): # FOR COMPASS
	return bus.read_byte_data(address, adr)

def read_word(adr): # FOR COMPASS
	high = bus.read_byte_data(address, adr)
	low = bus.read_byte_data(address, adr+1)
	val = (high << 8) + low
	return val

def read_word_2c(adr): # FOR COMPASS
	val = read_word(adr)
	if (val >= 0x8000):
		return -((65535 - val) + 1)
	else:
	        return val

def write_byte(adr, value): # FOR COMPASS
	bus.write_byte_data(address, adr, value)
 
gpsd = None #setting the global variable

class GpsPoller(threading.Thread):
	def __init__(self, start=True):
		threading.Thread.__init__(self)
		global gpsd #bring it in scope
		self.i = 0 # counter for averaging
		self.average_number = 1#5 # number of values for average
		gpsd = gps(mode=WATCH_ENABLE) #starting the stream of info
		self.data = [float('nan'), float('nan'), float('nan'), float('nan'), [], float('nan')]
		self.lat_list = [float('nan')] * self.average_number
		self.long_list = [float('nan')] * self.average_number
		self.alt_list = [float('nan')] * self.average_number
		#data = [gpsd.fix.latitude, gpsd.fix.longitude, gpsd.fix.altitude, gpsd.fix.track, gpsd.satellites, time.time()]

		self.scale = 0.92 # for compass
		self.x_offset = 27 # for compass
		self.y_offset = -133 # for compass
		self.degree_offset = 188 # offset to north in degree

		if (start):
			self.start()

 


	def run(self):
		global gpsd
		self.running = True
		self.i = 0
		while self.running:
      
			# FOR COMPASS
			write_byte(0, 0b01110000) # Set to 8 samples @ 15Hz
			write_byte(1, 0b00100000) # 1.3 gain LSb / Gauss 1090 (default)
			write_byte(2, 0b00000000) # Continuous sampling
				 
			x_out = (read_word_2c(3) - self.x_offset ) * self.scale
			y_out = (read_word_2c(7) - self.y_offset) * self.scale
			z_out = read_word_2c(5) * self.scale
				 
			bearing  = math.degrees(math.atan2(y_out, x_out)) - self.degree_offset
			bearing = bearing%360 # normalize to 0..360
			bearing = 360 - bearing # we want the CLOCKWISE angle between north and compass
			if bearing > 180: # normalize to -180..180
				bearing -= 360

			# FOR GPS
			gpsd.next() #this will continue to loop and grab EACH set of gpsd info to clear the buffer
			self.lat_list[self.i%self.average_number] = gpsd.fix.latitude
			self.long_list[self.i%self.average_number] = gpsd.fix.longitude
			self.alt_list[self.i%self.average_number] = gpsd.fix.altitude
      			self.data = [sum(self.lat_list)/float(len(self.lat_list)), sum(self.long_list)/float(len(self.long_list)), sum(self.alt_list) / float(len(self.alt_list)), bearing, gpsd.satellites, time.time()]
			self.i += 1

gps = GpsPoller()
while math.isnan(gps.data[0]):
	pass
print "got it no average:"
time.sleep(20)

start_time = time.time()
dat = gps.data[0:2]
n=0
av=0
stop_time = time.time()

for i in range(30):

	while gps.data[0:2] == dat:
		stop_time = time.time()
	av += (stop_time-start_time)
	n += 1
	print str(stop_time-start_time) + "s; average: " + str(av/n)
	start_time = time.time()
	stop_time = time.time()
	dat = gps.data[0:2]


gps.running = False
print "finished"
