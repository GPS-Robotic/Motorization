#! /usr/bin/python
# Written by Dan Mandle http://dan.mandle.me September 2012
# License: GPL 2.0

# modified by GPS-Robotics-Team
 
from gps import *
from time import *
import time
import threading
 
gpsd = None #setting the global variable
 
class GpsPoller(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    global gpsd #bring it in scope
    gpsd = gps(mode=WATCH_ENABLE) #starting the stream of info
    self.data = [float('nan'), float('nan'), float('nan'), float('nan'), [], float('nan')]
    	#data = [gpsd.fix.latitude, gpsd.fix.longitude, gpsd.fix.altitude, gpsd.fix.track, gpsd.satellites, time.time()]
    self.running = True
    self.start()
 
  def run(self):
    global gpsd
    while self.running:
      gpsd.next() #this will continue to loop and grab EACH set of gpsd info to clear the buffer
      self.data = [gpsd.fix.latitude, gpsd.fix.longitude, gpsd.fix.altitude, gpsd.fix.track, gpsd.satellites, time.time()]

