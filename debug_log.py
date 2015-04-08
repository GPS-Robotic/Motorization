# This is a function to control console-output and to safe it to a file via debug-level
# initialize this at the begining of the main-file via
#	from debug_log import debug_print
#	lg = debug_print( --PARAMETERS-- )
#
# all parameters are optional. their default values and significance are:
# 	debug_level = 0
#		all messages with level equal or higher than debug_level will be print on screen
#	save_debug = False
#		messages will be saved to file additionally, if True
#	filename = ""
#		filename, where messages should be saved
#		standard-filename: "debug"+str(time.time())+".txt"
#	save_level = ""
#		all messages with level equal or higher than save_level will be saved to file
#		standard-level: save_level = debug_level
#	time_stamp = False
#		time.time() will be added to output
#
# to print / save a message on debug level, use (in main)
#	lg.prt( --PARAMETERS / MESSAGES-- )
# or (in any module)
#	from __main__ import lg
#	lg.prt( --PARAMETERS / MESSAGES-- )
#
# as parameters / messages for the output, use:
#	any number of objects, seperated by ','; they will be print in the same way as via 'print'
#	parameters as follows:
#		lv = ""
#			setting the output-level, if not set or "": will be print and saved anyway
#		inst = ""
#			giving a name of the instance sending the message (if "", won't be print)
#			HINT: use inst=__name__ to automatically generate module-(file-)name
#
# IMPORTANT: the parameters lv & inst must be set as last parameters, else: error!
#
# valid use-example in module:
#	lst = [1, "hallo", 3.4]
#	from __main__ import lg
#	lg.prt(lst, "test", True, 0, lv=5, inst=__name__)
#
#
# SUGGESTED LEVELS:
#
#	10	useless, any
#	100	info
#	1000	debug
#	10000	warning
#	100000	error

import time

class debug_print:
	def __init__(self, debug_level=0, save_debug=False, filename="", save_level="", time_stamp=False):
		self.save_level=save_level
		if save_level == "":
			self.save_level = debug_level
		
		self.filename = filename
		if filename == "":
			self.filename="debug"+str(time.time())+".txt"

		self.debug_level = debug_level
		self.time_stamp = time_stamp
		self.save_debug = save_debug

		if save_debug:
			self.log_file=open(self.filename, 'a')
			self.opened = True

	def prt(self, *args, **keyargs): #*message, lv="", inst=""):
		lv = ""
		inst = ""

		if "lv" in keyargs:
			lv = keyargs["lv"]
		if "inst" in keyargs:
			inst = keyargs["inst"]

		total_message = ""
		if lv != "":
			total_message = "[" + str(lv) + "] "
		if self.time_stamp:
			total_message += str(time.time()) + " "
		if inst != "":
			total_message += str(inst) + ": "
		for entry in args:
			total_message +=  str(entry) + " "

		if lv == "" or lv >= self.debug_level:
			print total_message

		if lv == "" or lv >= self.save_level and self.save_debug:
			self.log_file.write(total_message + "\n")			

	def stop(self):
		if self.opened:
			self.log_file.close()
			self.opened = False
