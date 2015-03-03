#! /usr/bin/python
# Written by Dan Mandle http://dan.mandle.me September 2012
# License: GPL 2.0
 
import os
from gps import *
from time import *
import time
import threading
 
gpsd = None #setting the global variable
 
#os.system('clear') #clear the terminal (optional)
 
class GpsPoller(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    global gpsd #bring it in scope
    gpsd = gps(mode=WATCH_ENABLE) #starting the stream of info
    self.data = [float('nan'), float('nan'), float('nan'), float('nan'), [], float('nan')]
#data = [gpsd.fix.latitude, gpsd.fix.longitude, gpsd.fix.altitude, gpsd.fix.track, gpsd.satellites, time.time()]
    self.current_value = None
    self.running = True #setting the thread running to true
 
  def run(self):
    global gpsd
    while gpsp.running:
      gpsd.next() #this will continue to loop and grab EACH set of gpsd info to clear the buffer
      self.data = [gpsd.fix.latitude, gpsd.fix.longitude, gpsd.fix.altitude, gpsd.fix.track, gpsd.satellites, time.time()]
 
gpsp = GpsPoller() # create the thread
try:
  gpsp.start() # start it up
 
except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
  print "ERROR FROM GPS, EXITING:"
  print KeyboardInterrupt
  print SystemExit
  gpsp.running = False
  gpsp.join() # wait for the thread to finish what it's doing
