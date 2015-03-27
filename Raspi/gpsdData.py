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

 
from gps import *
from time import *
import time
import threading
 
gpsd = None #setting the global variable

class GpsPoller(threading.Thread):
  def __init__(self, start=True):
    threading.Thread.__init__(self)
    global gpsd #bring it in scope
    self.i = 0 # counter for averaging
    self.average_number = 5 # number of values for average
    gpsd = gps(mode=WATCH_ENABLE) #starting the stream of info
    self.data = [float('nan'), float('nan'), float('nan'), float('nan'), [], float('nan')]
    self.lat_list = [float('nan')] * self.average_number
    self.long_list = [float('nan')] * self.average_number
    self.alt_list = [float('nan')] * self.average_number
    	#data = [gpsd.fix.latitude, gpsd.fix.longitude, gpsd.fix.altitude, gpsd.fix.track, gpsd.satellites, time.time()]
    if (start):
    	self.start()
 
  def run(self):
    global gpsd
    self.running = True
    self.i = 0
    while self.running:
      gpsd.next() #this will continue to loop and grab EACH set of gpsd info to clear the buffer
      self.lat_list[self.i%self.average_number] = gpsd.fix.latitude
      self.long_list[self.i%self.average_number] = gpsd.fix.longitude
      self.alt_list[self.i%self.average_number] = gpsd.fix.altitude
      self.data = [sum(self.lat_list)/float(len(self.lat_list)), sum(self.long_list)/float(len(self.long_list)), sum(self.alt_list) / float(len(self.alt_list)), gpsd.fix.track, gpsd.satellites, time.time()]
      self.i += 1
