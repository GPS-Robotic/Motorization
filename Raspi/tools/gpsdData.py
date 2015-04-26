# ONLY FOR TOOLS-USE HERE! IF YOU WANT TO CHANGE THIS MODULE, YOU HAVE TO CHANGE IT IN MAIN DIRECTORY, TOO!

#! /usr/bin/python
# Written by Dan Mandle http://dan.mandle.me September 2012
# License: GPL 2.0

# modified by GPS-Robotics-Team

# This module creates a gps-background instance (Thread), which constantly updates the current GPS-data & compass.
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
#
# The GPS-data will be averaged over self.averaging_number (e.g. 10) values.
# The variable self.is_new tells wether the averaged data has changed by more than 2*sigma (self.sigma) since the last time fetching data.
#	In this way fluctuations due to bad GPS-data are avoided.
#

from __main__ import lg
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
		self.average_number = 10 # number of values for average
		gpsd = gps(mode=WATCH_ENABLE) #starting the stream of info
		self.data = [float('nan'), float('nan'), float('nan'), float('nan'), [], float('nan')] # averaged data
		self.raw_data = self.data # not averaged data
		self.lat_list = [float('nan')] * self.average_number
		self.long_list = [float('nan')] * self.average_number
		self.alt_list = [float('nan')] * self.average_number
		#data = [gpsd.fix.latitude, gpsd.fix.longitude, gpsd.fix.altitude, gpsd.fix.track, gpsd.satellites, time.time()]

		self.scale = 0.92 # for compass
		self.x_offset = 27 # for compass
		self.y_offset = -133 # for compass
		self.degree_offset = 188 # offset to north in degree

		self.sigma = 0.0000075 # standart-deviation for data; CAUTION: has to be adjusted for average_number;
			      #  av_nmb = 1 --> sigma = 0.00005
			      #  av_nmb = 5 --> sigma = 0.00001
			      #  av_nmb = 10 --> sigma = 0.0000075

		self.is_new = True # tells, whether new data is out of 2-sigma-range since last fetch
		self.last = [0.0, 0.0] # last fetched data

		if (start):
			self.start()

 
	def fetch(self): # returns averaged data
		self.is_new = False
		self.last = self.raw_data[0:2]
		return self.data

	def fetch_raw(self): # return raw data (not averaged)
		self.is_new = False
		self.last = self.raw_data[0:2]
		return self.raw_data

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

			self.data[3] = bearing # update compass-data immediately

			# FOR GPS
			gpsd.next() # this will continue to loop and grab EACH set of gpsd info to clear the buffer
			if [gpsd.fix.latitude, gpsd.fix.longitude] != [self.lat_list[(self.i-1)%self.average_number], self.long_list[(self.i-1)%self.average_number]]: # check whether new data is available

				self.lat_list[self.i%self.average_number] = gpsd.fix.latitude
				self.long_list[self.i%self.average_number] = gpsd.fix.longitude
				self.alt_list[self.i%self.average_number] = gpsd.fix.altitude
	      			self.data = [sum(self.lat_list)/float(len(self.lat_list)), sum(self.long_list)/float(len(self.long_list)), sum(self.alt_list) / float(len(self.alt_list)), bearing, gpsd.satellites, time.time()]
				self.i += 1

				# save raw_data also (not averaged)
				self.raw_data = [gpsd.fix.latitude, gpsd.fix.longitude, gpsd.fix.altitude, bearing, gpsd.satellites, time.time()] 

				dist = math.sqrt( (self.raw_data[0]-self.last[0])*(self.raw_data[0]-self.last[0]) +  (self.raw_data[1]-self.last[1])*(self.raw_data[1]-self.last[1]) )
				if dist > 2*self.sigma: # check if we moved more than 2 sigma (to avoid noise)
					self.is_new = True
				

			time.sleep(0.05) # it takes about 0.25s for the gps to deliver new data

